# Hardened Dockerfile
# Phase 1: Builder
FROM python:3.11-slim AS builder

WORKDIR /app

# Upgrade pip and suppress warnings
ENV PIP_ROOT_USER_ACTION=ignore \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --user -r requirements.txt

# Phase 2: Runtime
FROM python:3.11-slim-bullseye

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/home/appuser/.local/bin:${PATH}"

# Create a non-root user
RUN groupadd -r appgroup && useradd -r -g appgroup -s /sbin/nologin -c "Docker image user" appuser

WORKDIR /app

# Copy dependencies from builder
COPY --from=builder /root/.local /home/appuser/.local
COPY --from=builder /app /app

# Copy application code with correct ownership
COPY --chown=appuser:appgroup app.py .

# Switch to non-root user
USER appuser

# Healthcheck using Python to avoid needing curl in the runtime image
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python3 -c 'import urllib.request; urllib.request.urlopen("http://localhost:5000/health")' || exit 1

EXPOSE 5000

# Use Gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]
