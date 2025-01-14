# Function: 读取传感器数据
import asyncio
import logging


async def read_sensor(server_ip, server_port):
    """
    读取传感器数据
    :param server_ip: 传感器IP
    :param server_port: 传感器端口
    :return: 温度，湿度，传感器返回的字符串
    """
    # global temp, hum
    try:
        """
        因为传感器使用的是原始的TCP协议，所以需要使用socket来进行通信
        设置超时时间为2秒，避免超时阻塞主线程
        """
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(server_ip, server_port), timeout=2
        )
    except asyncio.TimeoutError:
        logging.error(f"{server_ip} Connection Timeout")
        return None, None, list()
    except ConnectionRefusedError:
        logging.error(f"{server_ip} Connection Refused")
        return None, None, list()
    except Exception as e:
        logging.error(f"{server_ip} Connection Error")
        logging.exception(e)
        return None, None, list()
    text: list[str] = []
    for _ in range(5):
        data = await asyncio.wait_for(reader.readline(), timeout=1.0)
        if not data:
            break
        else:
            try:
                # 字符串拼接
                text.append(data.decode("utf-8").strip("\r\n"))
            except UnicodeDecodeError:
                logging.error(f"{server_ip} Decode Error")
                return None, None, list()
            except asyncio.TimeoutError:
                logging.error(f"{server_ip} Read Timeout")
                return None, None, list()
    writer.close()
    await writer.wait_closed()
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
    except (IndexError, ValueError) as e:
        logging.error(f"{server_ip} Split Error {e}")
        logging.error(text)
        return None, None, list()
    return temp, hum, text


if __name__ == "__main__":
    server_ip = "10.10.31.253"
    server_port = 80
    temp, hum, _ = asyncio.run(read_sensor(server_ip, server_port))
    print(temp, hum)
