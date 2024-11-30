FROM python:3.11-slim

WORKDIR /app

# Install Rust and other build dependencies
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/* \
    && curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y

# Add Rust to PATH
ENV PATH="/root/.cargo/bin:${PATH}"

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ /app/src/
WORKDIR /app/src

EXPOSE ${FASTAPI_PORT}

# Run the application with uvicorn
CMD uvicorn main:app --host 0.0.0.0 --port ${FASTAPI_PORT}