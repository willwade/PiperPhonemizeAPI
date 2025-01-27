# Use multi-stage build for smaller final image
FROM python:3.9-slim as builder

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    autoconf \
    automake \
    libtool \
    pkg-config \
    make \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install espeak-ng from Rhasspy fork
RUN git clone https://github.com/rhasspy/espeak-ng.git \
    && cd espeak-ng \
    && ./autogen.sh \
    && ./configure --prefix=/usr \
    && make \
    && make install \
    && cd .. \
    && rm -rf espeak-ng

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Copy project files
WORKDIR /app
COPY pyproject.toml ./
COPY app ./app

# Install Python dependencies
RUN pip install --no-cache-dir ".[dev]"

# Final stage
FROM python:3.9-slim

# Install curl for healthcheck
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy installed packages and espeak-ng from builder
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=builder /usr/local/bin/uvicorn /usr/local/bin/
COPY --from=builder /usr/lib/libespeak-ng.so* /usr/lib/
COPY --from=builder /usr/lib/libespeak-ng.a /usr/lib/
COPY --from=builder /usr/share/espeak-ng-data /usr/share/espeak-ng-data

WORKDIR /app
COPY app ./app

# Add healthcheck
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Expose port
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"] 