import asyncio


# async def coro_i(i: int) -> None:
#     another_coro_i = {1:2, 2:1}[i]
#     print(f"coro_{i} says, hello coro_{another_coro_i}!")


# async def entry_point():
#     await asyncio.gather(*[asyncio.create_task(coro_i(i)) for i in range(1, 3)])


async def coro_1():
    print("coro_1 says, hello coro_2!")


async def coro_2():
    print("coro_2 says, hello coro_1!")


async def entry_point():
    await asyncio.gather(coro_1(), coro_2())


asyncio.run(main=entry_point())
