import logging
import math
import time

import pywinctl as pwc
from PIL import ImageGrab

from config import AppConfig


def get_players_list_img():
    wotb_window = __get_wotb_windows()

    # Max WoTB player width is 1270 from center
    # Max WoTB player height is 350 from y1
    max_player_width = 1270
    max_player_height = 350

    x_margin = (wotb_window.width - max_player_width) / 2
    x1 = x_margin
    x2 = wotb_window.width - x_margin
    y1 = AppConfig.start_player_y_point
    y2 = y1 + max_player_height
    first_point = (math.floor(x1), math.floor(y1))
    second_point = (math.floor(x2), math.floor(y2))

    return wotb_window.crop(
        (first_point[0], first_point[1], second_point[0], second_point[1]))


def __get_wotb_windows():
    time.sleep(0.1)
    window = pwc.getActiveWindow()
    print(window)
    if "WoT Blitz" not in window.title:
        logging.warning("Active Window is not WoTB, will assume WoTB Blitz is full-screen")
        active_screen = pwc.getScreenSize()
        return ImageGrab.grab((0, 0, active_screen.width, active_screen.height))
    return ImageGrab.grab((window.left, window.top, window.left + window.width, window.top + window.height))


if __name__ == "__main__":
    get_players_list_img().show()
