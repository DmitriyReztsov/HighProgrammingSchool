import asyncio

INIT_TIME = 2


async def activate_portal(time_needed: int) -> int:
    print(f"Активация портала в процессе, требуется времени: {time_needed} единиц")
    await asyncio.sleep(time_needed)
    energy_poluted = time_needed * 2
    # print(f"Результат активации портала: {energy_poluted} единиц энергии")
    return energy_poluted


async def perform_teleportation(time_needed: int) -> int:
    print(f"Телепортация в процессе, требуется времени: {time_needed} единиц")
    await asyncio.sleep(time_needed)
    time_spent = time_needed + 2
    # print(f"Результат телепортации: {time_spent} единиц времени")
    return time_spent


async def recharge_portal(time_to_recharge: int) -> int:
    print(f"Подзарядка портала, требуется времени: {time_to_recharge} единиц")
    await asyncio.sleep(time_to_recharge)
    energy_to_recharge = time_to_recharge * 3
    # print(f"Результат подзарядки портала: {energy_to_recharge} единиц энергии")
    return energy_to_recharge


async def check_portal_stability(time_to_check: int) -> int:
    print(f"Проверка стабильности портала, требуется времени: {time_to_check} единиц")
    await asyncio.sleep(time_to_check)
    stable_time = time_to_check * 4
    # print(f"Результат проверки стабильности: {stable_time} единиц времени")
    return stable_time


async def restore_portal(time_to_restore: int) -> int:
    print(f"Восстановление портала, требуется времени: {time_to_restore} единиц")
    await asyncio.sleep(time_to_restore)
    energy_to_restore = time_to_restore * 5
    # print(f"Результат восстановления портала: {energy_to_restore} единиц энергии")
    return energy_to_restore


async def close_portal(time_to_close: int) -> int:
    print(f"Закрытие портала, требуется времени: {time_to_close} единиц")
    await asyncio.sleep(time_to_close)
    closure_time = time_to_close - 1
    # print(f"Результат закрытия портала: {closure_time} единиц времени")
    return closure_time


async def portal_operator() -> None:
    activate_portal_future = asyncio.ensure_future(activate_portal(INIT_TIME))
    energy_poluted = await activate_portal_future

    teleport_time = energy_poluted if energy_poluted <= 4 else 1
    perform_teleportation_future = asyncio.ensure_future(perform_teleportation(teleport_time))
    recharge_portal_future = asyncio.ensure_future(recharge_portal(teleport_time))
    portal_stability_future = asyncio.ensure_future(check_portal_stability(teleport_time))
    restore_future = asyncio.ensure_future(restore_portal(teleport_time))
    processes_results = await asyncio.gather(
        perform_teleportation_future, recharge_portal_future, portal_stability_future, restore_future
    )

    closure_future = asyncio.ensure_future(close_portal(teleport_time))
    closure_time = await closure_future

    teleport_time_resuts = [energy_poluted] + processes_results + [closure_time]
    report_masks = [
        "Результат активации портала: {} единиц энергии",
        "Результат телепортации: {} единиц времени",
        "Результат подзарядки портала: {} единиц энергии",
        "Результат проверки стабильности: {} единиц времени",
        "Результат восстановления портала: {} единиц энергии",
        "Результат закрытия портала: {} единиц времени",
    ]
    for time, report in zip(teleport_time_resuts, report_masks):
        print(report.format(time))


asyncio.run(portal_operator())
