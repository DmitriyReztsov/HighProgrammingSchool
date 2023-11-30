import aiocsv
import csv
import aiofiles
import asyncio
import json
from aiofiles import os as aos
from collections import defaultdict


result_dict = defaultdict(int)
result_locker = asyncio.Lock()


class CustomDialect(csv.Dialect):
    delimiter = ";"  # Определяет символ-разделитель столбцов в csv файле как ";"
    quotechar = '"'  # Определяет символ кавычек, используемый для обрамления полей в csv файле, как двойные кавычки
    doublequote = True  # Если этот параметр True, две кавычки внутри поля трактуются как одна кавычка
    skipinitialspace = True  # Если параметр True, пробелы в начале каждого поля игнорируются
    lineterminator = "\n"  # Определяет символ окончания строки в csv файле как "\n"
    quoting = csv.QUOTE_MINIMAL


csv.register_dialect("customDialect", CustomDialect)  # Регистрирует диалект


async def proceed_csv(file_path: str):
    global result_dict

    async with aiofiles.open(file_path, mode="r", encoding="windows-1251", newline="") as file:
        async for row in aiocsv.AsyncDictReader(file, dialect="customDialect"):
            async with result_locker:
                if row["Состояние авто"] == "Б/У":
                    result_dict["Б/У"] += int(row["Стоимость авто"])
                elif row["Состояние авто"] == "Новый":
                    result_dict["Новый"] += int(row["Стоимость авто"])


async def process_directory(folder_path: str):
    tasks = []
    entries = await aos.scandir(folder_path)
    for entry in entries:
        full_path = f"{entry.path}"
        if await aos.path.isfile(full_path) and entry.name.endswith(".csv"):
            tasks.append(asyncio.create_task(proceed_csv(full_path)))
        elif await aos.path.isdir(full_path):
            tasks.append(asyncio.create_task(process_directory(full_path)))
    await asyncio.gather(*tasks)


async def main():
    global result_dict

    folders_path = "HighProgrammingSchool/lessons/async_python/10_9_files/auto/Задача 3"
    await process_directory(folders_path)

    json_file_path = "HighProgrammingSchool/lessons/async_python/10_9_files/auto.json"
    content = json.dumps(result_dict, ensure_ascii=False, indent=4)
    async with aiofiles.open(json_file_path, encoding="utf-8", mode="w") as file:
        await file.write(content)


asyncio.run(main())
