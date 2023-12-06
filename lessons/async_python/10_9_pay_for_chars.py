import asyncio
import json
import sys
from collections import defaultdict
from pprint import pprint

import aiofiles
import aiofiles.os as aos

path = "HighProgrammingSchool/lessons/async_python/10_9_files/chat_log"
char_price = 3  # in cents
users_costs = defaultdict(int)
semaphor = asyncio.Semaphore(200)
total_files = 0
counter_files = 0


async def proceed_file(file_path: str) -> None:
    global users_costs
    global counter_files

    async with semaphor:
        async with aiofiles.open(file_path, "r") as file:
            while line := await file.readline():
                user_message = line.split("- ")[1]
                user = user_message.split(": ")[0].strip()
                message = user_message.split(": ")[1].strip()
                users_costs[user] += len(message) * char_price
    counter_files += 1
    print(f"{file_path} proceeded. {counter_files} from {total_files}")


def format_user_cost(user_cost: dict) -> dict:
    return_dict = defaultdict(str)
    for key, value in user_cost.items():
        return_dict[key] = f"{value / 100}р"
    return return_dict


async def main():
    global total_files

    files = await aos.listdir(path)
    total_files = len(files)
    tasks = [asyncio.create_task(proceed_file(f"{path}/{file_name}")) for file_name in files]
    await asyncio.gather(*tasks)
    return format_user_cost(users_costs)


if __name__ == "__main__":
    return_dict = asyncio.run(main())
    pprint(json.dump(return_dict, sys.stdout, ensure_ascii=False, indent=4))
