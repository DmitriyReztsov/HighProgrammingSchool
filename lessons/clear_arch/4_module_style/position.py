from math import cos, radians, sin


class Position:
    def __init__(self, x: float = 0, y: float = 0) -> None:
        self.x = x
        self.y = y

    def calculate_new_position(self, azimuth: float, distance: float) -> None:
        angle = radians(azimuth)
        self.x += distance * sin(angle)
        self.y += distance * cos(angle)
