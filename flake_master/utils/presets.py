import configparser
import json
import os
from typing import List, Tuple, Optional

from click import echo

from flake_master.common_types import Flake8Preset, Flake8PresetInfo
from flake_master.utils.preset_fetchers import load_preset_from_file, load_preset_from_url
from flake_master.utils.requirements import merge_requirements_data


def fetch_preset(
    preset_name_or_url_or_path: str = None,
    preset_info: Flake8PresetInfo = None,
    presets_repo_url: str = 'https://raw.githubusercontent.com/Melevir/flake_master_presets',
) -> Optional[Flake8Preset]:
    preset = None

    preset_file_path, preset_url = extract_preset_credentials(
        preset_name_or_url_or_path,
        preset_info,
        presets_repo_url,
    )

    if preset_file_path:
        preset = load_preset_from_file(preset_file_path)
    if not preset and preset_url:
        preset = load_preset_from_url(preset_url)
    return preset


def extract_preset_credentials(
    preset_name_or_url_or_path: Optional[str],
    preset_info: Optional[Flake8PresetInfo],
    presets_repo_url: str,
) -> Tuple[Optional[str], Optional[str]]:
    return (
        extract_preset_file_path(preset_name_or_url_or_path, preset_info),
        extract_preset_url(preset_name_or_url_or_path, preset_info, presets_repo_url),
    )


def extract_preset_file_path(
    preset_name_or_url_or_path: Optional[str],
    preset_info: Optional[Flake8PresetInfo],
) -> Optional[str]:
    preset_file_path = None
    if (
        preset_name_or_url_or_path
        and preset_name_or_url_or_path.endswith('.cfg')
        and os.path.exists(preset_name_or_url_or_path)
    ):
        preset_file_path = os.path.abspath(preset_name_or_url_or_path)
    if preset_info and preset_info['filepath']:
        preset_file_path = preset_info['filepath']
    return preset_file_path


def extract_preset_url(
    preset_name_or_url_or_path: Optional[str],
    preset_info: Optional[Flake8PresetInfo],
    presets_repo_url: str,
) -> Optional[str]:
    preset_url = None
    if preset_name_or_url_or_path and preset_name_or_url_or_path.startswith('http'):
        preset_url = preset_name_or_url_or_path
    if preset_info and preset_info['url']:
        preset_url = preset_info['url']
    if not preset_url and preset_name_or_url_or_path:
        preset_url = f'{presets_repo_url}/master/presets/{preset_name_or_url_or_path}.cfg'
    return preset_url


def apply_preset_to_path(
    preset: Flake8Preset,
    project_path: str,
    preset_file_name: str,
) -> None:
    echo(f'\tAdding {len(preset.flake8_plugins)} requirements...')
    add_packages_to_requirements_file(
        preset.flake8_plugins,
        project_path,
        requirements_files_names=['requirements_dev.txt', 'requirements.txt'],
        default_requirements_file_name='requirements.txt',
    )
    echo('\tCreating flake8 config...')
    add_flake8_config(preset.flake8_config, project_path, config_file_name='setup.cfg')
    echo('\tCreating preset file...')
    create_preset_file(preset, project_path, preset_file_name=preset_file_name)


def add_packages_to_requirements_file(
    flake8_plugins: List[Tuple[str, str]],
    project_path: str,
    requirements_files_names: List[str],
    default_requirements_file_name: str,
) -> None:
    for requirements_file_name in requirements_files_names:
        requirements_file_path = os.path.join(project_path, requirements_file_name)
        if not os.path.exists(requirements_file_path):
            continue
        echo(f'\t\tadding to {requirements_file_path}...')
        with open(requirements_file_path, 'r') as file_handler:
            raw_old_requirements = [l.strip() for l in file_handler.readlines()]
        requirements = merge_requirements_data(raw_old_requirements, flake8_plugins)
        with open(requirements_file_path, 'w') as file_handler:
            file_handler.write(requirements)
        break
    else:
        echo(f'\t\tcreating {default_requirements_file_name}...')
        with open(os.path.join(project_path, default_requirements_file_name), 'w') as file_handler:
            file_handler.write('\n'.join(f'{p}=={v}' for (p, v) in flake8_plugins))


def add_flake8_config(
    flake8_config: List[Tuple[str, str]],
    project_path: str,
    config_file_name: str,
    flake8_section_name: str = 'flake8',
) -> None:
    config_path = os.path.join(project_path, config_file_name)
    parser = configparser.ConfigParser()
    if not os.path.exists(config_path):
        echo(f'\t\tconfig file {config_path} not found', err=True)
    else:
        echo(f'\t\tUpdating {config_path}...')
        parser.read(config_path)

    if flake8_section_name not in parser:
        parser.add_section(flake8_section_name)
    for param_name, param_value in flake8_config:
        parser[flake8_section_name][param_name] = param_value

    with open(config_path, 'w') as file_handler:
        parser.write(file_handler)


def create_preset_file(preset: Flake8Preset, project_path: str, preset_file_name: str) -> None:
    preset_file_path = os.path.join(project_path, preset_file_name)
    with open(preset_file_path, 'w') as file_handler:
        json.dump({
            'name': preset.name,
            'revision': preset.revision,
            'url': preset.config_url,
            'filepath': preset.filepath,
        }, file_handler)
