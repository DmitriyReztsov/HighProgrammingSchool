import asyncio


max_counts = {"Counter 1": 10, "Counter 2": 5, "Counter 3": 15}


delays = {
    "Counter 1": 1,
    "Counter 2": 2,
    "Counter 3": 0.5,
}


async def counter(counter_name: str, delay: int) -> None:
    count = 0
    while count < max_counts[counter_name]:
        count += 1
        await asyncio.sleep(delay)
        print(f"{counter_name}: {count}")


async def main():
    await asyncio.gather(
        *[
            asyncio.create_task(counter(counter_name, counter_delay))
            for counter_name, counter_delay in delays.items()
        ]
    )


asyncio.run(main=main())
