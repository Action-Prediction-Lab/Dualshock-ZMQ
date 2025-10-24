FROM python:3.9-slim-bullseye

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libsdl2-2.0-0 \
    udev \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt



COPY dualshock_publisher.py .
COPY dualshock_mappings.py .

# Command to run the application
CMD ["python", "dualshock_publisher.py"]
