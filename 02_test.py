import os
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Chrome 옵션 설정
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--remote-debugging-port=9222")

# Chrome 경로 설정 (Codespaces의 일반적인 Chrome 위치)
CHROME_PATH = "/usr/bin/google-chrome"
if os.path.exists(CHROME_PATH):
    chrome_options.binary_location = CHROME_PATH
    logging.info(f"Chrome found at {CHROME_PATH}")
else:
    logging.warning(f"Chrome not found at {CHROME_PATH}. Attempting to use system default.")

try:
    # WebDriver 설정
    logging.info("Initializing Chrome WebDriver...")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # 페이지 로드
    url = "https://new.land.naver.com/houses?ms=37.5342137,127.0625872,16&a=VL:DDDGG:JWJT:SGJT:HOJT&b=A1&e=RETAIL"
    logging.info(f"Loading page: {url}")
    driver.get(url)

    # 데이터 추출
    logging.info("Extracting data...")
    try:
        # 페이지가 완전히 로드될 때까지 기다림
        element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "item"))
        )
        
        # 데이터 추출 로직
        items = driver.find_elements(By.CLASS_NAME, "item")
        for index, item in enumerate(items, start=1):
            try:
                title = item.find_element(By.CLASS_NAME, "item_title").text
                price = item.find_element(By.CLASS_NAME, "price").text
                info = item.find_element(By.CLASS_NAME, "info_area").text
                
                logging.info(f"Item {index}: Title: {title}, Price: {price}")
                logging.info(f"Info: {info}")
                logging.info("-" * 50)
            except Exception as e:
                logging.error(f"Error extracting data from item {index}: {str(e)}")

    except TimeoutException:
        logging.error("Timeout waiting for page to load")
    except Exception as e:
        logging.error(f"Error during data extraction: {str(e)}")

except WebDriverException as e:
    logging.error(f"WebDriver error: {str(e)}")
except Exception as e:
    logging.error(f"Unexpected error: {str(e)}")

finally:
    logging.info("Closing WebDriver...")
    if 'driver' in locals():
        driver.quit()