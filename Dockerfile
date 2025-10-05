# Dockerfile
FROM python:3.11-slim

# Create the same UID (1000) that is used when running your container
RUN useradd -m -u 1000 user

# Install system dependencies (before switching to user)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies before copying the entire source tree
WORKDIR /home/user/app
COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app and switch to the non-root user
COPY --chown=user . .
USER user

# Set APP_PORT from build argument with default value
ARG APP_PORT=7420
ENV APP_PORT=$APP_PORT
ENV HOME=/home/user PATH=/home/user/.local/bin:$PATH

EXPOSE 7420
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${APP_PORT}"]
