from fastapi import FastAPI, HTTPException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os

app = FastAPI()

# ChromeDriver configuration
def configure_driver(environment='production'):

    # service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    
    if environment != 'production':
       options.add_argument('--headless')

    
    # Add common options
    options.add_argument('--no-sandbox')  # Required for running as root
    options.add_argument('--disable-dev-shm-usage')  # Prevent shared memory issues
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--remote-debugging-port=9222')
    options.binary_location = os.getenv('GOOGLE_CHROME_BIN', '/usr/bin/chromium')
    service = Service(ChromeDriverManager().install())
    
    return webdriver.Chrome(executable_path='/usr/local/bin/chromedriver', options=options)

@app.get("/")
def read_root():
    return {"message": "Google Selenium Running !!"}



@app.get("/open-google")
async def open_google():
    """
    Endpoint to open Google's homepage using Selenium.
    """
    
    environment = 'production'
    
    driver = configure_driver(environment=environment)

    try:
        driver.get("https://google.com")
        
        # Verifying that the page has loaded correctly
        if "Google" not in driver.title:
            raise HTTPException(status_code=500, detail="Failed to open Google or incorrect title")

        return {"message": "Google opened successfully!", "title": driver.title}
    except WebDriverException as e:
        raise HTTPException(status_code=500, detail=f"Error occurred while using Selenium: {str(e)}")
    finally:
        driver.quit()
