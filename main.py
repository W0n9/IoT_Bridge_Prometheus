import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from prometheus_client import Gauge, make_asgi_app
from rich.logging import RichHandler

from .config import Sensor, Settings, settings
from .read_sensor import read_sensor

logging.basicConfig(
    format="%(message)s",
    level=logging.INFO,
    handlers=[RichHandler(rich_tracebacks=True)],
)


# Create a metric to track temperature and humidity
gt = Gauge(
    "temperature_metric_celsius",
    "Temperature measured by the WRD Sensor",
    ["node", "campus", "building", "room"],
)
gh = Gauge(
    "humidity_metric_ratio",
    "Humidity percentage measured by the WRD Sensor",
    ["node", "campus", "building", "room"],
)


async def write_prometheus(sensor: Sensor):
    while True:
        try:
            temp, hum, _ = await read_sensor(sensor.ip, 80)
            if hum == 0:
                raise ValueError("Humidity is 0")
            if _ == None or _ == "":
                raise ValueError("Data is None")
            # print(temp, hum, _)
        except Exception as e:
            logging.error(
                f"{sensor.ip} {sensor.campus} {sensor.building} {sensor.room} {e}"
            )
            # logging.exception(e)
            try:
                if isinstance(
                    gt.labels(
                        sensor.ip,
                        sensor.campus,
                        sensor.building,
                        sensor.room,
                    ),
                    Gauge,
                ):
                    gt.remove(
                        sensor.ip,
                        sensor.campus,
                        sensor.building,
                        sensor.room,
                    )
            except Exception as e:
                logging.exception(e)
            try:
                if isinstance(
                    gh.labels(
                        sensor.ip,
                        sensor.campus,
                        sensor.building,
                        sensor.room,
                    ),
                    Gauge,
                ):
                    gh.remove(
                        sensor.ip,
                        sensor.campus,
                        sensor.building,
                        sensor.room,
                    )
            except Exception as e:
                logging.exception(e)
            await asyncio.sleep(5)
            continue
        # print("Temperature: %s, Humidity: %s" % (temp, hum))
        if _ != None or _ != "":
            try:
                gt.labels(
                    node=sensor.ip,
                    campus=sensor.campus,
                    building=sensor.building,
                    room=sensor.room,
                ).set(temp)
            except:
                logging.error(f"{sensor.ip} Temp Error")
                print(_)
                continue
            try:
                gh.labels(
                    node=sensor.ip,
                    campus=sensor.campus,
                    building=sensor.building,
                    room=sensor.room,
                ).set(hum)
            except:
                logging.error(f"{sensor.ip} Humd Error")
                print(_)
                continue
            await asyncio.sleep(1)


async def main(settings: Settings):
    """
    后台任务，用于持续读取传感器数据，写入prometheus
    """
    import asyncer

    async with asyncer.create_task_group() as task_group:
        [task_group.soonify(write_prometheus)(sensor) for sensor in settings.sensors]


@asynccontextmanager
async def background_task(app: FastAPI):
    """
    启动后台任务，再启动fastapi
    https://fastapi.tiangolo.com/advanced/events/#lifespan
    """
    print(settings.sensors)
    asyncio.create_task(main(settings))
    yield


# Create app
app = FastAPI(debug=False, lifespan=background_task)

# Add prometheus asgi middleware to route /metrics requests
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=9580)
