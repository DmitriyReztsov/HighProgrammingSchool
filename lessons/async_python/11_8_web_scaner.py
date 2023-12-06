import asyncio

import aiohttp

semaphore = asyncio.Semaphore(15)


async def get_response(session, url):
    async with semaphore:
        async with session.get(url) as response:
            print(f"Статус код: {response.status}")
    return response.status


async def main():
    async with aiohttp.ClientSession() as session:
        main_url = "https://asyncio.ru/zadachi/5/"
        tasks = [asyncio.create_task(get_response(session, f"{main_url}{i}.html")) for i in range(1, 1001)]
        result = await asyncio.gather(*tasks)
    print(">>> Magic sum <<<", sum(result))


if __name__ == "__main__":
    asyncio.run(main())
