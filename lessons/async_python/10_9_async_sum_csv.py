import aiocsv
import aiofiles
import asyncio
from aiofiles import os as aos


async def read_csv(file_path: str) -> int:
    return_array = []
    async with aiofiles.open(file_path, "r") as file:
        async for row in aiocsv.AsyncReader(file):
            return_array.extend(row)
    return int(row[0])


async def main():
    file_path = "HighProgrammingSchool/lessons/async_python/10_9_files/5000csv/5000csv"
    file_names = await aos.listdir(file_path)
    tasks = [asyncio.create_task(read_csv(f"{file_path}/{file_name}")) for file_name in file_names]
    results = await asyncio.gather(*tasks)
    print(sum(results))


asyncio.run(main())
