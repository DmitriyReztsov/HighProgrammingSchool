import asyncio


stone_resources_dict = {
    "Каменная плитка": 10,
    "Каменная ваза": 40,
    "Каменный столб": 50,
}

metal_resources_dict = {
    "Металлическая цепь": 6,
    "Металлическая рамка": 24,
    "Металлическая ручка": 54,
}

cloth_resources_dict = {
    "Тканевая занавеска": 8,
    "Тканевый чехол": 24,
    "Тканевое покрывало": 48,
}

condition = asyncio.Condition()
event_stone = asyncio.Event()
event_metal = asyncio.Event()
event_cloth = asyncio.Event()

storage = {
    "stone": 0,
    "metal": 0,
    "cloth": 0,
}


async def gather_stone():
    global storage

    # Добываем камень, 10ед каждую сек.
    while True:
        await asyncio.sleep(1)
        if event_stone.is_set():
            break
        storage["stone"] += 10
        print(f"Добыто 10 ед. камня. На складе {storage['stone']} ед.")
        async with condition:
            condition.notify()


async def gather_metal():
    global storage

    # Добываем металл, 6ед каждую сек.
    while True:
        await asyncio.sleep(1)
        if event_metal.is_set():
            break
        storage["metal"] += 6
        print(f"Добыто 6 ед. металла. На складе {storage['metal']} ед.")
        async with condition:
            condition.notify()


async def gather_cloth():
    global storage

    # Добываем ткань, 8ед каждую сек.
    while True:
        await asyncio.sleep(1)
        if event_cloth.is_set():
            break
        storage["cloth"] += 8
        print(f"Добыто 8 ед. ткани. На складе {storage['cloth']} ед.")
        async with condition:
            condition.notify()


async def craft_stone_items():
    global storage

    event_stone.clear()

    # Мастерская по крафту из камня
    for item, need in stone_resources_dict.items():
        async with condition:
            # while need > storage["metall"]:
            await condition.wait_for(lambda: need <= storage["stone"])

        print(f"Изготовлен {item} из камня.")
        storage["stone"] -= need
    event_stone.set()


async def craft_metal_items():
    global storage

    event_metal.clear()

    # Мастерская по крафту из мателла
    for item, need in metal_resources_dict.items():
        async with condition:
            # while need > storage:
            await condition.wait_for(lambda: need <= storage["metal"])

        print(f"Изготовлен {item} из металла.")
        storage["metal"] -= need
    event_metal.set()


async def craft_cloth_items():
    global storage

    event_cloth.clear()
    # Мастерская по крафту из ткани
    for item, need in cloth_resources_dict.items():
        async with condition:
            while need > storage["cloth"]:
                await condition.wait()

        print(f"Изготовлен {item} из ткани.")
        storage["cloth"] -= need
    event_cloth.set()


async def main():
    # Запускаем производства
    await asyncio.gather(
        gather_stone(), gather_metal(), gather_cloth(), craft_stone_items(), craft_metal_items(), craft_cloth_items()
    )


asyncio.run(main())
