from dataclasses import dataclass, field
from typing import Literal


@dataclass(frozen=True)
class PlayerStats:
    ign: str
    wr: float | None = field(default=None)
    avg_dmg: int | None = field(default=None)
    wn8: int | None = field(default=None)
    account_id: str | None = field(default=None)
    region: Literal["asia", "na", "eu", "ru"] = field(default="asia")

    def valid_to_print(self):
        return bool(self.wr) and bool(self.avg_dmg)
