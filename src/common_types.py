from typing import Tuple, List, NamedTuple


class Flake8Preset(NamedTuple):
    name: str
    revision: str
    config_url: str
    flake8_plugins: List[Tuple[str, str]]
    flake8_config: List[Tuple[str, str]]
