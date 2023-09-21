import os
from typing import List


def find_all_files(dir_path: str) -> List:
    files_list = []
    obj_in_dir = list(entry for entry in os.scandir(dir_path))
    for obj in obj_in_dir:
        if obj.is_file():
            files_list.append(obj.path)
        elif obj.is_dir():
            files_list.extend(find_all_files(obj.path))
    return files_list
