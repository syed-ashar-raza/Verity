FROM python:3.13-slim
WORKDIR /app
COPY pyproject.toml README.md LICENSE ./
COPY src ./src
COPY examples ./examples
RUN pip install --no-cache-dir .
EXPOSE 8000
CMD ["verity", "serve", "--host", "0.0.0.0", "--port", "8000"]
