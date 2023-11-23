import asyncio

ip = ["192.168.0.3", "192.168.0.1", "192.168.0.2", "192.168.0.4", "192.168.0.5"]

event = asyncio.Event()


async def sensor_job(sensor_id: int, sensor_address: str):
    print(f"Датчик {sensor_id} IP-адрес {sensor_address} настроен и ожидает срабатывания")
    await event.wait()
    print(f'Датчик {sensor_id} IP-адрес {sensor_address} активирован, "Wee-wee-wee-wee"')


async def alarm_on():
    event.clear()
    await asyncio.sleep(5)
    event.set()
    print("Датчики зафиксировали движение")


async def main():
    tasks = [asyncio.create_task(sensor_job(s_id, s_addr)) for s_id, s_addr in enumerate(ip)]
    await asyncio.gather(*tasks, alarm_on())


asyncio.run(main())
