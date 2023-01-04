import asyncio
import time

import colorama
from pynput import keyboard

from config import AppConfig
from gui import TableGui
from player_service import WgApiService
from player_stats import PlayerStats
from preprocess_image import processing_before_ocr, get_players_list
from screenshot import get_players_list_img, get_wotb_window

processing = False

render_service = TableGui()
api_service = WgApiService()


def start_xvm():
    print("Start Processing Screenshot")
    start_time = time.perf_counter()
    print(colorama.Fore.RESET + colorama.Back.RESET)

    # Get Game Loading Snapshot
    wotb_window_img = get_wotb_window()
    player_snapshot_img = get_players_list_img(wotb_window_img)

    # Process Image using OCR
    processed_img = processing_before_ocr(player_snapshot_img)
    allied_section_img = processed_img[0: AppConfig.players_section_h,
                                       0:AppConfig.box_width]
    enemy_section_img = processed_img[0: AppConfig.players_section_h,
                                      AppConfig.players_section_w - AppConfig.box_width:AppConfig.players_section_w]

    allied_ign_list = get_players_list(allied_section_img)
    enemy_ign_list = get_players_list(enemy_section_img)

    # Get player data via API
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    allied_tasks = [api_service.get_stats(ign) for ign in allied_ign_list]
    enemy_tasks = [api_service.get_stats(ign) for ign in enemy_ign_list]

    allied_stats: list[PlayerStats] = loop.run_until_complete(asyncio.gather(
        *allied_tasks
    ))
    enemy_stats: list[PlayerStats] = loop.run_until_complete(asyncio.gather(
        *enemy_tasks
    ))

    # Render
    render_service.render(allied_stats, enemy_stats)
    print(f"Done in {time.perf_counter() - start_time} second(s)")
    print(colorama.Fore.WHITE + colorama.Back.RESET)


def on_press(key: keyboard.Key | keyboard.KeyCode):
    global processing
    if not hasattr(key, "vk") or processing:
        return
    if key.vk == 99:
        processing = True
        start_xvm()
        processing = False
        print("Start listening... on Numpad 3")


def main():
    with keyboard.Listener(on_press=on_press) as listener:
        print("Start listening... on Numpad 3")
        listener.join()


if __name__ == "__main__":
    main()
