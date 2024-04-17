import logging
import threading
import time

import yaml
from prometheus_client import Gauge, start_http_server

from read_sensor import read_sensor

logging.basicConfig(format="%(asctime)s %(message)s", level=logging.DEBUG)

# Read config file
with open("config.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)
    logging.info(config)

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


def write_prometheus(sensor):
    while True:
        try:
            temp, hum, _ = read_sensor(sensor["ip"], 80)
            if hum == 0:
                raise ValueError("Humidity is 0")
            # print(temp, hum, _)
        except Exception as e:
            logging.error(
                sensor["ip"] + sensor["campus"] + sensor["building"] + sensor["room"]
            )
            logging.exception(e)
            try:
                if isinstance(
                    gt.labels(
                        sensor["ip"],
                        sensor["campus"],
                        sensor["building"],
                        sensor["room"],
                    ),
                    Gauge,
                ):
                    gt.remove(
                        sensor["ip"],
                        sensor["campus"],
                        sensor["building"],
                        sensor["room"],
                    )
            except Exception as e:
                logging.exception(e)
            try:
                if isinstance(
                    gh.labels(
                        sensor["ip"],
                        sensor["campus"],
                        sensor["building"],
                        sensor["room"],
                    ),
                    Gauge,
                ):
                    gh.remove(
                        sensor["ip"],
                        sensor["campus"],
                        sensor["building"],
                        sensor["room"],
                    )
            except Exception as e:
                logging.exception(e)
            time.sleep(5)
            continue
        # print("Temperature: %s, Humidity: %s" % (temp, hum))
        if _ != None:
            try:
                gt.labels(
                    node=sensor["ip"],
                    campus=sensor["campus"],
                    building=sensor["building"],
                    room=sensor["room"],
                ).set(temp)
            except:
                logging.error(sensor["ip"] + " Temp Error")
                print(_)
                continue
            try:
                gh.labels(
                    node=sensor["ip"],
                    campus=sensor["campus"],
                    building=sensor["building"],
                    room=sensor["room"],
                ).set(hum)
            except:
                logging.error(sensor["ip"] + " Humd Error")
                print(_)
                continue
            time.sleep(1)


if __name__ == "__main__":
    # Start up the server to expose the metrics.
    start_http_server(9580, addr="0.0.0.0")
    # 遍历传感器
    for sensor in config["sensors"]:
        t = threading.Thread(target=write_prometheus, args=(sensor,))
        t.start()
