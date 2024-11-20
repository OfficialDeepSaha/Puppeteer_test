FROM ghcr.io/puppeteer/puppeteer:23.8.0

ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true \
    PUPPETEER_EXECUTABLE_PATH=/usr/bin/google-chrome-stable

WORKDIR /usr/src/app

# Copy package files
COPY package*.json ./

# Set proper permissions
USER root
RUN chmod -R 777 /usr/src/app
RUN npm install
USER pptruser

# Copy the rest of the application code
COPY . .

CMD ["node", "server.js"]
