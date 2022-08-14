from dataclasses import dataclass, field
from typing import Literal


@dataclass(frozen=True)
class PlayerStats:
    ign: str
    wr: float
    avg_dmg: int
    wn8: int | None = field(default=None)
    account_id: str | None = field(default=None)
    region: Literal["asia", "na", "eu", "ru"] = field(default="asia")
