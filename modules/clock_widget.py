from typing import Union
from modules.config import Clock
from modules.font import get_font
from modules.inertia import InertialNumber
from modules.clock_images import get_clock_state_images
import pytz
import datetime
import pygame as pg


class ClockWidget:
    def __init__(self, position: Union[tuple, list], size: Union[tuple, list], clock_config: Clock):
        self._x, self._y = self._position = position
        self._w, self._h = self._size = self._original_size = size

        self._clock_state_images = get_clock_state_images()
        self._clock_state_offset = 37800
        self._time_zone = clock_config.time_zone
        self._am_format = clock_config.am_format

        self._inertia = InertialNumber(friction=0.75, force_multiplier=0.25)
        self._inertia.apply_force(250)

        self._clock_text_show = clock_config.clock_text_show
        self._clock_font_scale = clock_config.clock_font_scale
        self._clock_text_offset = clock_config.clock_text_offset
        self._blinking_dots = clock_config.blinking_dots
        self._blink_rarity = clock_config.blink_rarity

    def __get_clock_string(self) -> str:
        try:
            time_zone = pytz.timezone(self._time_zone)
        except pytz.UnknownTimeZoneError:
            time_zone = pytz.timezone("Europe/Moscow")
        
        current_time = datetime.datetime.now(time_zone)

        if self._am_format:
            clock_string = datetime.datetime.strftime(current_time, "%I %M")
        else:
            clock_string = datetime.datetime.strftime(current_time, "%H %M")
        
        return clock_string

    def __get_clock_state(self) -> pg.Surface:
        try:
            time_zone = pytz.timezone(self._time_zone)
        except pytz.UnknownTimeZoneError:
            time_zone = pytz.timezone("Europe/Moscow")

        current_time = datetime.datetime.now(time_zone)
        day_start_time = current_time.replace(hour=0, minute=0, second=0, microsecond=0)
        self._inertia.set_target_value((current_time - day_start_time).seconds)

        day_seconds = (self._inertia.get_value() + self._clock_state_offset) % 86400

        index = int((day_seconds / 86400) * len(self._clock_state_images))

        return self._clock_state_images[index]

    def __render(self) -> pg.Surface:
        surface = pg.Surface(self._size, pg.SRCALPHA)

        clock = pg.transform.scale(self.__get_clock_state(), (self._w / 1.5, self._h / 1.5))
        clock_rect = clock.get_rect(center=(self._w / 2, self._h / 2 - self._h / 16))

        surface.blit(clock, clock_rect)

        if self._clock_text_show:
            clock_font = get_font(int(self._h / 6.4 * self._clock_font_scale))

            clock_text = clock_font.render(self.__get_clock_string(), False, (255, 255, 255))
            clock_text_rect = clock_text.get_rect(center=(self._w / 2, self._h / 2 + self._h / 3.41 + self._clock_text_offset))

            surface.blit(clock_text, clock_text_rect)

            blink_dots = clock_font.render(":", False, (255, 255, 255))
            blink_dots_rect = blink_dots.get_rect(center=(self._w / 2, self._h / 2 + self._h / 3.41 + self._clock_text_offset))

            if self._blinking_dots:
                if int(datetime.datetime.now().timestamp()) % self._blink_rarity:
                    surface.blit(blink_dots, blink_dots_rect)
            else:
                surface.blit(blink_dots, blink_dots_rect)

        return surface

    @property
    def rect(self) -> pg.Rect:
        rect = pg.Rect(0, 0, self._w, self._h)
        rect.center = self._position

        return rect

    def set_position(self, position: Union[tuple, list]) -> None:
        self._x, self._y = self._position = position

    def set_size_scale(self, scale: float) -> None:
        self._w, self._h = self._size = tuple(map(lambda x: x * scale, self._original_size))

    def update(self, dt: int = 1) -> None:
        self._inertia.update(dt * 8)

    def build(self, surface: pg.Surface) -> None:
        rendered_surface = self.__render()
        surface_rect = rendered_surface.get_rect(center=(self._x, self._y))

        surface.blit(rendered_surface, surface_rect)
