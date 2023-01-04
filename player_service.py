import logging
import os
import dotenv
import cachetools
from abc import abstractmethod, abstractproperty
from config import AppConfig
from player_stats import PlayerStats, WgServer
import requests


class BaseStatsService:
    @abstractproperty
    def server(self) -> WgServer:
        pass

    @abstractmethod
    async def get_stats(self, ign: str, timeout: int = 5) -> PlayerStats:
        pass


class WgApiService(BaseStatsService):
    application_id: str

    server = AppConfig.server

    def __init__(self):
        dotenv.load_dotenv()
        apps_id = os.environ.get("WG_APPS_ID")
        if apps_id is None:
            raise TypeError("WG_APPS_ID is None")
        self.application_id = apps_id

    async def get_stats(self, ign: str) -> PlayerStats | None:
        account_id = self.__get_account_id(ign)
        if account_id is None:
            return PlayerStats(ign=ign)
        account_stats = await self.__fetch_to_wg_api(account_id)
        if account_stats is None:
            return PlayerStats(ign=ign)
        return account_stats

    @cachetools.cached(cache=cachetools.TTLCache(maxsize=1024, ttl=604800))
    async def __fetch_to_wg_api(self, account_id: str):
        try:
            res = requests.get(f"https://api.wotblitz.{self.server}/wotb/account/info/",
                               params={"application_id": self.application_id, "account_id": account_id,
                                       "fields": "statistics.all.dropped_capture_points,statistics.all.spotted,account_id,nickname,"
                                       "statistics.all.battles,statistics.all.damage_dealt,statistics.all.wins,statistics.all.frags "})
            return self.__convert_to_player_statistic(res.json()["data"][f"{account_id}"])
        except Exception as e:
            logging.error("__fetch_to_wg_api" + str(e))
            return None

    @cachetools.cached(cache={})
    def __get_account_id(self, ign: str) -> str | None:
        res = requests.get(f'https://api.wotblitz.{self.server}/wotb/account/list/',
                           params={"application_id": self.application_id, "search": ign, "type": "exact"})
        data = res.json()
        try:
            if len(data["data"]) == 0:
                logging.error(f"IGN {ign} not found")
                return None
            return data["data"][0]["account_id"]
        except Exception as e:
            logging.error(f"Failed at {ign}\nReason: {e}")
            return None

    @staticmethod
    def __convert_to_player_statistic(dict_wg: dict) -> PlayerStats:
        stats_all = dict_wg["statistics"]["all"]
        battle_count = stats_all["battles"]
        avg_dmg = stats_all["damage_dealt"] / battle_count
        wr = stats_all["wins"] / battle_count
        stats = PlayerStats(ign=dict_wg["nickname"], account_id=dict_wg["account_id"], avg_dmg=round(avg_dmg),
                            wr=round(wr * 100, 2), region="asia")
        return stats


def __main__():
    stats = WgApiService().get_players_stats(["Tankerch"])
    print(stats)


if __name__ == "__main__":
    __main__()
