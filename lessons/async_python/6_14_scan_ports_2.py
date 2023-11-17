import asyncio
import random


async def scan_port(address, port, lock, number_open_ports):
    await asyncio.sleep(1)
    if port_is_open := random.choices([True, False], weights=[0.01, 0.99], k=1)[0]:
        print(f"Port {port} on {address} is open")
        async with lock:
            if number_open_ports.get(address):
                number_open_ports[address] += 1
            else:
                number_open_ports[address] = 1
    return port, port_is_open


async def scan_range(address, start_port, end_port, lock, number_open_ports):
    print(f"Scanning ports {start_port}-{end_port} on {address}")
    tasks = [
        asyncio.create_task(scan_port(address, port, lock, number_open_ports))
        for port in range(start_port, end_port + 1)
    ]
    results = await asyncio.gather(*tasks)
    open_ports = [port for port, port_is_open in results if port_is_open]
    if not open_ports:
        print(f"No open ports on {address}")
        async with lock:
            number_open_ports[address] = 0
    return len(open_ports)


async def main():
    number_open_ports = {}
    # список ip-адресов
    ip_addresses = [
        "192.168.0.1",
        "192.168.0.2",
        "192.168.0.3",
        "192.168.0.4",
        "192.168.0.5",
        "192.168.0.6",
        "192.168.0.7",
        "192.168.0.8",
        "192.168.0.9",
        "192.168.0.10",
        "192.168.1.1",
        "192.168.1.2",
        "192.168.1.3",
        "192.168.1.4",
        "192.168.1.5",
        "192.168.1.6",
        "192.168.1.7",
        "192.168.1.8",
        "192.168.1.9",
        "192.168.1.10",
        "192.168.2.1",
        "192.168.2.2",
        "192.168.2.3",
        "192.168.2.4",
        "192.168.2.5",
    ]

    start_port = 0  # Получение стартового порта из аргументов командной строки
    end_port = 300  # Получение конечного порта из аргументов командной строки
    lock = asyncio.Lock()
    for ip_adress in ip_addresses:
        await scan_range(
            ip_adress, start_port, end_port, lock, number_open_ports
        )  # Выполнение асинхронной функции сканирования портов
    for ip_adress in ip_addresses:
        print(f"Всего найдено открытых портов {number_open_ports[ip_adress]} для ip: {ip_adress}")


asyncio.run(main())  # Запуск асинхронного приложения
