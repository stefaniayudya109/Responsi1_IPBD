import json
import time
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def get_data():
    options = Options()
    options.page_load_strategy = 'eager'
    options.add_argument("--headless")  # WAJIB untuk Airflow

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    driver.get("https://www.wired.com/category/business/")
    time.sleep(5)

    for i in range(3):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    articles = driver.find_elements(By.CSS_SELECTOR, "a[href*='/story/']")

    data = []
    seen = set()

    for a in articles:
        try:
            url = a.get_attribute("href")
            title = a.text.strip()
        except:
            continue

        if not title or not url or url in seen:
            continue

        seen.add(url)

        data.append({
            "title": title,
            "url": url,
            "scraped_at": datetime.now().isoformat(),
            "source": "Wired.com"
        })

        if len(data) >= 50:
            break

    driver.quit()

    # optional save file
    with open("wired_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    return data