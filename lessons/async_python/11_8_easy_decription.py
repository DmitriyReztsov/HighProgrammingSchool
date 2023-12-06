import asyncio

import aiohttp
from bs4 import BeautifulSoup


async def main():
    async with aiohttp.ClientSession() as session:
        main_url = "https://asyncio.ru/zadachi/1/index.html"
        async with session.get(main_url) as response:
            html_doc = await response.text()

    soup = BeautifulSoup(html_doc, "html.parser")
    p_text = soup.find("p").text.strip()
    code_dict = {
        0: "F",
        1: "B",
        2: "D",
        3: "J",
        4: "E",
        5: "C",
        6: "H",
        7: "G",
        8: "A",
        9: "I",
    }
    char_seq = ""
    for dig in p_text:
        print(">>> CODE <<<", code_dict[int(dig)])
        char_seq = f"{char_seq}{code_dict[int(dig)]}"
    print(">>> Magic sum <<<", char_seq)


if __name__ == "__main__":
    asyncio.run(main())
