import asyncio


INIT_TIME = 2


async def activate_portal(time_needed: int) -> int:
    print(f"Активация портала в процессе, требуется времени: {time_needed} единиц")
    await asyncio.sleep(time_needed)
    energy_poluted = time_needed * 2
    return energy_poluted


async def perform_teleportation(time_needed: int) -> int:
    print(f"Телепортация в процессе, требуется времени: {time_needed} единиц")
    await asyncio.sleep(time_needed)
    time_spent = time_needed + 2
    return time_spent


async def portal_operator() -> None:
    activate_portal_future = asyncio.ensure_future(activate_portal(INIT_TIME))
    energy_poluted = await activate_portal_future
    print(f"Результат активации портала: {energy_poluted} единиц энергии")

    teleport_time = energy_poluted if energy_poluted <= 4 else 1
    perform_teleportation_future = asyncio.ensure_future(perform_teleportation(teleport_time))
    teleport_time = await perform_teleportation_future
    print(f"Результат телепортации: {teleport_time} единиц времени")


asyncio.run(portal_operator())
