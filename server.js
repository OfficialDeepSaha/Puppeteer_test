const puppeteer = require('puppeteer');
require("dotenv").config();

const startTwitterAuthProcess = async () => {
  const browser = await puppeteer.launch({
    headless: false, // Run browser visibly to allow user interaction
    args: ['--no-sandbox', '--disable-setuid-sandbox'],
    executablePath:  process.env.PUPPETEER_EXECUTABLE_PATH
  });

  const page = await browser.newPage();

  try {
    console.log('Opening Twitter login page...');
    const req = await page.goto('https://x.com/login', {
      waitUntil: 'networkidle2',
      timeout: 0,
    });

    const re=  req
    console.log("Response:- " , re)
    console.log('Waiting for username field to load...');
    await page.waitForSelector('input[name="text"]', { timeout: 0 });

    console.log('Listening for username input...');
    let capturedUsername = null;
    await page.exposeFunction('captureUsername', (value) => {
      capturedUsername = value;
    });
    await page.evaluate(() => {
      const usernameInput = document.querySelector('input[name="text"]');
      if (usernameInput) {
        usernameInput.addEventListener('input', (event) => {
          window.captureUsername(event.target.value);
        });
      }
    });

    console.log('Waiting for password field to load...');
    await page.waitForSelector('input[name="password"]', { timeout: 0 });

    console.log('Listening for password input...');
    let capturedPassword = null;
    await page.exposeFunction('capturePassword', (value) => {
      capturedPassword = value;
    });
    await page.evaluate(() => {
      const passwordInput = document.querySelector('input[name="password"]');
      if (passwordInput) {
        passwordInput.addEventListener('input', (event) => {
          window.capturePassword(event.target.value);
        });
      }
    });

    console.log('Waiting for user to log in...');
    await page.waitForNavigation({ waitUntil: 'networkidle2', timeout: 0 });

    if (page.url().includes('https://x.com/home')) {
      console.log('Login successful.');
    } else {
      throw new Error('Login failed or user did not complete login.');
    }

    // Capture the auth token from cookies
    const cookies = await page.cookies();
    const authToken = cookies.find((cookie) => cookie.name === 'auth_token');
    if (!authToken) {
      throw new Error('Auth token not found in cookies.');
    }

    console.log('Captured Username:', capturedUsername);
    console.log('Captured Password:', capturedPassword);
    console.log('Twitter Auth Token:', authToken.value);

    return { username: capturedUsername, password: capturedPassword, token: authToken.value };

  } catch (error) {
    console.error('Error during Twitter auth process:', error.message);
    throw error;
  } finally {
    await browser.close();
  }
};

// Run the process
startTwitterAuthProcess()
  .then(({ username, password, token }) => {
    console.log('Process completed.');
    console.log('Captured Username:', username);
    console.log('Captured Password:', password);
    console.log('Captured Token:', token);
  })
  .catch((error) => {
    console.error('Process failed:', error.message);
  });
