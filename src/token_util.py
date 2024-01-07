import time

import selenium.webdriver


def get_new_token():
    try:
        driver = selenium.webdriver.Chrome()
    except Exception:
        print("Chrome is not installed on your PC")
        return ""
    driver.get("https://myschool.mosreg.ru/diary/schedules/schedule")
    time.sleep(2)
    while driver.current_url != "https://myschool.mosreg.ru/diary/schedules/schedule":
        time.sleep(1)
    return driver.get_cookie("auth_token")["value"]
