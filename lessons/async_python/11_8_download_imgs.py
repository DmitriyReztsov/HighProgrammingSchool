import asyncio
import os

import aiofiles
import aiohttp
from bs4 import BeautifulSoup

semaphore = asyncio.Semaphore(15)


async def write_to_file(content, index):
    async with aiofiles.open(
        f"HighProgrammingSchool/lessons/async_python/11_8_files/downloads/image_{index}.jpg", "wb"
    ) as file:
        await file.write(content)


async def download_file(session, url, index):
    async with semaphore:
        async with session.get(url) as response:
            await write_to_file(await response.read(), index)
    return response.status


async def main():
    async with aiohttp.ClientSession() as session:
        main_url = "https://asyncio.ru/zadachi/4/"
        async with session.get(main_url + "index.html") as response:
            html_content = await response.text()
            soup = BeautifulSoup(html_content, "html.parser")
            main_tag = soup.find("main")
            img_tags = main_tag.find_all("img")

        tasks = [
            asyncio.create_task(download_file(session, main_url + img["src"], i)) for i, img in enumerate(img_tags)
        ]
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())

    folder_path = r"HighProgrammingSchool/lessons/async_python/11_8_files/downloads"
    total_size = 0
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            total_size += os.path.getsize(file_path)
    print(total_size)
