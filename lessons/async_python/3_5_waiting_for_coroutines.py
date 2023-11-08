import asyncio


async def coroutine_1():
    print("Coroutine 1 is done")


async def coroutine_2():
    print("Coroutine 2 is done")


async def coroutine_3():
    print("Coroutine 3 is done")


async def entry_point():
    # asyncio.gather(coroutine_1(), coroutine_2(), coroutine_3())

    # asyncio.create_task(coroutine_1())
    # asyncio.create_task(coroutine_2())
    # asyncio.create_task(coroutine_3())

    asyncio.gather(
        *[
            asyncio.create_task(coro())
            for coro in [coroutine_1, coroutine_2, coroutine_3]
        ]
    )


asyncio.run(entry_point())
