import asyncio

import aiohttp
from bs4 import BeautifulSoup

semaphore = asyncio.Semaphore(100)
result_list = []


def add_to_list(number_tag):
    global result_list

    print(">>> TAG <<<", number_tag)
    result_list.append(number_tag)


async def process_url(main_url: str, sub_url: str):
    full_url = main_url + sub_url
    print(">>> INCOMMING URL <<<", full_url)
    # tasks = []
    async with semaphore:
        async with aiohttp.ClientSession() as session:
            async with session.get(full_url) as response:
                html_doc = await response.text()
                soup = BeautifulSoup(html_doc, "html.parser")
                number_tag = soup.find("p", {"id": "number"})
                links = soup.find_all("a", {"class": "link"})
    if number_tag:
        return add_to_list(number_tag.text)
    tasks = [
        asyncio.create_task(process_url(main_url + link["href"].split("/")[0] + "/", link["href"].split("/")[1]))
        for link in links
    ]
    return await asyncio.gather(*tasks)


async def main():
    main_url = "https://asyncio.ru/zadachi/3/"
    await process_url(main_url, "index.html")


if __name__ == "__main__":
    asyncio.run(main())
    print(">>> SUM <<<", sum(map(int, result_list)))
