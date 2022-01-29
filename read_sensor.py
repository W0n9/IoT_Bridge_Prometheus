from socket import *

"""
因为传感器使用的是原始的TCP协议，所以需要使用socket来进行通信
"""


def read_sensor(server_ip, server_port):
    global temp, hum
    with socket(AF_INET, SOCK_STREAM) as s:
        s.connect((server_ip, server_port))
        text = ""
        for _ in range(0, 5):
            data = s.recv(1024).decode("utf-8")
            if not data:
                break
            else:
                # 字符串拼接
                text += data
    # 字符串分割
    text = text.split("\r\n")
    # 去除单位，只保留数值
    try:
        if text[1].split()[-1][-1] == "C":
            temp = text[1].split()[-1][:-1]

        if text[2].split()[-1][-1] == "%":
            hum = text[2].split()[-1][:-1]
        else:
            hum = text[3].split()[-1][:-1]
    except:
        print("Error")
        print(text)
        return None, None, None
    return temp, hum, text


if __name__ == "__main__":
    server_ip = "127.0.0.1"
    server_port = 80
    temp, hum, _ = read_sensor(server_ip, server_port)
    print(temp, hum)