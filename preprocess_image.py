import os.path
import re
from math import floor

import cv2
import numpy
import pytesseract
from PIL import Image

from config import AppConfig
from screenshot import get_players_list_img

__max_player = 7


def processing_before_ocr(src_img: Image):
    grey_image = cv2.cvtColor(numpy.array(src_img), cv2.COLOR_RGB2GRAY)
    thresh = cv2.threshold(grey_image, 180, 255,
                           cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    norm = cv2.distanceTransform(thresh, cv2.DIST_L2, 5)
    norm = cv2.normalize(norm, norm, 0, 1.0, cv2.NORM_MINMAX)
    norm = (norm * 255).astype("uint8")

    after_thresh = cv2.threshold(
        norm, 0, 255, cv2.THRESH_BINARY_INV)[1]
    return after_thresh


def get_players_list(cropped_image):
    player_box_h = floor(AppConfig.players_section_h / __max_player)
    names: list[str] = []
    for i in range(__max_player):
        player_box = cropped_image[player_box_h *
                                   i: player_box_h * (i + 1), 0:AppConfig.box_width]
        player_box = cv2.resize(player_box, None, fx=2,
                                fy=2, interpolation=cv2.INTER_CUBIC)
        player_ign = __get_ign_from_image(player_box)
        if player_ign is None:
            continue
        names.append(player_ign)
    return names


def __get_ign_from_image(full_img):
    result = pytesseract.image_to_string(full_img, config="--psm 7")
    if result is None:
        return None
    if len(result) < 5:
        return None
    result = re.sub("[{|(\[].*[}|)\]](.*?)([{|(\[].*[}|)\]])?", "", result)
    result = result.strip().replace(" ", "")
    return result


def __main__():
    for i in range(3):
        test_image = Image.open(os.path.relpath(
            f"static/Screenshot_{i + 1}.jpg"))
        test_image = get_players_list_img(test_image)
        processed_image = processing_before_ocr(test_image)
        cv2.imshow("asd", processed_image)
        cv2.waitKey()


if __name__ == "__main__":
    __main__()
