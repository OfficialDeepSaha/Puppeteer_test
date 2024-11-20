FROM ghcr.io/puppeteer/puppeteer:23.8.0

ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true \
    PUPPETEER_EXECUTABLE_PATH=/usr/bin/google-chrome-stable

WORKDIR /usr/src/app

# Copy package files
COPY package*.json ./

# Set permissions and install Puppeteer dependencies
USER root
RUN apt-get update && apt-get install -y \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcups2 \
    libdbus-1-3 \
    libxcomposite1 \
    libxrandr2 \
    xdg-utils

# Run npm install
RUN npm install --omit=optional --no-audit --no-fund

# Copy application source code
COPY . .

USER pptruser
CMD ["node", "server.js"]

