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
    def render(self, allied: list[PlayerStats], enemy: list[PlayerStats]):
        pass


class ConsoleGui(BaseGui):

    def render(self, allied: list[PlayerStats], enemy: list[PlayerStats]):
        self.__print_allied_output(allied)
        print("")
        self.__print_enemy_output(enemy)

    @staticmethod
    def __categorized_avg_damage(avg_damage: int) -> Fore:
        if avg_damage > 1400:
            return console_color_code["unicum"]
        if avg_damage > 1000:
            return console_color_code["normal"]
        return console_color_code["bad"]

    @staticmethod
    def __color_for_wr(wr: float) -> Fore:
        if wr > 60:
            return console_color_code["unicum"]
        if wr > 50:
            return console_color_code["normal"]
        return console_color_code["bad"]

    @staticmethod
    def __color_for_wn8(wn8: float) -> Fore:
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
                  self.__color_for_wr(stats.wr) + f"{stats.wr}%" + "\t\t\t" + self.__categorized_avg_damage(
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
                  self.__color_for_wr(stats.wr) + f"{stats.wr}%" + "\t\t\t" + self.__categorized_avg_damage(
                stats.avg_dmg) + f"{stats.avg_dmg}")
