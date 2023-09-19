def calculate_power(base: int, power: int) -> int:
    if power == 0:
        return 1
    return base * calculate_power(base, power-1)
