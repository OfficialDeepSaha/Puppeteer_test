# Use official Python runtime as a base image
FROM python:3.11-slim

# Install dependencies for Chrome and Chromium
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    chromium \
    libgdk-pixbuf2.0-0 \
    libnss3 \
    libx11-xcb1 \
    libfontconfig1 \
    libxrender1 \
    libgtk-3-0 \
    && rm -rf /var/lib/apt/lists/*

# Download and install the specific version of ChromeDriver
RUN wget -q https://storage.googleapis.com/chrome-for-testing-public/131.0.6778.69/linux64/chromedriver-linux64.zip -P /tmp && \
    unzip /tmp/chromedriver-linux64.zip -d /usr/local/bin/ && \
    rm /tmp/chromedriver-linux64.zip

# Install the required Python dependencies
COPY requirements.txt /app/
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt

# Set up environment variables for Chrome
ENV GOOGLE_CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/local/bin/chromedriver

# Expose port for FastAPI
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "Selenium_Test:app", "--host", "0.0.0.0", "--port", "8000"]
