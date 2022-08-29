from dataclasses import dataclass


@dataclass(frozen=True)
class AppConfig:
    box_width = 300
    start_player_y_point = 500
    players_section_w = 1270
    players_section_h = 350
