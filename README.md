# Docker Security Lab

This project demonstrates container security best practices and automated vulnerability scanning using SonarCloud, Gitleaks, and Docker Scout.

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

## Automated Security & Deployment

This project includes a GitHub Actions workflow that:

1. **Secret Scanning**: Uses `gitleaks` to detect exposed credentials in the codebase.
2. **Linting the Dockerfile**: Uses `hadolint` to check for best practices.
3. **SAST Analysis**: Uses **SonarQube (SonarCloud)** to analyze code and Dockerfiles.
4. **Vulnerability Comparison**: Uses **Docker Scout** to compare the hardened image against a legacy standard image, highlighting security wins.
5. **Pushes to Docker Hub**: Automatically publishes the hardened image if all checks pass.

### Interpreting Comparison Reports

You can find the "Vulnerability Delta" in the **GitHub Actions > [Job Name] > Summary** page. Look for the Docker Scout section to see how many Critical and High vulnerabilities were removed by the hardening process.

### CI/CD Setup (GitHub Secrets)

To enable the full pipeline, add the following secrets to your GitHub repository (**Settings > Secrets and variables > Actions**):

- `SONAR_TOKEN`: From your SonarCloud account.
- `DOCKERHUB_USERNAME`: Your Docker Hub username.
- `DOCKERHUB_TOKEN`: A Personal Access Token (PAT) from Docker Hub.

### Verification

To check the health of the running container locally:

```bash
docker inspect --format='{{json .State.Health}}' security-app
```
