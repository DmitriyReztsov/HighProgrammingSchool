import asyncio

# Semaphore
sem = asyncio.Semaphore(2)
user_ids = [1, 2, 3, 4, 5]


async def fetch(user_id: int) -> dict:
    await asyncio.sleep(0.1)
    return {"id": user_id, "data": "user data"}


async def guarded_fetch(user_id: int):
    async with sem:
        return await fetch(user_id)


async def fetch_all(user_ids: list[int]) -> list[dict]:
    results = await asyncio.gather(
        *(map(guarded_fetch, user_ids)), return_exceptions=True
    )
    return results


async def main_semaphore():
    results = await fetch_all(user_ids)
    print(results)


# Lock
lock = asyncio.Lock()
user_ids = [1, 2, 3, 4, 5]
user_data = {}


async def add(user_id: int) -> None:
    await asyncio.sleep(0.1)
    user_data.update({user_id: "user data"})


async def guarded_add(user_id: int):
    async with lock:
        return await add(user_id)


async def add_all(user_ids: list[int]) -> list[dict]:
    results = await asyncio.gather(
        *(map(guarded_add, user_ids)), return_exceptions=True
    )
    return results


async def main_lock():
    results = await add_all(user_ids)
    print(results)


# Barrier
# в отличие от asyncio работают на threading, т.е. на отдельных потоках. Выносим в поток блокирующие операции, например - обработку файлов
import threading
import time

init_file_paths = ["file1", "file2", "file3"]
barrier = threading.Barrier(
    len(init_file_paths)
)  # каждый файл обрабатывается в своем потоке, для следующей стадии обработки - ждем обработки всех файлов
stage1_file_paths = {}
lock_stage1 = threading.Lock()  # Lock для потоков


def process_file(worker_id: int, file_path: str) -> None:
    print(f"Waiting for start, state: {stage1_file_paths}")
    barrier.wait()
    print(f"Worker {worker_id} proceeds file {file_path}")
    time.sleep(1)  # обработка большого файла
    with lock_stage1:
        stage1_file_paths[worker_id] = f"{file_path} proceeded"
        print(f"Worker {worker_id} finished stage 1, state: {stage1_file_paths}")


def process_all_files(worker_id: int) -> None:
    print(f"Waiting for start stage 2, state: {stage1_file_paths}")
    barrier.wait()
    print(f"Worker {worker_id} proceeds stage 2")
    time.sleep(0.5)
    with lock_stage1:
        stage1_file_paths[worker_id] += " after stage 2"
        print(f"Worker {worker_id} finished stage 2, state: {stage1_file_paths}")


def main_barrier():
    threads = []
    for worker_id, file_path in enumerate(init_file_paths):
        t = threading.Thread(
            target=lambda w, f: (process_file(w, f), process_all_files(w)),
            args=(worker_id, file_path),
        )
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    """
    Waiting for start, state: {}
    Waiting for start, state: {}
    Waiting for start, state: {}
    Worker 2 proceeds file file3
    Worker 1 proceeds file file2
    Worker 0 proceeds file file1
    Worker 2 finished stage 1, state: {2: 'file3 proceeded'}
    Waiting for start stage 2, state: {2: 'file3 proceeded'}
    Worker 1 finished stage 1, state: {2: 'file3 proceeded', 1: 'file2 proceeded'}
    Waiting for start stage 2, state: {2: 'file3 proceeded', 1: 'file2 proceeded'}
    Worker 0 finished stage 1, state: {2: 'file3 proceeded', 1: 'file2 proceeded', 0: 'file1 proceeded'}
    Waiting for start stage 2, state: {2: 'file3 proceeded', 1: 'file2 proceeded', 0: 'file1 proceeded'}
    Worker 0 proceeds stage 2
    Worker 2 proceeds stage 2
    Worker 1 proceeds stage 2
    Worker 0 finished stage 2, state: {2: 'file3 proceeded', 1: 'file2 proceeded', 0: 'file1 proceeded after stage 2'}
    Worker 2 finished stage 2, state: {2: 'file3 proceeded after stage 2', 1: 'file2 proceeded', 0: 'file1 proceeded after stage 2'}
    Worker 1 finished stage 2, state: {2: 'file3 proceeded after stage 2', 1: 'file2 proceeded after stage 2', 0: 'file1 proceeded after stage 2'}
    
    """


import time

# Atomic
# В Питоне нет отдельного класса для атомарных операций. Если смотреть на библиотеку multiprocessing, то можно там воспользоваться классом Value, в который вшит лок
from multiprocessing import Process, Value


def increment_atomic(counter):
    for _ in range(100000):
        with counter.get_lock():
            counter.value += 1


counter = Value("i", 0)  # "i" = integer type_code, начальное значение 0


def main_atomic():
    processes = []
    for _ in range(4):
        p = Process(target=increment_atomic, args=(counter,))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    print(f"Counter value: {counter.value}")  # 400000


# Event
import threading
import time

# События для каждого этапа
stage1_done = threading.Event()
stage2_done = threading.Event()


def stage1():
    print("Stage 1: data downloading...")
    time.sleep(2)
    print("Stage 1: completed")
    stage1_done.set()


def stage2():
    print("Stage 2: waiting for stage 1...")
    stage1_done.wait()
    print("Stage 2: data processing...")
    time.sleep(1)
    print("Satge 2: completed")
    stage2_done.set()


def stage3():
    print("Stage 3: waiting for stage 2...")
    stage2_done.wait()
    print("Stage 3: data saving...")
    time.sleep(1)
    print("Stage 3: completed")


def main_event():
    threads = [
        threading.Thread(target=stage1),
        threading.Thread(target=stage2),
        threading.Thread(target=stage3),
    ]

    for t in threads:
        t.start()

    for t in threads:
        t.join()


if __name__ == "__main__":
    main_event()
