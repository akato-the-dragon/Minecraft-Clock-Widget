import pygame as pg

CLOCK_STATES_FOLDER = "resources/clock_states"


def get_clock_state_images(name: str = "clock_{}.png", states: int = 64) -> list[pg.Surface]:
    clock_states = []
    for clock_state in range(1, states):
        clock_state_image = pg.image.load(f"{CLOCK_STATES_FOLDER}/{name.format(clock_state)}")
        clock_states.append(clock_state_image)

    return clock_states
