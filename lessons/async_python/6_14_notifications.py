import asyncio


async def publish_post(text: str):
    # принимает на вход текст поста и имитирует публикацию нового поста на блоге Васи
    await asyncio.sleep(1)
    print(f"Пост опубликован: {text}")
    return f"Пост опубликован: {text}"


async def notify(sub: str):
    await asyncio.sleep(1)
    print(f"Уведомление отправлено {sub}")


async def notify_subscribers(subscribers: list):
    # принимает на вход список подписчиков и имитирует отправку уведомления каждому подписчику
    tasks = [asyncio.create_task(notify(sub)) for sub in subscribers]
    await asyncio.gather(*tasks)


async def main():
    post_text = "Hello world!"
    subscribers = ["Alice", "Bob", "Charlie", "Dave", "Emma", "Frank", "Grace", "Henry", "Isabella", "Jack"]
    asyncio.create_task(publish_post(post_text))
    await notify_subscribers(subscribers)


asyncio.run(main())
