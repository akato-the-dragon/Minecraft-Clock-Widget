from dacite import from_dict
from dataclasses import dataclass, field, asdict
import os
import json

CONFIG_PATH = "config.json"
CONFIG_ENCODING = "utf-8"


@dataclass
class Position:
    position: list = field(default_factory=lambda: [250, 250])
    size_scale: float = 1.0
    lock_widget: bool = False

@dataclass
class Clock:
    time_zone: str = "Europe/Moscow"
    am_format: bool = False

    clock_text_show: bool = False
    clock_text_offset: int = 0
    clock_font_scale: float = 1.0

    blinking_dots: bool = True
    blink_rarity: int = 2

@dataclass
class Config:
    position: Position = field(default_factory=Position)
    clock: Clock = field(default_factory=Clock)
    lay_top_most: bool = True
    fps: int = 30
    vsync: bool = False
    debug: bool = False


def new_config() -> None:
    with open(CONFIG_PATH, "w", encoding=CONFIG_ENCODING) as new_file:
        json.dump(asdict(Config()), new_file, ensure_ascii=False, indent=4)


def load_config() -> Config:
    if not os.path.exists(CONFIG_PATH):
        new_config()

    with open(CONFIG_PATH, encoding=CONFIG_ENCODING) as load_file:
        data = json.load(load_file)

    return from_dict(Config, data)


def save_config(data: Config) -> None:
    with open(CONFIG_PATH, "w", encoding=CONFIG_ENCODING) as save_file:
        json.dump(asdict(data), save_file, ensure_ascii=False, indent=4)
