import asyncio
import json
import traceback
import random

import pytz
from datetime import datetime, timedelta, date as date_
from threading import Thread

from pprint import pprint

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from seleniumwire import webdriver

from flask_app_init import db
from config import ERRS_MAX, ADMIN_ID, STD_TEXT
from loader import bot
from models import Proxy, Account, Config, City

main_callback = CallbackData("main", 'account_id', 'user_id', 'city_id', 'date', 'time')


class Parser(object):
    loop = None

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Parser, cls).__new__(cls)
            cls.instance.table_dict = None
            cls.instance.proxies = None
            cls.instance.db = db
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
        script = f'let xmlHttpReq = new XMLHttpRequest();xmlHttpReq.open("GET", "https://ais.usvisa-info.com/en-ca/niv/schedule/{user_id}/appointment/times/{city.site_id}.json?date={date}&appointments[expedite]=false", false); xmlHttpReq.send(null);return xmlHttpReq.responseText;'
        times = json.loads(driver.execute_script(script))
        return times['available_times']

    def driver_process(self, account, proxy: Proxy):
        driver = None
        try:
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
                EC.element_to_be_clickable(
                    (By.CLASS_NAME, 'primary')))

            # print(user_id.get_attribute('innerHTML'))
            user_id = user_id.get_attribute('href').split('/')[-2]
            print(user_id)

            days = {}
            for city in account.cities:
                city_days = {}
                dates = self.get_network_dates(driver, user_id, city)
                for date in dates:
                    if date_(*[int(param) for param in date.split('-')]) < account.up_to_date:
                        city_days[date] = self.get_network_times(driver, user_id, city, date)
                days[city.name] = city_days

            print(days)
        except Exception as e:
            print(traceback.format_exc())
            if driver:
                driver.quit()
                # driver.close()
            return False, False

        driver.quit()
        # driver.close()
        return days, user_id

    @classmethod
    def driver_do(cls, account_id, user_id, city_id, date, time):
        driver = None
        proxy = Proxy.query.filter_by(status='OK').all()[0]
        account = Account.query.filter(id=int(account_id)).all()[0]
        try:
            driver = cls.driver_init(proxy)
            driver.get('https://google.com')
            # driver.get('https://ais.usvisa-info.com/en-ca/niv/users/sign_in')
            driver.find_element(By.ID, 'user_email').send_keys(account.login)
            driver.find_element(By.ID, 'user_password').send_keys(account.password)
            print('------------------------')
            elem = driver.find_element(By.CLASS_NAME, 'icheckbox')
            cls.scroll_shim(driver, elem)
            elem.click()
            WebDriverWait(driver, 10000).until(
                EC.presence_of_element_located((By.XPATH, '//input[@value="Sign In"]'))).click()

            user_id = WebDriverWait(driver, 10000).until(
                EC.element_to_be_clickable(
                    (By.CLASS_NAME, 'primary')))

            user_id = user_id.get_attribute('href').split('/')[-2]
            print(user_id)

            driver.get('https://ais.usvisa-info.com/en-ca/niv/schedule/38770842/appointment')

            WebDriverWait(driver, 10000).until(
                EC.element_to_be_clickable(By.CLASS_NAME, 'primary')).click()

            authenticity_token = WebDriverWait(driver, 10000).until(
                EC.element_to_be_clickable(By.XPATH, '//input[@name="authenticity_token"]')).get_attribute('value')

            data = {
                'utf8': '✓',
                'authenticity_token': authenticity_token,
                'confirmed_limit_message': '1',
                'use_consulate_appointment_capacity': 'true',
                'appointments[consulate_appointment][facility_id]': city_id,
                'appointments[consulate_appointment][date]': date,
                'appointments[consulate_appointment][time]': time,
            }
            script = f'''var xhr = new XMLHttpRequest();xhr.open("POST", https://ais.usvisa-info.com/en-ca/niv/schedule/{user_id}/appointment, true);xhr.setRequestHeader('Content-Type', 'application/json');xhr.send(JSON.stringify({data}));'''
            result = driver.execute_script(script)
            with open('results.txt', 'a') as f:
                f.write('--------------')
                f.write(result)

        except:
            if driver:
                driver.quit()
                # driver.close()
            return False
        driver.quit()
        # driver.close()
        account.status = 'DONE'
        cls.db.session.commit()
        return True

    @staticmethod
    async def send_messages(days, account: Account, user_id):
        print('send_messages')
        async for admin_id in ADMIN_ID:
            for city, dates in days.items():
                if dates:
                    city_obj = City.query.filter_by(name=city).all()[0]
                    inline_keyboard = []
                    for date, times in dates.items():
                        for time in times:
                            time = time.replace(':', '.')
                            inline_keyboard.append(
                                [InlineKeyboardButton(text=f'{date}  {time}', callback_data=main_callback.new(
                                    account_id=account.id, user_id=user_id, city_id=city_obj.id, date=date, time=time
                                ))]
                            )
                    keyboard = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
                    await bot.send_message(
                        admin_id,
                        text=STD_TEXT.format(login=account.login, city=city),
                        reply_markup=keyboard
                    )
                else:
                    await bot.send_message(
                        admin_id,
                        text=STD_TEXT.format(login=account.login, city=city),
                    )

    async def parse_account(self, account: Account, proxy: Proxy, db):
        print('account parse')
        try:
            try:
                days, user_id = self.driver_process(account, proxy)
                if not days:
                    return False
            except Exception as e:
                print('proxy_err: ', e)
                proxy.status = 'WAIT'
                db.session.commit()

                Parser.loop.create_task(self.wait_proxy(proxy, db))
                self.accounts.append(account)
                return False
            # except ZeroDivisionError:
            #     proxy.status = 'EXPIRED'
            #     db.session.commit()
            #     return False
            await asyncio.sleep(0.1)
            await self.send_messages(days, account, user_id)

        except:
            self.accounts.append(account)
            print(traceback.format_exc())
            return False

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
            print('cycle_start')
            try:
                sleep_conf = Config.query.all()[0]
                accounts = Account.query.filter_by(status='SEARCH').all()
                while True:
                    proxies = Proxy.query.filter_by(status='OK').all()
                    if not proxies:
                        await asyncio.sleep(20)
                    else:
                        break
                self.proxies = proxies
                self.accounts = accounts
                self.errors = {}

                i = 0

                while self.accounts and len([task for task in asyncio.all_tasks(loop) if not task.done()]) > i:
                    if i == 0:
                        i = 1
                    account = self.accounts.pop(0)
                    proxy = self.proxies[0]
                    self.shift_proxy()
                    print(account)
                    print(proxy.http)

                    while True:
                        try:
                            result = await self.parse_account(account, proxy, db)
                            if not result:
                                self.add_error(account)
                                if self.errors.get(account) > ERRS_MAX:
                                    try:
                                        self.accounts.remove(account)
                                    except:
                                        pass
                                    break
                                    break
                                else:
                                    continue

                        except Exception as e:
                            print(traceback.format_exc())
                            self.add_error(account)
                            if self.errors.get(account) > ERRS_MAX:
                                try:
                                    self.accounts.remove(account)
                                except:
                                    pass
                                break
                            else:
                                continue
                            await asyncio.sleep(2)

                        else:
                            break
                    await asyncio.sleep(2)

                sleep = random.randint(sleep_conf.sleep_min, sleep_conf.sleep_max)
                await asyncio.sleep(sleep)
            except Exception as e:
                print(traceback.format_exc())
                await asyncio.sleep(100)

    def start_parse(self, db=db):
        loop = asyncio.new_event_loop()
        Parser.loop = loop
        loop.create_task(self.parse(loop, db))
        Thread(target=loop.run_forever, args=()).start()

    async def wait_proxy(self, proxy: Proxy, db):
        await asyncio.sleep(30)
        proxy.status = 'OK'
        db.session.commit()
        self.proxies.append(proxy)


if __name__ == '__main__':
    pass