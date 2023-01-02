import os
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


class ConsoleColorStatsMixin:
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


class TableGui(BaseGui, ConsoleColorStatsMixin):
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
            if allied.ign_is_empty():
                continue
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
