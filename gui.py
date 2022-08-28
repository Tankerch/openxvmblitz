import tkinter as tk
from abc import abstractmethod

from colorama import Fore

from player_stats import PlayerStats

console_color_code = {
    "unicum": Fore.MAGENTA,
    "normal": Fore.GREEN,
    "bad": Fore.RED
}


class BaseGui:
    @abstractmethod
    def render(self, allied_list: list[PlayerStats], enemy_list: list[PlayerStats]):
        pass


class ConsoleGui(BaseGui):

    def render(self, allied_list: list[PlayerStats], enemy_list: list[PlayerStats]):
        self.__print_allied_output(allied_list)
        print("")
        self.__print_enemy_output(enemy_list)

    @staticmethod
    def __color_avg_damage(avg_damage: int) -> Fore:
        if avg_damage > 1400:
            return console_color_code["unicum"]
        if avg_damage > 1000:
            return console_color_code["normal"]
        return console_color_code["bad"]

    @staticmethod
    def __color_wr(wr: float) -> Fore:
        if wr > 60:
            return console_color_code["unicum"]
        if wr > 50:
            return console_color_code["normal"]
        return console_color_code["bad"]

    @staticmethod
    def __color_wn8(wn8: float) -> Fore:
        if wn8 > 1850:
            return console_color_code["unicum"]
        if wn8 > 1100:
            return console_color_code["normal"]
        return console_color_code["bad"]

    @staticmethod
    def __print_tab(ign: str):
        ign_length = len(ign)
        if ign_length >= 16:
            return "\t"
        if ign_length >= 12:
            return "\t\t"
        if ign_length >= 8:
            return "\t\t\t"
        return "\t\t\t\t"

    def __print_allied_output(self, stats_list: list[PlayerStats]):
        print(Fore.GREEN + "Allied Team")
        for index, stats in enumerate(stats_list):
            if not stats.valid_to_print():
                print(Fore.WHITE + stats.ign)
                continue
            tabs = self.__print_tab(stats.ign)
            print(Fore.WHITE + str(stats.ign) + tabs +
                  self.__color_wr(stats.wr) + f"{stats.wr}%" + "\t\t\t" + self.__color_avg_damage(
                stats.avg_dmg) + f"{stats.avg_dmg}")
            pass

    def __print_enemy_output(self, stats_list: list[PlayerStats]):
        print(Fore.RED + "Enemy Team")
        for index, stats in enumerate(stats_list):
            if not stats.valid_to_print():
                print(Fore.WHITE + stats.ign)
                continue
            tabs = self.__print_tab(stats.ign)
            print(Fore.WHITE + str(stats.ign) + tabs +
                  self.__color_wr(stats.wr) + f"{stats.wr}%" + "\t\t\t" + self.__color_avg_damage(
                stats.avg_dmg) + f"{stats.avg_dmg}")


class OverlayGui(BaseGui):
    __default_font__ = ("Arial", 14, "bold")

    __transparent_color = "white"

    __init_executed = False

    __root = tk.Tk()

    def init(self):
        self.__root.attributes('-fullscreen', True)
        self.__root.wm_attributes("-topmost", True)
        self.__root.wm_attributes("-transparentcolor", "white")
        self.__root.config(bg=self.__transparent_color)

        self.__root.option_add("*font", "Arial 14 bold")
        self.__init_executed = True

    def mainloop(self):
        return self.__root.mainloop()

    @staticmethod
    def __color_for_wr__(wr: float):
        if wr > 60:
            return "magenta"
        if wr > 52:
            return "green"
        return "red"

    @staticmethod
    def __color_avg_dmg__(avg_dmg: int):
        if avg_dmg > 1400:
            return "magenta"
        if avg_dmg > 1000:
            return "green"
        return "red"

    def render(self, allied_list: list[PlayerStats], enemy_list: list[PlayerStats]):
        player_battle_box_width = 400

        if not self.__init_executed:
            self.init()

        # Set to 50% width each frame
        self.__root.columnconfigure(0, weight=1)

        self.__root.columnconfigure(1, weight=1)

        allied_frame = tk.Frame(self.__root)
        allied_frame.config(bg=self.__transparent_color)
        for idx, player in enumerate(allied_list):
            if not player.valid_to_print():
                empty_widget = tk.Label(allied_frame, text="A", bg=self.__transparent_color)
                empty_widget.grid(sticky=tk.W, row=idx, column=0, padx=(player_battle_box_width, 8))
                empty_widget.grid(sticky=tk.W, row=idx, column=1)
                continue
            wr = tk.Label(allied_frame, text=f"{str(player.wr)}%", bg=self.__transparent_color,
                          fg=self.__color_for_wr__(player.wr), font=self.__default_font__)
            dmg = tk.Label(allied_frame, text=str(player.avg_dmg), bg=self.__transparent_color,
                           fg=self.__color_avg_dmg__(player.avg_dmg), font=self.__default_font__)
            wr.grid(sticky=tk.W, row=idx, column=0, padx=(player_battle_box_width, 8))
            dmg.grid(sticky=tk.W, row=idx, column=1)
        allied_frame.grid(column=0, row=0, sticky=tk.NW)

        enemy_frame = tk.Frame(self.__root)
        enemy_frame.config(bg="white")
        for idx, player in enumerate(enemy_list):
            if not player.valid_to_print():
                empty_widget = tk.Label(enemy_frame, text="", bg=self.__transparent_color)
                empty_widget.grid(row=idx, column=1, padx=(8, player_battle_box_width))
                empty_widget.grid(row=idx, column=0)
                continue
            wr = tk.Label(enemy_frame, text=f"{str(player.wr)}%", bg=self.__transparent_color,
                          fg=self.__color_for_wr__(player.wr), font=self.__default_font__)
            dmg = tk.Label(enemy_frame, text=str(player.avg_dmg), bg=self.__transparent_color,
                           fg=self.__color_avg_dmg__(player.avg_dmg), font=self.__default_font__)
            wr.grid(row=idx, column=1, padx=(8, player_battle_box_width))
            dmg.grid(row=idx, column=0)
        enemy_frame.grid(column=1, row=0, sticky=tk.NE)
        self.__root.update()


def __main__():
    gui = OverlayGui()
    allied_list = [PlayerStats(ign=f"allied_{i}", wr=round(60 + i * 0.1, 2), avg_dmg=800 + int(f"{i}00")) for i in
                   range(7)]
    allied_list[1] = PlayerStats(ign="allied_failed")
    enemy_list = [PlayerStats(ign=f"enemy_{i}", wr=round(50 + i, 2), avg_dmg=800 + int(f"{i}00")) for i in range(7)]
    gui.render(allied_list, enemy_list)
    gui.mainloop()


if __name__ == "__main__":
    __main__()
