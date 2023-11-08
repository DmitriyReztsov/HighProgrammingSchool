import asyncio


async def print_with_delay(i: int) -> None:
    await asyncio.sleep(1)
    print(f"Coroutine {i} is done")


async def entry_point():
    tasks = []
    for i in range(10):
        tasks.append(asyncio.create_task(print_with_delay(i)))
    await asyncio.gather(*tasks)


asyncio.run(entry_point())
