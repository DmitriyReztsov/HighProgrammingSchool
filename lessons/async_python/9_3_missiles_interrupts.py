import asyncio
import random

error = None
count = 0
sek = 0

interrupt_flag = asyncio.Event()


async def monitor_rocket_launches(interrupt_flag: asyncio.Event):
    global count
    global error
    global sek

    try:
        # Допишите сюда цикл
        while not error:
            error = random.choices([True, False], weights=[0.25, 0.75], k=1)[0]
            if not error:
                print(f"Мониторинг ракетных запусков... (Запуск номер {count} прошёл успешно)")
                count += 1
                await asyncio.sleep(1)
                sek += 1
            else:
                interrupt_flag.set()
    finally:
        # Поместите сообщение о завершении мониторинга
        print("Завершение мониторинга ракетных запусков")


async def hui():
    while count < 50 and not error:
        await asyncio.sleep(5)
        print(f"Время ожидания составило {sek} секунд. За это время ошибки не произошло")
    if error:
        print(f"Ошибка при запуске произошла на {sek} секунде =(")
        print("Отмена мониторинга ракетных запусков...")


async def main():
    global error
    global count
    global sek

    # Создайте Task задачу
    task = asyncio.create_task(monitor_rocket_launches(interrupt_flag))
    # Допишите сюда цикл

    # Запустите созданную корутину в пункте 2 через await
    await asyncio.gather(task, hui())


if __name__ == "__main__":
    asyncio.run(main())
