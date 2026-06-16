import threading
import time

counter = 0
lock = threading.Lock()


def task():
    global counter

    # На таком маленьком примере построчный перевод из Джавы в Питон не покажет гонку из-за GIL, поэтому добавил еще
    # операцию над ресурсом - присваивание + задержка. В таком случае гонка проявляется
    # for _ in range(10):
    #     t = counter
    #     time.sleep(0.0001)
    #     counter = t + 1

    # Для работы с гонкой используем Lock()
    for _ in range(10):
        with lock:
            t = counter
            time.sleep(0.0001)
            counter = t + 1


def main():
    global counter

    thread1 = threading.Thread(target=task)
    thread2 = threading.Thread(target=task)

    thread1.start()
    thread2.start()

    try:
        thread1.join()
        thread2.join()
    except Exception as e:
        print(e)

    print(f"Counter: {counter}")


if __name__ == "__main__":
    main()
