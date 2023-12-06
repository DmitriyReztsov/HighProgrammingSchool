import asyncio
import csv
import json

import aiocsv
import aiofiles
from aiofiles import os as aos

result_list_json = []


class CustomDialect(csv.Dialect):
    delimiter = ","  # Определяет символ-разделитель столбцов в csv файле как ";"
    quotechar = '"'  # Определяет символ кавычек, используемый для обрамления полей в csv файле, как двойные кавычки
    doublequote = True  # Если этот параметр True, две кавычки внутри поля трактуются как одна кавычка
    skipinitialspace = True  # Если параметр True, пробелы в начале каждого поля игнорируются
    lineterminator = "\n"  # Определяет символ окончания строки в csv файле как "\n"
    quoting = csv.QUOTE_MINIMAL


csv.register_dialect("customDialect", CustomDialect)  # Регистрирует диалект


async def proceed_csv(file_path: str):
    global result_list_json

    async with aiofiles.open(file_path, mode="r", encoding="utf-8-sig", newline="") as file:
        async for row in aiocsv.AsyncDictReader(file, dialect="customDialect"):
            if not row.get("Балл ЕГЭ") or (row.get("Балл ЕГЭ") and int(row["Балл ЕГЭ"]) < 100):
                continue
            result_list_json.append(row)


async def main():
    global result_list_json

    folders_path = "HighProgrammingSchool/lessons/async_python/10_9_files/region_student/Задача Студенты"
    all_files_paths = []

    scandir_iter = await aos.scandir(folders_path)
    for folder in scandir_iter:
        files = await aos.listdir(folder.path)
        files_paths = [f"{folder.path}/{file_name}" for file_name in files]
        all_files_paths.extend(files_paths)
    tasks = [asyncio.create_task(proceed_csv(f"{file_name}")) for file_name in all_files_paths]
    await asyncio.gather(*tasks)

    json_file_path = "HighProgrammingSchool/lessons/async_python/10_9_files/region_student.json"
    result_list_json = sorted(result_list_json, key=lambda x: x["Телефон для связи"])
    content = json.dumps(result_list_json, ensure_ascii=False, indent=4)
    async with aiofiles.open(json_file_path, encoding="utf-8", mode="w") as file:
        await file.write(content)


asyncio.run(main())
