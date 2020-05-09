from typing import Tuple, List, NamedTuple, Optional

from typing_extensions import TypedDict


class Flake8Preset(NamedTuple):
    name: str
    revision: str
    config_url: Optional[str]
    filepath: Optional[str]
    flake8_plugins: List[Tuple[str, str]]
    flake8_config: List[Tuple[str, str]]


class Flake8PresetInfo(TypedDict):
    name: str
    revision: str
    url: Optional[str]
    filepath: Optional[str]
