import time
from multiprocessing.pool import ThreadPool

from colorama import Fore, Back
from colorama import init
from pynput import keyboard

from config import AppConfig
from gui import ConsoleGui
from player_service import WgApiService
from preprocess_image import processing_before_ocr, get_players_list
from screenshot import get_players_list_img, get_wotb_window

processing = False


def start_xvm():
    print("Start Processing Screenshot")
    start_time = time.perf_counter()
    print(Fore.RESET + Back.RESET)

    # Get Game Loading Snapshot
    wotb_window_img = get_wotb_window()
    player_snapshot_img = get_players_list_img(wotb_window_img)

    # Process Image using OCR
    processed_img = processing_before_ocr(player_snapshot_img)
    allied_section_img = processed_img[0: AppConfig.players_section_h, 0:AppConfig.box_width]
    enemy_section_img = processed_img[0: AppConfig.players_section_h,
                        AppConfig.players_section_w - AppConfig.box_width:AppConfig.players_section_w]

    allied_ign_list = get_players_list(allied_section_img)
    enemy_ign_list = get_players_list(enemy_section_img)

    # Get player data via API
    with ThreadPool() as api_pool:
        api_service = WgApiService()
        allied_pool = api_pool.apply_async(api_service.get_players_stats, (allied_ign_list, "asia"))
        enemy_pool = api_pool.apply_async(api_service.get_players_stats, (enemy_ign_list, "asia"))

        allied_stats = allied_pool.get()
        enemy_stats = enemy_pool.get()

    # Render
    ConsoleGui().render(allied_stats, enemy_stats)
    print(f"Done in {time.perf_counter() - start_time} second(s)")
    print(Fore.WHITE + Back.RESET)


def on_press(key: keyboard.Key | keyboard.KeyCode):
    global processing
    if not hasattr(key, "vk") or processing:
        return
    if key.vk == 99:
        processing = True
        start_xvm()
        processing = False
        print("Start listening... on Numpad 3")


def initialise():
    #  Init Colorama
    init()


def main():
    initialise()
    with keyboard.Listener(on_press=on_press) as listener:
        print("Start listening... on Numpad 3")
        listener.join()


if __name__ == "__main__":
    main()
