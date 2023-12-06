import asyncio
import itertools
import random

shapes = ["circle", "star", "square", "diamond", "heart"]
colors = ["red", "blue", "green", "yellow", "purple"]
actions = ["change_color", "explode", "disappear"]


async def launch_firework(shape: str, color: str, action: str):
    print(f"Запущен {color} {shape} салют, в форме {action}!!!")
    await asyncio.sleep(random.randint(1, 5))
    print(f"Салют {color} {shape} завершил выступление {action}")


async def main():
    tasks = [
        asyncio.create_task(launch_firework(*combination))
        for combination in list(itertools.product(shapes, colors, actions))
    ]
    await asyncio.gather(*tasks)


asyncio.run(main())
