FROM python:3.9.10-slim-bullseye

LABEL TsungWing Wong <TsungWing_Wong@outlook.com>

ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

COPY . .

RUN touch config.yaml \
    && pip3 install --no-cache-dir -r requirements.txt -i https://mirrors.bfsu.edu.cn/pypi/web/simple/

EXPOSE 9580

CMD ["python3", "main.py"]