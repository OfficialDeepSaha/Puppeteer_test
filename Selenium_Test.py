from fastapi import FastAPI, HTTPException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException

app = FastAPI()

# ChromeDriver configuration
def configure_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')  # Required for running as root
    options.add_argument('--disable-dev-shm-usage')  # Prevent shared memory issues
    # Do not use '--headless' if you need to interact with the browser visually
    return webdriver.Chrome(options=options)

@app.get("/open-google")
async def open_google():
    """
    Endpoint to open Google's homepage using Selenium.
    """
    driver = configure_driver()

    try:
        driver.get("https://www.google.com")
        
        # Verifying that the page has loaded correctly
        if "Google" not in driver.title:
            raise HTTPException(status_code=500, detail="Failed to open Google or incorrect title")

        return {"message": "Google opened successfully!", "title": driver.title}
    except WebDriverException as e:
        raise HTTPException(status_code=500, detail=f"Error occurred while using Selenium: {str(e)}")
    finally:
        driver.quit()
