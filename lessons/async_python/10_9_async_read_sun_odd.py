import aiofiles
import aiofiles.os as aos
import asyncio


async def process_file(file_path: str) -> int:
    async with aiofiles.open(file_path, "r") as file:
        num = await file.read()
    return int(num) if int(num) % 2 == 0 else 0


async def main():
    path = "HighProgrammingSchool/lessons/async_python/10_9_files/files/files"
    files = await aos.listdir(path)
    tasks = [asyncio.create_task(process_file(f"{path}/{file_name}")) for file_name in files]
    results = await asyncio.gather(*tasks)
    return sum(results)


if __name__ == "__main__":
    c_sum = asyncio.run(main())
    print(c_sum)
