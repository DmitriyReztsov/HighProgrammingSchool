import asyncio

from _5_6_space_research_data import sensors, space_data, space_time, test_type


async def sensor_data(sensor_name):
    await asyncio.sleep(space_time(sensor_name))
    data_from_sensor = space_data(sensor_name)

    return f"{sensor_name}_data: {''.join(data_from_sensor)}"


async def main():
    tasks_list = [
        asyncio.create_task(sensor_data(sensor_name))
        for sensor_name in sorted(sensors, key=lambda x: int(x.split("_")[1]))
    ]
    tasks_results = await asyncio.gather(*tasks_list)
    result = [
        f"Результаты проведения теста типа {test_type}:",
    ] + tasks_results
    return result


a = asyncio.run(main())
