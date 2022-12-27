import os
import tkinter as tk
from abc import abstractmethod
import prettytable
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


class ColorStatsMixin:
    @staticmethod
    def color_avg_damage(avg_damage: int) -> Fore:
        if avg_damage > 1400:
            return console_color_code["unicum"]
        if avg_damage > 1000:
            return console_color_code["normal"]
        return console_color_code["bad"]

    @staticmethod
    def color_wr(wr: float) -> Fore:
        if wr >= 60:
            return console_color_code["unicum"]
        if wr >= 50:
            return console_color_code["normal"]
        return console_color_code["bad"]


class ConsoleGui(BaseGui, ColorStatsMixin):

    def render(self, allied_list: list[PlayerStats], enemy_list: list[PlayerStats]):
        self.__print_allied_output(allied_list)
        print("")
        self.__print_enemy_output(enemy_list)

    @staticmethod
    def __print_tab(ign: str):
        ign_length = len(ign)
        if ign_length >= 24:
            return "\t"
        if ign_length >= 16:
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
                  self.color_wr(stats.wr) + f"{stats.wr}%" + "\t\t\t" + self.color_avg_damage(
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
                  self.color_wr(stats.wr) + f"{stats.wr}%" + "\t\t\t" + self.color_avg_damage(
                stats.avg_dmg) + f"{stats.avg_dmg}")


class TableGui(BaseGui, ColorStatsMixin):
    @staticmethod
    def __render_avg_dmg(value):
        if value is None:
            return Fore.WHITE + "-"
        console_color = TableGui.color_avg_damage(value)
        return console_color + str(value) + Fore.WHITE

    @staticmethod
    def __render_wr(value):
        if value is None:
            return Fore.WHITE + "-"

        console_color = TableGui.color_wr(value)
        return console_color + str(value) + Fore.WHITE

    def render(self, allied_list: list[PlayerStats], enemy_list: list[PlayerStats]):
        os.system('cls' if os.name == 'nt' else 'clear')
        table = prettytable.PrettyTable(['Allied IGN', 'a_WR', 'a_Avg Dmg',
                                         'Enemy IGN', "e_WR", "e_Avg Dmg"])
        for tuple_player in zip(allied_list, enemy_list):
            [allied, enemy] = tuple_player
            table.add_row([allied.ign, self.__render_wr(allied.wr), self.__render_avg_dmg(allied.avg_dmg),
                          enemy.ign, self.__render_wr(enemy.wr), self.__render_avg_dmg(enemy.avg_dmg)])
        print(table)
        return


def __main__():
    gui = TableGui()
    allied_list = [PlayerStats(ign=f"allied_{i}", wr=round(60 + i * 0.1, 2), avg_dmg=800 + int(f"{i}00")) for i in
                   range(7)]
    allied_list[1] = PlayerStats(ign="allied_failed")
    enemy_list = [PlayerStats(ign=f"enemy_{i}", wr=round(
        50 + i, 2), avg_dmg=800 + int(f"{i}00")) for i in range(7)]
    gui.render(allied_list, enemy_list)


if __name__ == "__main__":
    __main__()
