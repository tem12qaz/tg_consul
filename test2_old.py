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


def get_network_dates(driver):
    # for request in driver.requests:
    #     if request.response:
    #         if 'ais.usvisa-info.com/en-ca/niv/schedule/38770842/appointment/days/'in request.url:
    #             return
    script = 'let xmlHttpReq = new XMLHttpRequest();xmlHttpReq.open("GET", "https://ais.usvisa-info.com/en-ca/niv/schedule/38770842/appointment/days/94.json?appointments[expedite]=false", false); xmlHttpReq.send(null);return xmlHttpReq.responseText;'
    print(driver.execute_script())

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
    get_network(driver)


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