FROM python:3.10-slim

WORKDIR /app

# Install system dependencies and tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    make \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Install the package in development mode
RUN pip install -e .

# Create non-root user
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Expose the API port
EXPOSE 8000

# Set environment variables
ENV PYTHONPATH=/app

# Create data directories if they don't exist
RUN mkdir -p /app/data/raw /app/data/processed /app/data/embeddings

# Entry point script
RUN echo '#!/bin/bash\n\
if [ "$1" = "api" ]; then\n\
    exec uvicorn workspace.app:app --host 0.0.0.0 --port 8000\n\
elif [ "$1" = "test" ]; then\n\
    exec pytest\n\
elif [ "$1" = "setup" ]; then\n\
    exec make seed-data\n\
elif [ "$1" = "shell" ]; then\n\
    exec /bin/bash\n\
elif [ "$1" = "notebook" ]; then\n\
    exec jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --allow-root\n\
elif [ "$1" = "phi" ]; then\n\
    shift\n\
    exec phi "$@"\n\
else\n\
    exec "$@"\n\
fi' > /app/docker-entrypoint.sh && chmod +x /app/docker-entrypoint.sh

ENTRYPOINT ["/app/docker-entrypoint.sh"]

# Default command
CMD ["api"]
