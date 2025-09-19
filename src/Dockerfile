FROM python:3.10-slim
WORKDIR /app
COPY . /app
RUN apt-get update && apt-get install -y libusb-1.0-0 && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir pyusb flask pytest
EXPOSE 5000
CMD ["python", "main.py"]
