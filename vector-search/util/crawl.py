from selenium.webdriver.chrome.options import Options
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def get_webdriver():
    """
    Selenium WebDriver 객체를 초기화하고 반환합니다.
    """
    selenium_url = os.getenv("SELENIUM_URL")
    # WebDriver 옵션 설정
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    # 원격(Remote) WebDriver에 연결합니다.
    driver = webdriver.Remote(command_executor=selenium_url, options=options)

    return driver


def get_web_content(driver, url, class_name):
    """
    WebDriver를 사용하여 주어진 URL에서 특정 클래스명의 모든 텍스트를 추출합니다.
    """
    try:
        driver.get(url)

        wait = WebDriverWait(driver, 10)
        main_content_div = wait.until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, class_name))
        )

        extracted_text = "\n".join([div.text for div in main_content_div])
        return extracted_text

    except Exception as e:
        print(f"URL: {url}에서 웹 콘텐츠를 가져오는 중 오류 발생: {e}")
        return "" 