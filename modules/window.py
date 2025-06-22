from modules.font import get_font
from typing import Optional, Union, List
from modules.clock_widget import ClockWidget
from modules.config import Config
import win32api
import win32con
import win32gui
import pygame as pg


class MainWindow:
    def __init__(self, title: str = "Title", flags: int = 0, fps: int = 60,
                 vsync: bool = False, config: Optional[Config] = None) -> None:

        ... if pg.display.get_init() else pg.display.init()
        ... if pg.font.get_init() else pg.font.init()

        info = pg.display.Info()

        self._w, self._h = self._size = (info.current_w, info.current_h)
        self._title = title
        self._flags = flags
        self._fps = fps
        self._vsync = vsync

        self._window = pg.display.set_mode(self._size, self._flags, vsync=self._vsync)
        self._clock = pg.time.Clock()

        self._is_running = False
        self._show_fps = False
        self._show_hitboxes = False

        self._update_rects: List[pg.Rect] = []
        self._old_update_rects: List[pg.Rect] = []

        self._config = config
        
        if self._config:
            position = self._config.position.position
            size = tuple(map(lambda x: x * self._config.position.size_scale, (256, 256)))
            self._clock_widget = ClockWidget(position, size, self._config.clock)

        self.__setup()

    def __setup(self) -> None:
        pg.display.set_caption(self._title)
        pg.display.set_icon(pg.image.load("icon.ico"))

        hwnd = pg.display.get_wm_info()["window"]

        self.set_transparent_color(hwnd, (0, 0, 255))

        if self._config.lay_top_most:
            self.set_top_most(hwnd)

        allowed_events = [pg.QUIT, pg.MOUSEMOTION, pg.MOUSEBUTTONDOWN, pg.MOUSEBUTTONUP, pg.KEYDOWN, pg.KEYUP]
        pg.event.set_allowed(allowed_events)

        self._update_rects.append(pg.Rect(0, 0, self._w, self._h))

    def __clear_update_rects(self) -> None:
        self._old_update_rects = []
        self._old_update_rects = self._update_rects
        self._update_rects = []

    def set_config(self, config: Config) -> None:
        self._config = config

    def set_transparent_color(self, hwnd: int, color: Union[tuple, list]) -> None:
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                       win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
        win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*color), 0, win32con.LWA_COLORKEY)

    def set_top_most(self, hwnd: int) -> None:
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOSIZE)
    
    def unset_top_most(self, hwnd: int) -> None:
        win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0, win32con.SWP_NOSIZE | win32con.SWP_NOMOVE)

    def start_loop(self, debug: bool = False) -> None:
        self._is_running = True
        while self._is_running:
            dt = self._clock.tick(self._fps) / 1000

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.close()
                    break

                if event.type == pg.MOUSEMOTION:
                    if self._clock_widget.rect.collidepoint(event.pos) and pg.mouse.get_pressed()[0]:
                        self._config.position.position = event.pos

                        if not self._config.position.lock_widget:
                            self._clock_widget.set_position(self._config.position.position)
                
                if event.type == pg.MOUSEWHEEL:
                    if self._clock_widget.rect.collidepoint(pg.mouse.get_pos()):
                        if not self._config.position.lock_widget:
                            scroll = round(event.y / 50, 2)

                            if 0.25 < self._config.position.size_scale + scroll < 4.0:
                                self._config.position.size_scale += scroll

                                self._clock_widget.set_size_scale(self._config.position.size_scale)

                if event.type == pg.KEYDOWN:
                    mods = pg.key.get_mods()

                    if mods & pg.KMOD_CTRL and event.key == pg.K_f:
                        if not self._config.position.lock_widget:
                            self._clock_widget.set_position((self._w / 2, self._h / 2))
                    
                    if mods & pg.KMOD_CTRL and event.key == pg.K_l:
                        self._config.position.lock_widget = not self._config.position.lock_widget
                    
                    if mods & pg.KMOD_CTRL and event.key == pg.K_t:
                        hwnd = pg.display.get_wm_info()["window"]

                        if self._config.lay_top_most:
                            self.unset_top_most(hwnd)
                            self._config.lay_top_most = False
                        else:
                            self.set_top_most(hwnd)
                            self._config.lay_top_most = True
                    
                    if mods & pg.KMOD_CTRL and event.key == pg.K_ESCAPE:
                        self.close()

                    if mods & pg.KMOD_CTRL and event.key == pg.K_p and debug:
                        self._show_fps = not self._show_fps
                    
                    if mods & pg.KMOD_CTRL and event.key == pg.K_h and debug:
                        self._show_hitboxes = not self._show_hitboxes

            self._window.fill((0, 0, 255))

            if self._show_fps:
                font = get_font(36)
                text = font.render(f"Fps: {round(self._clock.get_fps(), 2)}", False, (255, 0, 0))
                text_rect = text.get_rect()
                text_rect.bottomleft = (15, self._h - 15)

                self._window.blit(text, text_rect)
                self._update_rects.append(text_rect)
            
            if self._show_hitboxes:
                pg.draw.rect(self._window, (255, 0, 0), self._clock_widget.rect, 2)

            self._clock_widget.update(dt)
            self._clock_widget.build(self._window)
            self._update_rects.append(self._clock_widget.rect)

            pg.display.update(self._update_rects + self._old_update_rects)
            self.__clear_update_rects()

    def close(self) -> None:
        self._is_running = False
        