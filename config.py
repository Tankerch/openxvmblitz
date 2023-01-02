from dataclasses import dataclass
from player_stats import WgServer


@dataclass(frozen=True)
class AppConfig:
    server: WgServer = "asia"
    box_width = 300
    start_player_y_point = 520
    players_section_w = 1270
    players_section_h = 350
