import asyncio

from _6_9_data import data


async def call_company(company_data: dict) -> None:
    await asyncio.sleep(company_data["call_time"])
    print(f"Company {company_data['Name']}: {company_data['Phone']} дозвон успешен")


async def task_with_timeout(task):
    try:
        await asyncio.wait_for(task, timeout=5)
    except asyncio.TimeoutError:
        task.cancel()


async def main():
    tasks = [
        asyncio.create_task(task_with_timeout(asyncio.create_task(call_company(company_data)))) for company_data in data
    ]

    await asyncio.wait(tasks, timeout=10)


asyncio.run(main())
