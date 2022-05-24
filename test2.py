import json
import time

import aiohttp
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from seleniumwire import webdriver
from selenium.webdriver.support.ui import WebDriverWait as driver_wait
from selenium.webdriver.support import expected_conditions as EC

from admin.config import HEADERS


def scroll_shim(driver, element):
    x = element.location['x']
    y = element.location['y']
    scroll_by_coord = 'window.scrollTo(%s,%s);' % (
        x,
        y
    )
    scroll_nav_out_of_way = 'window.scrollBy(0, -120);'
    driver.execute_script(scroll_by_coord)
    driver.execute_script(scroll_nav_out_of_way)


def driver_init(proxy):
    options = Options()
    options.headless = True
    options.add_argument("--width=1200")
    options.add_argument("--height=1000")
    proxy_options = {
        'proxy': {
            'http': f'{proxy.http}',
            'https': f'{proxy.https}',
            'no_proxy': 'localhost,127.0.0.1,dev_server:8080'
        }
    }
    driver = webdriver.Firefox(seleniumwire_options=proxy_options, options=options)
    return driver


def get_network(driver):
    logs_raw = driver.get_log("performance")
    logs = [json.loads(lr["message"])["message"] for lr in logs_raw]

    def log_filter(log_):
        return (
            # is an actual response
                log_["method"] == "Network.responseReceived"
                # and json
                and "json" in log_["params"]["response"]["mimeType"]
        )

    output = ''
    for log in filter(log_filter, logs):
        request_id = log["params"]["requestId"]
        resp_url = log["params"]["response"]["url"]
        print(f"Caught {resp_url}")
        resp = driver.execute_cdp_cmd("Network.getResponseBody", {"requestId": request_id})
        output += resp
        output += '''


'''
        print(resp)

    with open('output.txt', 'w') as f:
        f.write(output)


def get_cookies(account, proxy):
    driver = driver_init(proxy)
    driver.get('https://ais.usvisa-info.com/en-ca/niv/users/sign_in')
    driver.find_element(By.ID, 'user_email').send_keys(account.login)
    driver.find_element(By.ID, 'user_password').send_keys(account.password)
    print('------------------------')
    elem = driver.find_element(By.CLASS_NAME, 'icheckbox')
    scroll_shim(driver, elem)
    elem.click()
    WebDriverWait(driver, 10000).until(EC.presence_of_element_located((By.XPATH, '//input[@value="Sign In"]'))).click()
    # WebDriverWait(driver, 10000).until(EC.presence_of_element_located((By.CLASS_NAME, 'primary'))).click()
    user_id = WebDriverWait(driver, 10000).until(
        EC.presence_of_element_located(
            (By.CLASS_NAME, 'primary'))).get_attribute('href').split('/')[-2]

    driver.get(f'https://ais.usvisa-info.com/en-ca/niv/schedule/{user_id}/appointment')
    button = driver.find_element(By.XPATH, "//input[@value='Continue']")
    if button:
        button.click()
    time.sleep(2)



async def get_dates(account, proxy):
    cookies = get_cookies(account, proxy)
    async with aiohttp.ClientSession(cookies=cookies) as session:
        resp = await session.get(
            url='url',
            headers=HEADERS,
            proxy=str(proxy)
        )
        data = (await resp.read()).decode('utf-8')
        return data


if __name__ == '__main__':
    class Acc:
        def __init__(self):
            self.login = 'yuliakrivoruk@gmail.com'
            self.password = 'Yulia08!'

    class Prx:
        def __init__(self):
            self.ip = '138.59.207.172'
            self.port = '9068'
            self.user = 'UonNTz'
            self.password = '1tfyat'

        @property
        def http(self):
            return f'http://{self.user}:{self.password}@{self.ip}:{self.port}/'

        @property
        def https(self):
            return f'https://{self.user}:{self.password}@{self.ip}:{self.port}/'

    prx = Prx()
    acc = Acc()
    get_cookies(acc, prx)