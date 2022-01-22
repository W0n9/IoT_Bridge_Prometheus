from prometheus_client import start_http_server, Gauge
from read_sensor import read_sensor
import time
import yaml

# Read config file
with open("config.yaml", "r") as f:
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

if __name__ == "__main__":
    # Start up the server to expose the metrics.
    start_http_server(8000, addr="0.0.0.0")
    # 遍历传感器
    while True:
        for sensor in config["sensors"]:
            try:
                temp, hum, _ = read_sensor(sensor["ip"], 80)
            except:
                print(sensor["ip"] + " Error")
                print(_)
                continue
            print("Temperature: %s, Humidity: %s" % (temp, hum))
            gt.labels(
                instance=sensor["ip"],
                location=sensor["location"],
                sub_location=sensor["sub_location"],
            ).set(temp)
            gh.labels(
                instance=sensor["ip"],
                location=sensor["location"],
                sub_location=sensor["sub_location"],
            ).set(hum)
        time.sleep(1)
