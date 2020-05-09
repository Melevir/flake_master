import configparser
from typing import Optional

from requests import get

from flake_master.common_types import Flake8Preset


def load_preset_from_file(preset_file_path: str) -> Optional[Flake8Preset]:
    with open(preset_file_path, 'r') as file_handler:
        raw_text = file_handler.read()
    return parse_preset_from_str_config(raw_text, preset_file_path=preset_file_path)


def load_preset_from_url(preset_url: str) -> Optional[Flake8Preset]:
    raw_text = get(preset_url).text
    return parse_preset_from_str_config(raw_text, preset_url=preset_url)


def parse_preset_from_str_config(
    raw_text: str,
    preset_file_path: str = None,
    preset_url: str = None,
) -> Flake8Preset:
    parser = configparser.ConfigParser()
    parser.read_string(raw_text)
    return Flake8Preset(
        name=parser['info']['name'],
        revision=parser['info']['revision'],
        config_url=preset_url,
        filepath=preset_file_path,
        flake8_plugins=list(parser['flake8_plugins'].items()),
        flake8_config=list(parser['flake8_config'].items()),
    )
