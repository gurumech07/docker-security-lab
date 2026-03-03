# Docker Security Lab

This project demonstrates container security best practices and vulnerability scanning with Docker Scout and Trivy.

## Project Structure

- `app.py`: Production-ready Flask API with health check.
- `Dockerfile.std`: Standard (vulnerable) Dockerfile for comparison.
- `Dockerfile`: Hardened (production-ready) Dockerfile.
- `.dockerignore`: Files to exclude from builds.
- `.github/workflows/security-scan.yml`: CI/CD security scanning.

## Quick Start

### Build Comparisons

```bash
# Build standard image
docker build -t security-lab:std -f Dockerfile.std .

# Build hardened image
docker build -t security-lab:hardened -f Dockerfile .
```

### Scan for Vulnerabilities

```bash
docker scout quickview security-lab:std
docker scout quickview security-lab:hardened
```

### Run Hardened Container

```bash
docker run -d --name security-app -p 5001:5000 security-lab:hardened
```

## Hardening Features

- **Multi-stage build process**: Separates build dependencies from the runtime image.
- **Minimal base image**: Uses `python:3.11-slim-bullseye`.
- **Non-root user execution**: Runs as `appuser` (UID 1000).
- **Python-native Health Check**: Removes `curl` from the runtime image to reduce attack surface.
- **Production Server**: Uses `Gunicorn` instead of the Flask development server.

## Automated Security

This project includes a GitHub Actions workflow that:

1. **Lints the Dockerfile**: Uses `hadolint` to check for best practices.
2. **Scans for CVEs**: Uses `Trivy` to block builds with High or Critical vulnerabilities.

### Verification

To check the health of the running container:

```bash
docker inspect --format='{{json .State.Health}}' security-app
```
