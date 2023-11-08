import asyncio


max_counts = {
    "Counter 1": 13,
    "Counter 2": 7,
}


counters = {
    "Counter 1": 0,
    "Counter 2": 0,
}


async def counter(counter_name: str, delay: int) -> None:
    # while counters[counter_name] < max_counts[counter_name]:
    #     counters[counter_name] += 1
    #     await asyncio.sleep(delay)
    #     print(f"{counter_name}: {counters[counter_name]}")

    count = 0
    while count < max_counts[counter_name]:
        count += 1
        await asyncio.sleep(delay)
        print(f"{counter_name}: {count}")


async def main():
    task_1 = asyncio.create_task(counter("Counter 1", 1))
    task_2 = asyncio.create_task(counter("Counter 2", 1))

    # await task_1
    # await task_2

    await asyncio.gather(task_1, task_2)


asyncio.run(main=main())
