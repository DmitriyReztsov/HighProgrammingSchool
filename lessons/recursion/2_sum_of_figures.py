def calculate_sum_of_figures(figure):
    if figure // 10 != 0:
        return figure % 10 + calculate_sum_of_figures(figure // 10)
    return figure % 10
