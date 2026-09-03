# =========================
# Build stage
# =========================
FROM python:3.12.3 AS builder

WORKDIR /build

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Get your source code
RUN git clone https://github.com/yanufo/Row_APP_V1.5.git .

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Nuitka
RUN pip install --no-cache-dir nuitka

# Compile the Streamlit application
RUN python -m nuitka \
    --standalone \
    --follow-imports \
    --output-dir=/build/dist \
    app_prototype.py


# =========================
# Runtime stage
# =========================
FROM python:3.12.3-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy only the compiled application
COPY --from=builder /build/dist/app_prototype.dist /app/app_prototype.dist

EXPOSE 8501

HEALTHCHECK \
    --interval=30s \
    --timeout=10s \
    --start-period=30s \
    --retries=3 \
    CMD curl --fail http://localhost:8501/_stcore/health || exit 1

ENTRYPOINT [
    "/app/app_prototype.dist/app_prototype",
    "--server.port=8501",
    "--server.address=0.0.0.0"
]