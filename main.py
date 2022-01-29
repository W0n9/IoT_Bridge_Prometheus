import threading
import time

import yaml
from prometheus_client import Gauge, start_http_server

from read_sensor import read_sensor

# Read config file
with open("config.yaml", "r", encoding="utf-8") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
    print(config)

# Create a metric to track temperature and humidity
gt = Gauge(
    "temperature_metric_celsius",
    "Temperature measured by the WRD Sensor",
    ["instance", "location", "sub_location"],
)
gh = Gauge(
    "humidity_metric_ratio",
    "Humidity percentage measured by the WRD Sensor",
    ["instance", "location", "sub_location"],
)


def write_prometheus(sensor):
    while True:
        try:
            temp, hum, _ = read_sensor(sensor["ip"], 80)
        except:
            print(sensor["ip"] + " Error")
            print(_)
            continue
        print("Temperature: %s, Humidity: %s" % (temp, hum))
        try:
            gt.labels(
                instance=sensor["ip"],
                location=sensor["location"],
                sub_location=sensor["sub_location"],
            ).set(temp)
        except:
            print(sensor["ip"] + "Temp Error")
            print(_)
            continue
        try:
            gh.labels(
                instance=sensor["ip"],
                location=sensor["location"],
                sub_location=sensor["sub_location"],
            ).set(hum)
        except:
            print(sensor["ip"] + "Humd Error")
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
