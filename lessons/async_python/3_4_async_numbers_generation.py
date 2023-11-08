import asyncio


async def generate(i: int) -> None:
    print(f"Корутина generate с аргументом {i}")


async def entry_point():
    await asyncio.gather(*[generate(i) for i in range(10)])


asyncio.run(entry_point())
