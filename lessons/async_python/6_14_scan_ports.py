import asyncio
import random


async def scan_port(address, port):
    await asyncio.sleep(random.randint(0, 5))
    if port_is_open := bool(random.randint(0, 1)):
        print(f"Порт {port} на адресе {address} открыт")
    return port, port_is_open


async def scan_range(address, start_port, end_port):
    print(f"Сканирование портов с {start_port} по {end_port} на адресе {address}")
    tasks = [asyncio.create_task(scan_port(address, port)) for port in range(start_port, end_port + 1)]
    results = await asyncio.gather(*tasks)
    open_ports = [port for port, port_is_open in results if port_is_open]
    if open_ports:
        print(f"Открытые порты на адресе {address}: {open_ports}")
    else:
        print(f"Открытых портов на адресе {address} не найдено")


asyncio.run(scan_range("192.168.0.1", 80, 85))
