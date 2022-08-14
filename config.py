from dataclasses import dataclass


@dataclass(frozen=True)
class AppConfig:
    box_width = 300
    first_point = (645, 520)
    second_point = (1910, 870)
