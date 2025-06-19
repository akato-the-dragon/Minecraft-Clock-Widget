import pygame as pg

FONT_PATH = "resources/minecrafter.ttf"


def get_font(size: int) -> pg.font.Font:
    return pg.font.Font(FONT_PATH, size)
