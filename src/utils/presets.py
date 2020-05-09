import configparser
import json
import os
from typing import List, Tuple

from click import echo

from common_types import Flake8Preset
from utils.requirements import merge_requirements_data


def fetch_preset(preset_name: str) -> Flake8Preset:
    return Flake8Preset(  # TODO
        name='test_preset',
        revision='1',
        config_url='https://github.com/',
        flake8_plugins=[
            ('pydocstyle', '3.0.0'),
            ('flake8', '3.7.9'),
            ('flake8-2020', '1.6.0'),
            ('flake8-blind-except', '0.1.1'),
            ('flake8-bugbear', '20.1.4'),
        ],
        flake8_config=[
            ('max-complexity', '18'),
            ('max-annotations-complexity', '4'),
            ('max-line-length', '120'),
            ('ignore', 'W503, P103, D'),
        ],
    )


def apply_preset_to_path(
    preset: Flake8Preset,
    project_path: str,
    preset_file_name='.flake_master',
) -> None:
    preset_file_path = os.path.join(project_path, preset_file_name)
    if os.path.exists(preset_file_path):
        echo(
            f'Preset file ({preset_file_path}) already exists. Looks like flake master '
            f'has already been deployed to {project_path}. May be you mean `upgrade`, not `setup`?',
            err=True
        )
        exit(1)
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
    default_requirements_file_name: str
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
            'url': preset.config_url
        }, file_handler)
