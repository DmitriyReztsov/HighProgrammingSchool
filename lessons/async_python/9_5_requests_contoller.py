import asyncio
import random

users = [
    "sasha",
    "petya",
    "masha",
    "katya",
    "dima",
    "olya",
    "igor",
    "sveta",
    "nikita",
    "lena",
    "vova",
    "yana",
    "kolya",
    "anya",
    "roma",
    "nastya",
    "artem",
    "vera",
    "misha",
    "liza",
]

semaphore = asyncio.Semaphore(3)
requests_num = 0


async def request_processing(user: str):
    global requests_num

    async with semaphore:
        print(f"Пользователь {user} делает запрос")
        requests_num += 1
        await asyncio.sleep(random.randint(0, 5))
        print(f"Запрос от пользователя {user} завершен")
        print(f"Всего запросов: {requests_num}")


async def main():
    tasks = [asyncio.create_task(request_processing(user)) for user in users]
    await asyncio.gather(*tasks)


asyncio.run(main())
