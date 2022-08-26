import time
from multiprocessing.pool import ThreadPool

from colorama import Fore, Back
from colorama import init
from pynput import keyboard

from gui import ConsoleGui
from player_service import WgApiService
from preprocess_image import get_allied_list, get_enemy_list, processing_before_ocr
from screenshot import get_players_list_img

processing = False


def start_xvm():
    print("Start Processing Screenshot")
    start_time = time.perf_counter()
    print(Fore.RESET + Back.RESET)
    # Get Game Loading Snapshot
    raw_snapshot = get_players_list_img()

    # Process Image to OCR ready
    processed_image = processing_before_ocr(raw_snapshot)
    allied_ign_list = get_allied_list(processed_image)
    enemy_ign_list = get_enemy_list(processed_image)

    # Web scrapping data
    pool = ThreadPool()
    api_service = WgApiService()
    allied_pool = pool.apply_async(api_service.get_players_stats, (allied_ign_list, "asia"))
    enemy_pool = pool.apply_async(api_service.get_players_stats, (enemy_ign_list, "asia"))

    allied_stats = allied_pool.get()
    enemy_stats = enemy_pool.get()

    ConsoleGui().render(allied_stats, enemy_stats)
    print(Fore.WHITE + Back.RESET)
    print(f"Done in {time.perf_counter() - start_time} second")


def on_press(key: keyboard.Key | keyboard.KeyCode):
    global processing
    if not hasattr(key, "vk") or processing:
        return
    if key.vk == 99:
        processing = True
        start_xvm()
        processing = False


def main():
    init()
    with keyboard.Listener(on_press=on_press) as listener:
        print("Start listening... on Numpad 3")
        listener.join()


if __name__ == "__main__":
    main()
