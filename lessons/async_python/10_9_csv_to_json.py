import asyncio
import csv
import json

import aiocsv
import aiofiles


class CustomDialect(csv.Dialect):
    delimiter = ";"  # Определяет символ-разделитель столбцов в csv файле как ";"
    quotechar = '"'  # Определяет символ кавычек, используемый для обрамления полей в csv файле, как двойные кавычки
    doublequote = True  # Если этот параметр True, две кавычки внутри поля трактуются как одна кавычка
    skipinitialspace = True  # Если параметр True, пробелы в начале каждого поля игнорируются
    lineterminator = "\n"  # Определяет символ окончания строки в csv файле как "\n"
    quoting = csv.QUOTE_MINIMAL


csv.register_dialect("customDialect", CustomDialect)  # Регистрирует диалект


async def main():
    file_path = "HighProgrammingSchool/lessons/async_python/10_9_files/adress_1000000.csv"
    json_file_path = "HighProgrammingSchool/lessons/async_python/10_9_files/adress_1000000.json"
    data_list = []

    async with aiofiles.open(file_path, mode="r", encoding="utf-8-sig", newline="") as file:
        async for row in aiocsv.AsyncDictReader(file, dialect="customDialect"):
            data_list.append(row)

    with open(json_file_path, "w") as file:
        json.dump(data_list, file, ensure_ascii=False, indent=4)


asyncio.run(main())
