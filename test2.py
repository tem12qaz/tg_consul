import time

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from seleniumwire import webdriver
from selenium.webdriver.support.ui import WebDriverWait as driver_wait
from selenium.webdriver.support import expected_conditions as EC


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


def get_request_params(account, proxy):
    driver = driver_init(proxy)
    driver.get('https://ais.usvisa-info.com/en-ca/niv/users/sign_in')
    driver.find_element(By.ID, 'user_email').send_keys(account.login)
    driver.find_element(By.ID, 'user_password').send_keys(account.password)
    print('------------------------')
    elem = driver.find_element(By.CLASS_NAME, 'icheckbox')
    scroll_shim(driver, elem)
    time.sleep(4)
    driver.save_screenshot('eee2.png')
    elem.click()
    driver.find_element(By.XPATH, "//input[data-disable-with='Sign In']").click()
    time.sleep(2)
    request = driver.requests[-1]
    print(request.headers)
    print(driver.get_cookies())


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
    get_request_params(acc, prx)