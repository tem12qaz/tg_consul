import asyncio
import json
import time
import traceback
import random

import pytz
from datetime import datetime, timedelta
from threading import Thread

# from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from seleniumwire import webdriver

from admin.views import AdminMixin
from config import ERRS_MAX
from models import Proxy, Account, Config


# fa = UserAgent()


class Parser(object):
    loop = None
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Parser, cls).__new__(cls)
            cls.instance.table_dict = None
            cls.instance.proxies = None
        return cls.instance


    @staticmethod
    def driver_init(proxy: Proxy):
        options = Options()
        options.headless = True

        proxy_options = {
            'proxy': {
                'http': f'{proxy.http}',
                'https': f'{proxy.https}',
                'no_proxy': 'localhost,127.0.0.1,dev_server:8080'
            }
        }
        driver = webdriver.Firefox(seleniumwire_options=proxy_options, options=options)
        return driver

    @staticmethod
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

    @staticmethod
    def get_network_dates(driver, user_id, city):
        script = f'let xmlHttpReq = new XMLHttpRequest();xmlHttpReq.open("GET", "https://ais.usvisa-info.com/en-ca/niv/schedule/{user_id}/appointment/days/{city.site_id}.json?appointments[expedite]=false", false); xmlHttpReq.send(null);return xmlHttpReq.responseText;'
        dates = json.loads(driver.execute_script(script))
        dates_list = [date['date'] for date in dates]
        return dates_list

    @staticmethod
    def get_network_times(driver, user_id, city, date):
        script = f'let xmlHttpReq = new XMLHttpRequest();xmlHttpReq.open("GET", "https://ais.usvisa-info.com/en-ca/niv/schedule/{user_id}/appointment/times/{city.site_id}.json?date{date}&appointments[expedite]=false", false); xmlHttpReq.send(null);return xmlHttpReq.responseText;'
        dates = json.loads(driver.execute_script(script))
        dates_list = [date['date'] for date in dates]
        return dates_list

    def driver_process(self, account: Account, proxy: Proxy, db, reg=None):
        driver = self.driver_init(proxy)
        driver.get('https://ais.usvisa-info.com/en-ca/niv/users/sign_in')
        driver.find_element(By.ID, 'user_email').send_keys(account.login)
        driver.find_element(By.ID, 'user_password').send_keys(account.password)
        print('------------------------')
        elem = driver.find_element(By.CLASS_NAME, 'icheckbox')
        self.scroll_shim(driver, elem)
        elem.click()
        WebDriverWait(driver, 10000).until(
            EC.presence_of_element_located((By.XPATH, '//input[@value="Sign In"]'))).click()
        user_id = WebDriverWait(driver, 10000).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, 'primary'))).get_attribute('href').split('/')[-2]

        days = {}
        for city in account.cities:
            dates = self.get_network_dates(driver, user_id, city)
            for date in dates:
                if date:             # ЕСЛИ ДЕНЬ В ПРЕДЕЛАХ АККАУНТА
                    self.get_network_dates(driver, user_id, date)



    def parse_account(self, account: Account, proxy: Proxy, db):

        try:
            try:
                pass
            except Exception as e:
                print('proxy_err: ', e)
                proxy.status = 'WAIT'
                db.session.commit()

                Parser.loop.create_task(self.wait_proxy(proxy, db))
                self.accounts.append(product)
                return False
            # except ZeroDivisionError:
            #     proxy.status = 'EXPIRED'
            #     db.session.commit()
            #     return False

            offers_output = []
            for offer in offers:
                price = int(offer['price'])
                delivery = offer.get('delivery')
                if delivery:
                    delivery = delivery.split('.')[0]
                    date = datetime.strptime(delivery, '%Y-%m-%dT%H:%M:%S')
                    date = date + timedelta(hours=6)
                    if self.compare_delivery_duration_datetime(date, product):
                        offers_output.append(price)
                        break

            if offers_output:
                return min(offers_output)
            else:
                self.accounts.append(product)
                return False
        except:
            self.accounts.append(product)
            print(traceback.format_exc())
            return False

    def parse_and_process_account(self, account: Account, db, proxy: Proxy):
        self.proxies.remove(proxy)
        куыгде = await self.parse_account(account, proxy, db)
        await asyncio.sleep(0.3)
        if not price:
            if self.errors.get(product):
                self.errors[product] += 1
            else:
                self.errors[product] = 1
            product.kaspi_price = 0
        else:
            product.kaspi_price = price
            for i in range(1, 11):
                code = getattr(product, f'supplier{i}_code')
                if not code:
                    continue
                row = self.table_dict[code]
                setattr(product, f'supplier{i}_name', row[3])
                setattr(product, f'supplier{i}_amount', row[1])
                setattr(product, f'supplier{i}_price', row[0])

                db.session.commit()
                self.calculate_margin(product, commission, db, i)

        db.session.commit()
        print(product)
        self.proxies.append(proxy)

    def shift_proxy(self):
        if len(self.proxies) > 1:
            proxies = self.proxies
            self.proxies = proxies[1:].append(proxies[0])

    def add_error(self, account):
        if self.errors.get(account):
            self.errors[account] += 1
        else:
            self.errors[account] = 1

    async def parse(self, loop, db):
        while True:
            try:
                sleep_conf = Config.query.all()[0]
                accounts = Account.query.filter_by(status='SEARCH').all()
                proxies = Proxy.query.filter_by(status='OK').all()
                self.proxies = proxies
                self.accounts = accounts
                self.errors = {}

                i = 0

                while self.accounts and len([task for task in asyncio.all_tasks(loop) if not task.done()]) > i:
                    if i == 0:
                        i = 1
                    account = self.accounts[0]
                    proxy = self.proxies[0]
                    print(account)

                    while True:
                        try:
                            result = self.parse_and_process_account(account, db, proxy)
                            if not result:
                                self.add_error(account)
                                if self.errors.get(account) > ERRS_MAX:
                                    self.accounts.remove(account)
                                    break
                                else:
                                    continue

                        except Exception as e:
                            print(traceback.format_exc())
                            self.add_error(account)
                            if self.errors.get(account) > ERRS_MAX:
                                self.accounts.remove(account)
                                break
                            else:
                                continue
                            await asyncio.sleep(2)

                        else:
                            self.accounts.remove(account)
                            break
                    await asyncio.sleep(2)

                sleep = random.randint(sleep_conf.sleep_min, sleep_conf.sleep_max)
                await asyncio.sleep(sleep)
            except Exception as e:
                print(traceback.format_exc())
                await asyncio.sleep(100)

    def start_parse(self, db):
        loop = asyncio.new_event_loop()
        Parser.loop = loop
        loop.create_task(self.parse(loop, db))
        Thread(target=loop.run_forever, args=()).start()

    async def wait_proxy(self, proxy: Proxy, db):
        await asyncio.sleep(30)
        proxy.status = 'OK'
        db.session.commit()
        self.proxies.append(proxy)
