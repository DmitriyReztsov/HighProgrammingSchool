import asyncio

import aiofiles
import aiohttp
from bs4 import BeautifulSoup

semaphore = asyncio.Semaphore(15)


async def proceed_page(content):
    soup = BeautifulSoup(content, "html.parser")
    return soup.find("p", id="number").text


async def get_response(line):
    url = f"https://asyncio.ru/zadachi/2/html/{line}.html"
    async with semaphore:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                html_doc = await response.text()
    return await proceed_page(html_doc)


async def main():
    all_figures = []
    async with aiofiles.open("HighProgrammingSchool/lessons/async_python/11_8_files/problem_pages.txt", "r") as file:
        async for line in file:
            figure = await get_response(line)
            all_figures.append(figure)
    return all_figures


if __name__ == "__main__":
    result = asyncio.run(main())
    print(">>> SUM <<<", sum(map(int, result)))
