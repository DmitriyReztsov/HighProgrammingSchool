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
    folders_path = "HighProgrammingSchool/lessons/async_python/10_9_files/5000folder/5000folder"
    # folders_names = await aos.listdir(file_path)
    all_files_paths = []

    scandir_iter = await aos.listdir(folders_path)
    for folder in scandir_iter:
        files = await aos.listdir(folders_path + "/" + folder)
        files_paths = [f"{folders_path}/{folder}/{file_name}" for file_name in files]
        all_files_paths.extend(files_paths)
    tasks = [asyncio.create_task(read_csv(f"{file_name}")) for file_name in all_files_paths]
    results = await asyncio.gather(*tasks)
    print(sum(results))


asyncio.run(main())
