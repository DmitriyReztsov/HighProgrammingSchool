"""
я перевел код Джавы в Питон. Из-за GIL и локально без небольшой задержки в выполнении эффект гонки скорее всего не будет получен (у меня не получилось).
Поэтому добавил задержку - тогда гонка проявляется.
Гонка возникает из-за того, что операция counter += 1 не атомарна и состоит из нескольких операций:
- захват значения, инкремент, запись обратно. На любом из этих этапов возможно изменение ресурса (counter) другим потоком.

"""

import threading
import time

counter = 0


def increment():
    global counter
    for _ in range(100_000):
        temp = counter
        time.sleep(0.000001)  # увеличиваем шанс переключения
        counter = temp + 1


def main_race():
    number_of_threads = 10
    threads = []

    for _ in range(number_of_threads):
        t = threading.Thread(target=increment)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print(f"Final counter value: {counter}")


"""
Для исключения гонки надо в Питоне добавить блокировку ресурса, чтоб другие потоки ждали его освобождения.

Результат:
Final counter value: 100006
Final counter value 2: 1000000

"""

counter2 = 0
lock = threading.Lock()


def increment2():
    global counter2

    for _ in range(100_000):
        with lock:
            counter2 += 1


def main_no_race():
    number_of_threads = 10
    threads = []

    for _ in range(number_of_threads):
        t = threading.Thread(target=increment2)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print(f"Final counter value 2: {counter2}")


"""
Взаимная блокировка - первый поток захватил лок1, второй - лок2, а ждут внутри этих блокировок освобождения второго лока (который захвачен конкурирующим потоком).

Правильный подход - брать локи в одном порядке. Или не брать лок во время блокировки другим локом.

Результат:
Thread 1 acquired lock1
Thread 1 acquired lock2
Thread 2 acquired lock2
Thread 2 acquired lock1
Finished

"""

lock1 = threading.Lock()
lock2 = threading.Lock()


def thread1_func():
    with lock1:
        print("Thread 1 acquired lock1")

        time.sleep(0.05)

        with lock2:
            print("Thread 1 acquired lock2")


def thread2_func():
    # with lock2:
    #     print("Thread 2 acquired lock2")

    #     time.sleep(0.05)

    #     with lock1:
    #         print("Thread 2 acquired lock1")

    with lock1:
        print("Thread 2 acquired lock2")

        time.sleep(0.05)

        with lock2:
            print("Thread 2 acquired lock1")


def main_dead_lock():
    thread1 = threading.Thread(target=thread1_func)
    thread2 = threading.Thread(target=thread2_func)

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    print("Finished")


if __name__ == "__main__":
    main_race()
    main_no_race()
    main_dead_lock()
