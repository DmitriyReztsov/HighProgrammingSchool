import aiocsv
import csv
import aiofiles
import asyncio
import json
import aiofiles.os as aos
from datetime import datetime


class CustomDialect(csv.Dialect):
    delimiter = ";"  # Определяет символ-разделитель столбцов в csv файле как ";"
    quotechar = '"'  # Определяет символ кавычек, используемый для обрамления полей в csv файле, как двойные кавычки
    doublequote = True  # Если этот параметр True, две кавычки внутри поля трактуются как одна кавычка
    skipinitialspace = True  # Если параметр True, пробелы в начале каждого поля игнорируются
    lineterminator = "\n"  # Определяет символ окончания строки в csv файле как "\n"
    quoting = csv.QUOTE_MINIMAL


csv.register_dialect("customDialect", CustomDialect)  # Регистрирует диалект

result_jsons = []


async def analize_json(file_path: str):
    async with aiofiles.open(file_path, mode="r", encoding="utf-8-sig", newline="") as file:
        file_data = await file.read()
    json_data = json.loads(file_data)
    result_jsons.extend([log_entry for log_entry in json_data if log_entry["HTTP-статус"] == 200])


async def main():
    global result_jsons

    folder_path = "HighProgrammingSchool/lessons/async_python/10_9_files/logs"
    files = await aos.listdir(folder_path)

    tasks = [asyncio.create_task(analize_json(f"{folder_path}/{file}")) for file in files]
    await asyncio.gather(*tasks)

    csv_file_path = "HighProgrammingSchool/lessons/async_python/10_9_files/success_requests.csv"
    result_jsons.sort(key=lambda log_enrty: datetime.strptime(log_enrty["Время и дата"], "%Y-%m-%d %H:%M:%S"))
    for log_entry in result_jsons:
        dt_log_time = datetime.strptime(log_entry["Время и дата"], "%Y-%m-%d %H:%M:%S")
        log_entry["Время и дата"] = datetime.strftime(dt_log_time, "%d.%m.%Y %H:%M:%S")
    headers = result_jsons[0].keys()
    async with aiofiles.open(csv_file_path, mode="w", encoding="utf-8-sig") as file:
        writer = aiocsv.AsyncDictWriter(file, headers, dialect="customDialect")
        await writer.writeheader()
        await writer.writerows(result_jsons)


asyncio.run(main())
