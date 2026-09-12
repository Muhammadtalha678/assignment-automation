# Base image.
FROM python:3.14-slim

# install uv and copy specific file to run uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Xvfb aur GUI libraries install karein jo headless=False chalane ke liye zaroori hain
RUN apt-get update && apt-get install -y xvfb x11-xkb-utils libxpm4 libxrender1 libxtst6 && rm -rf /var/lib/apt/lists/*

# Where all my project files are stored inside container
WORKDIR /app

# Copy dependency files into /app
COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-cache --no-editable

ENV PATH="/app/.venv/bin:$PATH"

RUN uv run playwright install chromium  --with-deps && \
    apt-get clean && rm -rf /var/lib/apt/lists/*


# Now copy all my project files into /app
COPY . .



# Run the application.
CMD ["xvfb-run", "--server-args=-screen 0 1920x1080x24", "uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
# CMD ["uv", "run","uvicorn", "main:app", "--host", "0.0.0.0","--port", "7860"]