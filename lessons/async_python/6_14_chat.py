import asyncio
import random


# Список сообщений чата
messages = []
number_messages = 0
Stepik = 0  # Не удалять ! Необходимо для проверки на stepik


# Функция, которая будет обрабатывать новые сообщения
async def handle_message(message):
    global number_messages
    number_messages += 1
    messages.append(message)


# Функция, которая будет симулировать отправку сообщений
async def send_message(message):
    await asyncio.sleep(2)  # имитация задержки отправки сообщения
    if not message:
        message = " Собеседник решил промолчать..."
    else:
        await handle_message(message)
    print(f"Собеседник 1:  {message}")


# Описание работы Собеседник 1
async def messages_input():
    global Stepik  # Не удалять ! Необходимо для проверки на stepik
    message = None
    messages_bot = [
        "Привет !",
        "Как дела ?",
        "Был сегодня на улице ?",
        "Чего-то не устроило ?)",
        "Давай ещё пообщаемся",
        "Хорошая сегодня погода",
    ]
    # await asyncio.sleep(1) # Засыпает на 1 секунду имитируя набор текста пользователем
    if random.randint(0, 3) or Stepik > 2:
        message = f"{random.choice(messages_bot)}"
    else:
        Stepik += 1  # Не удалять ! Необходимо для проверки на stepik
    await send_message(message)


# Функция, которая будет делать long polling запросы для получения новых сообщений
async def poll_messages():
    messages_bot = [
        "Хорошее сообщение, мне нравится :)",
        "Плохое сообщение попробуй ещё :(",
        "Поясни",
        "Согласен с тобой, если это был не вопрос конечно :)",
        "Чего ?",
        "Напиши что-нибудь другое",
    ]

    # Допишите эту функцию
    control_messages = number_messages
    while number_messages < 5:
        await messages_input()
        if control_messages != number_messages:
            print("Получено сообщение:  ", messages.pop())
            control_messages = number_messages

        message = None
        if random.randint(0, 3):
            message = f"{random.choice(messages_bot)}"
        await asyncio.sleep(2)  # имитация задержки отправки сообщения
        if not message:
            message = "Собеседник решил промолчать..."
        print(f"Собеседник 2:   {message}")


# Функция, которая стартует оба процесса в асинхронной среде
async def main():
    print("Привет!")
    print("Запущен чат двух ботов !")
    print("Давай посмотрим как они будут общаться =)")
    await asyncio.create_task(poll_messages())


# Запуск программы
if __name__ == "__main__":
    asyncio.run(main())
