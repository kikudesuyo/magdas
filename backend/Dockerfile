FROM python:3.11-slim

WORKDIR /app

RUN pip install uv

CMD ["sh", "-c", "uv sync && uv run inv server"]
