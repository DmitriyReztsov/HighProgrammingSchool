import asyncio
import random


robot_names = ["Электра", "Механикс", "Оптимус", "Симулакр", "Футуриус"]

visit_counter = 0


async def visit_A(robot_name: str, robot_id: int, lock: asyncio.Lock):
    global visit_counter

    await lock.acquire()
    try:
        print(f"Робот {robot_name}({robot_id}) передвигается к месту A")
        await asyncio.sleep(random.randint(0, 5))
        visit_counter += 1
        print(f"Робот {robot_name}({robot_id}) достиг места A. Место A посещено {visit_counter} раз")
    finally:
        lock.release()


async def main():
    lock = asyncio.Lock()
    tasks = [
        asyncio.create_task(visit_A(robot_name, robot_id, lock)) for robot_id, robot_name in enumerate(robot_names)
    ]
    await asyncio.gather(*tasks)


asyncio.run(main())
