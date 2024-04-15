import logging
from socket import *

logging.basicConfig(format="%(asctime)s %(message)s", level=logging.DEBUG)
"""
因为传感器使用的是原始的TCP协议，所以需要使用socket来进行通信
"""


def read_sensor(server_ip, server_port):
    """
    读取传感器数据
    :param server_ip: 传感器IP
    :param server_port: 传感器端口
    :return: 温度，湿度，传感器返回的字符串
    """
    global temp, hum
    with socket(AF_INET, SOCK_STREAM) as s:
        s.settimeout(2)
        try:
            s.connect((server_ip, server_port))
        except Exception as e:
            logging.error(server_ip + " " + "Connect Error")
            logging.exception(e)
            return None, None, None
        text = ""
        for _ in range(0, 5):
            data = s.recv(1024).decode("utf-8")
            if not data:
                break
            else:
                try:
                    # 字符串拼接
                    text += data
                except Exception as e:
                    logging.error(server_ip + " " + "Recv Error")
                    logging.exception(e)
                    return None, None, None
    # 字符串分割
    text = text.split("\r\n")
    # 去除单位，只保留数值
    try:
        if text[1].split()[-1][-1] == "C":
            try:
                temp = float(text[1].split()[-1][:-1])
            except ValueError:
                Int = int(text[1].split()[-1][:-1].split(".")[0])
                Dec = int(text[1].split()[-1][:-1].split(".")[1][1:])
                temp = float(-1.0 * (abs(Int) + Dec * 0.01))

        if text[2].split()[-1][-1] == "%":
            hum = text[2].split()[-1][:-1]
        else:
            hum = text[3].split()[-1][:-1]
        hum = float(hum)
    except Exception as e:
        logging.error(server_ip + " Split Error")
        logging.error(text)
        return None, None, None
    return temp, hum, text


if __name__ == "__main__":
    server_ip = "127.0.0.1"
    server_port = 80
    temp, hum, _ = read_sensor(server_ip, server_port)
    print(temp, hum)
