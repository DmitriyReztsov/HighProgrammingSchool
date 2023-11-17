import asyncio
from functools import partial


codes = [
    "56FF4D",
    "A3D2F7",
    "B1C94A",
    "F56A1D",
    "D4E6F1",
    "A1B2C3",
    "D4E5F6",
    "A7B8C9",
    "D0E1F2",
    "A3B4C5",
    "D6E7F8",
    "A9B0C1",
    "D2E3F4",
    "A5B6C7",
    "D8E9F2",
]


messages = [
    "Привет, мир!",
    "Как дела?",
    "Что нового?",
    "Добрый день!",
    "Пока!",
    "Спокойной ночи!",
    "Удачного дня!",
    "Всего хорошего!",
    "До встречи!",
    "Счастливого пути!",
    "Успехов в работе!",
    "Приятного аппетита!",
    "Хорошего настроения!",
    "Спасибо за помощь!",
    "Всего наилучшего!",
]


async def print_message(txt: str):
    return txt


def print_code(task: asyncio.Task, txt: str):
    validate_code_map = {
        True: f"Сообщение: {task.result()}",
        False: "Сообщение: Неверный код, сообщение скрыто",
    }
    print(validate_code_map[int(txt, base=16) % 2 == 1])
    print(f"Код: {txt}")


async def main():
    tasks = []
    for text, code in zip(messages, codes):
        task = asyncio.create_task(print_message(text))
        task.add_done_callback(partial(print_code, txt=code))
        tasks.append(task)
    await asyncio.gather(*tasks)
    # _, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
    # while pending:
    #     asyncio.sleep(1)
    #     _, pending = await asyncio.wait(pending, return_when=asyncio.FIRST_COMPLETED)


asyncio.run(main())
