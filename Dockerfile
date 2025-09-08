# Use the official uv image
FROM ghcr.io/astral-sh/uv:debian

# Set working directory
WORKDIR /app

# Copy your application code
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Run your FastAPI app with uv
CMD ["uv", "run", "main.py"]
