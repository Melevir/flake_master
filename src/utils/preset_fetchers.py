import configparser
from typing import Optional

from common_types import Flake8Preset


def load_preset_from_file(preset_file_path: str) -> Optional[Flake8Preset]:
    parser = configparser.ConfigParser()
    parser.read(preset_file_path)
    url = None if parser['info']['config_url'] == 'None' else parser['info']['config_url']
    return Flake8Preset(
        name=parser['info']['name'],
        revision=parser['info']['revision'],
        config_url=url,
        filepath=preset_file_path,
        flake8_plugins=list(parser['flake8_plugins'].items()),
        flake8_config=list(parser['flake8_config'].items()),
    )


def load_preset_from_url(preset_url: str) -> Optional[Flake8Preset]:
    return None
