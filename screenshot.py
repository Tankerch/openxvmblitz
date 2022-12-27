import logging
import math

import pywinctl as pwc
from PIL import ImageGrab, Image

from config import AppConfig


def get_players_list_img(wotb_window: Image):
    # Max WoTB player width is 1270 from center
    # Max WoTB player height is 350 from y1
    section_w = AppConfig.players_section_w
    section_h = AppConfig.players_section_h

    x_margin = (wotb_window.width - section_w) / 2
    x1 = x_margin
    x2 = wotb_window.width - x_margin
    y1 = AppConfig.start_player_y_point
    y2 = y1 + section_h
    first_point = (math.floor(x1), math.floor(y1))
    second_point = (math.floor(x2), math.floor(y2))

    return wotb_window.crop((first_point[0], first_point[1], second_point[0], second_point[1]))


def get_wotb_window() -> Image:
    window = pwc.getActiveWindow()
    if "WoT Blitz" not in window.title:
        logging.warning(
            "Active Window is not WoTB, will assume WoTB Blitz is full-screen")
        active_screen = pwc.getScreenSize()
        return ImageGrab.grab((0, 0, active_screen.width, active_screen.height))
    return ImageGrab.grab((window.left, window.top, window.left + window.width, window.top + window.height))


def __main__():
    wotb_window = get_wotb_window()
    get_players_list_img(wotb_window).show()


if __name__ == "__main__":
    __main__()
