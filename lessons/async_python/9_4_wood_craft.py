import asyncio


wood_resources_dict = {
    "Деревянный меч": 6,
    "Деревянный щит": 12,
    "Деревянный стул": 24,
}
storage = 0
condition = asyncio.Condition()
event = asyncio.Event()


async def gather_wood():
    global storage

    # Код по добыче 2ед древесины в секунду
    while True:
        await asyncio.sleep(1)
        if event.is_set():
            break
        storage += 2
        print(f"Добыто 2 ед. дерева. На складе {storage} ед.")
        async with condition:
            condition.notify()


async def craft_item():
    global storage

    event.clear()

    # Код изготовлению деревянных предметов
    for item, need in wood_resources_dict.items():
        async with condition:
            while need > storage:
                await condition.wait()

        print(f"Изготовлен {item}.")
        storage -= need
    event.set()


async def main():
    await asyncio.gather(craft_item(), gather_wood())


asyncio.run(main())
