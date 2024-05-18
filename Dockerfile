FROM python:3.12-alpine3.19

LABEL TsungWing Wong <TsungWing_Wong@outlook.com>

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

COPY . .

RUN touch config.yaml \
    && pip3 install --no-cache-dir -r requirements.txt -i https://mirrors.bfsu.edu.cn/pypi/web/simple

EXPOSE 9580

CMD ["fastapi", "run", "--port", "9580", "main.py"]