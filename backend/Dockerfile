FROM python:3.12-slim

WORKDIR /app

RUN pip install uv

# Install dependencies
COPY pyproject.toml  uv.lock ./
RUN uv sync

# Copy application code
COPY . .

CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
