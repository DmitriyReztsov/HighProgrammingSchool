import asyncio

# Имена пользователей
users = ["Alice", "Bob", "Charlie", "Dave", "Eva", "Frank", "George", "Helen", "Ivan", "Julia"]
condition = asyncio.Condition()


async def database_connetion(user: str):
    async with condition:
        print(f"Пользователь {user} ожидает доступа к базе данных")
        await condition.wait()
        print(f"Пользователь {user} подключился к БД")
        await asyncio.sleep(1)
        print(f"Пользователь {user} отключается от БД")
        condition.notify()


async def db_controller():
    async with condition:
        condition.notify()


async def main():
    tasks = [asyncio.create_task(database_connetion(user)) for user in users]
    await asyncio.gather(db_controller(), *tasks)


asyncio.run(main())
