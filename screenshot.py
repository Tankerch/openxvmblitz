from PIL import ImageGrab

from config import AppConfig


def get_game_screenshot():
    return ImageGrab.grab(
        (AppConfig.first_point[0], AppConfig.first_point[1], AppConfig.second_point[0], AppConfig.second_point[1]))


if __name__ == "__main__":
    image = get_game_screenshot()
    image.show()
