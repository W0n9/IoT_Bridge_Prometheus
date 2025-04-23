FROM python:3.13-slim

LABEL TsungWing.Wong="TsungWing_Wong@outlook.com"

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:0.6.16 /uv /uvx /bin/

# Copy the application into the container.
COPY . /app

# Install the application dependencies.
WORKDIR /app
RUN uv sync --frozen --no-cache

# RUN pip install uv \
#     && touch config.yaml \
#     && uv pip install .

EXPOSE 9580

# Run the application.
CMD ["/app/.venv/bin/fastapi", "run", "main.py", "--port", "9580"]