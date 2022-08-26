import asyncio
import logging
import os
from abc import abstractmethod
from typing import Literal

import requests
from cachetools import cached, TTLCache
from dotenv import load_dotenv

from player_stats import PlayerStats


class BasePlayerStatsService:
    @abstractmethod
    def get_players_stats(self, players: list[str], region: Literal["asia", "na", "eu", "ru"] = "asia",
                          timeout: int = 5):
        pass

    @abstractmethod
    def get_individual_stats(self, ign: str, region: Literal["asia", "na", "eu", "ru"],
                             timeout: int = 5) -> PlayerStats:
        pass


class WgApiService(BasePlayerStatsService):
    application_id: str | None

    def __init__(self):
        load_dotenv()
        self.application_id = os.environ.get("WG_APPS_ID")

    def get_players_stats(self, players: list[str], region: Literal["asia", "na", "eu", "ru"] = "asia",
                          timeout: int = 5):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        urls = [asyncio.ensure_future(self.get_individual_stats(
            ign=player, region=region, timeout=timeout)) for player in players]
        return loop.run_until_complete(asyncio.gather(*urls))

    async def get_individual_stats(self, ign: str, region: Literal["asia", "na", "eu", "ru"],
                                   timeout: int = 5) -> PlayerStats | None:
        account_id = self.__get_account_id(ign)
        if account_id is None:
            return PlayerStats(ign=ign)
        account_stats = self.__fetch_to_wg_api(account_id)
        if account_stats is None:
            return PlayerStats(ign=ign)
        return account_stats

    @cached(cache=TTLCache(maxsize=1024, ttl=604800))
    def __fetch_to_wg_api(self, account_id: str):
        if self.application_id is None:
            return None
        res = requests.get("https://api.wotblitz.asia/wotb/account/info/", params={
            "application_id": self.application_id,
            "account_id": account_id,
            "fields": "statistics.all.dropped_capture_points,statistics.all.spotted,account_id,nickname,"
                      "statistics.all.battles,statistics.all.damage_dealt,statistics.all.wins,statistics.all.frags "
        })
        try:
            return self.__convert_to_player_statistic(res.json()["data"][f"{account_id}"])
        except Exception as e:
            logging.error("__fetch_to_wg_api" + str(e))
            return None

    @cached(cache={})
    def __get_account_id(self, ign: str) -> str | None:
        if self.application_id is None:
            return None

        res = requests.get(
            f'https://api.wotblitz.asia/wotb/account/list/', params={
                "application_id": self.application_id,
                "search": ign,
                "type": "exact"
            })
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
        stats = PlayerStats(ign=dict_wg["nickname"], account_id=dict_wg["account_id"], avg_dmg=round(
            avg_dmg), wr=round(wr * 100, 2), region="asia")
        return stats


def __main():
    stats = WgApiService().get_players_stats(["Tankerch"])
    print(stats)


if __name__ == "__main__":
    __main()
