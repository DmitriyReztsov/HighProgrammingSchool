# Код из задания, переведнный на Питон
import random
import threading
import time

SIZE = 1_000_000_000
THREADS = 8

data = [0] * SIZE
sum_ = 0
lock = threading.Lock()


def worker(start: int, end: int) -> None:
    global sum_

    local_sum = 0
    for j in range(start, end):
        local_sum += data[j]

    with lock:
        sum_ += local_sum


def main_init() -> None:
    global data

    for i in range(SIZE):
        data[i] = random.randint(0, 99)

    threads = []
    chunk_size = SIZE // THREADS

    for i in range(THREADS):
        start = i * chunk_size
        end = (i + 1) * chunk_size

        thread = threading.Thread(
            target=worker,
            args=(start, end),
        )
        threads.append(thread)
        thread.start()

    for thread in threads:
        try:
            thread.join()
        except KeyboardInterrupt:
            print("Interrupted")

    print(f"Sum of all elements: {sum_}")


# код в задании неоптимальный. Во-первых, для вычисления, т.е. CPU-bound задач в Питоне лучше подойдет не threading,
# а processing, т.е. вынос расчета в несколько процессов. Во-вторых, если мы делим список на чанки, которые потом суммируем
# и добавляем в глобальную переменную, то можно передать эти чанки в независимые процессы, а потом посчитать сумму результатов
# работы процессов. В таком случае не будет гонки данных, если мы обеспечим неизменяемость источника данных (общего ресурса).
# Дополнительно можно поменять +=1 на sum(), которая в Питоне реализована на Си и работает быстрее.
# Есть у именно этого подхода и недостаток - это затраты на сериализацию больших объемов данных и неоптимальность по
# памяти, поскольку в каждый процесс отправляется копия чанка. Можно было бы еще улучшить, использовав shared_memory
# для очень больших объемов данных.


from concurrent.futures import ProcessPoolExecutor


def partial_sum(chunk: list[int]) -> int:
    return sum(chunk)


def main_proc():
    # data creation
    data = [random.randint(0, 99) for _ in range(SIZE)]

    # нарезаем чанки
    chunk_size = SIZE // THREADS
    chunks = [data[i * chunk_size : (i + 1) * chunk_size] for i in range(THREADS - 1)]
    chunks.append(data[(THREADS - 1) * chunk_size :])

    # запускаем расчет в процессах
    with ProcessPoolExecutor(max_workers=THREADS) as executor:
        partials = executor.map(partial_sum, chunks)

    total = sum(partials)
    print(f"Sum of all elements from processes: {total}")


if __name__ == "__main__":
    # st = time.monotonic_ns()
    # print("01: ", st)
    # main_init()
    # print("02: ", time.monotonic_ns() - st)

    st = time.monotonic_ns()
    print("11: ", st)
    main_proc()
    print("12: ", time.monotonic_ns() - st)
