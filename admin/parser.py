import asyncio
import json
import traceback
import random
from copy import copy, deepcopy
import time as time_

from aiogram import Bot, Dispatcher, types
from selenium.webdriver.common.action_chains import ActionChains

from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import BOT_TOKEN, MONTH_STRING

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
            cls.instance.search = False
            cls.instance.appointment = False
            cls.instance.pass_appointment = False
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

    async def driver_process(self, account, proxy: Proxy, driver=None, user_id=None):
        try:
            if not driver:
                # if self.appointment:
                #     raise ZeroDivisionError
                driver = self.driver_init(proxy)
                # if self.appointment:
                #     raise ZeroDivisionError
                driver.get('https://ais.usvisa-info.com/en-ca/niv/users/sign_in')
                driver.find_element(By.ID, 'user_email').send_keys(account.login)
                driver.find_element(By.ID, 'user_password').send_keys(account.password)
                print('------------------------')
                # if self.appointment:
                #     raise ZeroDivisionError
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
                # if self.appointment:
                # raise ZeroDivisionError
            else:
                print('redo')
            days = {}
            block = True
            for city in account.cities:
                city_days = {}
                dates = self.get_network_dates(driver, user_id, city)
                for date in dates:
                    if date_(*[int(param) for param in date.split('-')]) < account.up_to_date:
                        city_days[date] = self.get_network_times(driver, user_id, city, date)
                days[city.name] = city_days
                if not dates and block:
                    cities = City.query.all()
                    for city_ in cities:
                        time_.sleep(1)
                        dates = self.get_network_dates(driver, user_id, city_)
                        if dates:
                            block = False
                            break
                        else:
                            continue
                    if block:
                        driver.quit()
                        for admin_id in ADMIN_ID:
                            await self.send_message(admin_id, f'{account.login} заблокирован')
                        print('account_blocked')
                        Parser.loop.create_task(self.wait_account(account, db))
                        return 'block', False, False

            print(days)
        except Exception as e:
            print(traceback.format_exc())
            if driver:
                driver.quit()
                # driver.close()
            return False, False, None

        if not days:
            driver.quit()
            return False, False, None

        else:
            return days, user_id, driver

    @classmethod
    def driver_do(cls, account_id, user_id, city_id, date, time, driver=None, account=None):
        print('appointment')
        if not account:
            try:
                # proxy = Proxy.query.filter_by(status='OK').all()[0]
                account = Account.query.get(int(account_id))
                proxy = account.proxy
            except Exception as e:
                print(traceback.format_exc())
                return False
        try:

            if not driver:
                print('appointment2')
                driver = cls.driver_init(proxy)
                driver.set_window_position(0, 0)
                driver.set_window_size(1600, 1000)
                # driver.get('https://google.com')
                driver.get('https://ais.usvisa-info.com/en-ca/niv/users/sign_in')
                print(account.login)
                print(account.password)

                WebDriverWait(driver, 10000).until(
                    EC.presence_of_element_located((By.ID, 'user_email'))).send_keys(account.login)

                WebDriverWait(driver, 10000).until(
                    EC.presence_of_element_located((By.ID, 'user_password'))).send_keys(account.password)

                # driver.find_element(By.ID, 'user_password').send_keys(account.password)
                print('------------------------')
                elem = driver.find_element(By.CLASS_NAME, 'icheckbox')
                cls.scroll_shim(driver, elem)
                elem.click()
                WebDriverWait(driver, 10000).until(
                    EC.presence_of_element_located((By.XPATH, '//input[@value="Sign In"]'))).click()
            else:
                print('appointment with existing driver')
                driver.set_window_position(0, 0)
                driver.set_window_size(1600, 1000)
            # time.sleep(2)
            # driver.save_screenshot('pre.png')

            driver.get(f'https://ais.usvisa-info.com/en-ca/niv/schedule/{user_id}/appointment')

            # elem = WebDriverWait(driver, 10000).until(
            #     EC.element_to_be_clickable((By.CLASS_NAME, 'primary')))

            elem_button = driver.find_element(By.CLASS_NAME, 'primary')
            cls.scroll_shim(driver, elem_button)
            ActionChains(driver).move_to_element(elem_button).click().perform()
            # elem_button.click()
            # driver.save_screenshot('first.png')

            WebDriverWait(driver, 10000).until(
                EC.presence_of_element_located((By.ID, 'appointments_consulate_appointment_facility_id'))).click()
            print('city_select')
            # driver.find_element(By.XPATH, f'//option[@value="{city_id}"]').click()
            WebDriverWait(driver, 10000).until(
                EC.element_to_be_clickable((By.XPATH, f'//option[@value="{city_id}"]'))).click()

            time_.sleep(2)
            print('selected')
            driver.save_screenshot('first.png')

            year, month, day = date.split('-')
            try:
                print('month select')
                # WebDriverWait(driver, 10000).until(
                #     EC.presence_of_element_located((By.ID, "appointments_consulate_appointment_date"))).click()

                temp = driver.find_element(By.ID, "appointments_consulate_appointment_date")
                cls.scroll_shim(driver, temp)
                # ActionChains(driver).move_to_element(elem).click().perform()
                # temp = WebDriverWait(driver, 10000).until(EC.element_to_be_clickable((By.ID, "appointments_consulate_appointment_date")))
                action = ActionChains(driver)
                # action.move_to_element(temp)
                action.click()
                action.perform()
                print('---')
                temp.click()
                time_.sleep(2)

                while True:
                    # elem = WebDriverWait(driver, 10000).until(
                    #     EC.presence_of_element_located((By.CLASS_NAME, "ui-datepicker-group-first")))
                    driver.save_screenshot('pre_date.png')

                    elem = driver.find_element(By.CLASS_NAME, 'ui-datepicker-group-first')
                    date_text = elem.find_element(By.CLASS_NAME, 'ui-datepicker-title').text
                    # print(date_text)
                    if int(year) < int(date_text[-4:]):
                        print('no_dates')
                        driver.quit()
                        return False
                    # print(date_text, MONTH_STRING[month])
                    if year in date_text and MONTH_STRING[month] in date_text:
                        print('selected')
                        break

                    WebDriverWait(driver, 10000).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "ui-icon-circle-triangle-e"))).click()
                if month[0] == '0':
                    month = month[1]
                print(month)
                month = int(month) - 1
                with open('source.txt', 'w') as f:
                    f.write(driver.page_source.encode('utf-8').decode('utf-8'))
                days = driver.find_elements(By.XPATH, f'//td[@data-month="{month}"]')
                print(days)
                print('day select')
                for day_ in days:
                    print(day_.text)
                    if day_.text == day:
                        day_.click()
                        print('selected')
                        driver.save_screenshot('middle.png')

                        WebDriverWait(driver, 10000).until(
                            EC.presence_of_element_located(
                                (By.ID, 'appointments_consulate_appointment_time'))).click()

                        WebDriverWait(driver, 10000).until(
                            EC.presence_of_element_located(
                                (By.XPATH, f'//option[@value="{time}"]'))).click()

                        WebDriverWait(driver, 10000).until(
                            EC.presence_of_element_located(
                                (By.ID, "appointments_submit"))).click()

                        WebDriverWait(driver, 10000).until(
                            EC.presence_of_element_located(
                                (By.XPATH, "//a[@class='button alert']"))).click()

                        time_.sleep(5)
                        driver.save_screenshot('last.png')
                        driver.quit()
                        return True

                driver.quit()
                return False

            except Exception as e:
                print('err_appointment')
                print(traceback.format_exc())
                return False
        except Exception as e:
            print('err_appointment')
            print(traceback.format_exc())
            return False

        # account.status = 'DONE'
        # cls.db.session.commit()
        # return True

    @staticmethod
    async def send_message(user_id, text, keyboard=None):
        Bot.set_current(Parser.bot)
        message = await Parser.bot.send_message(
            user_id,
            text=text,
            reply_markup=keyboard
        )
        return message

    @staticmethod
    async def send_messages(days, account: Account, user_id):
        print('send_messages')
        messages = []
        for admin_id in ADMIN_ID:
            for city, dates in days.items():
                if dates:
                    city_obj = City.query.filter_by(name=city).all()[0]
                    inline_keyboard = []
                    for date, times in dates.items():
                        for time in times:
                            inline_keyboard.append(
                                [InlineKeyboardButton(text=f'{date}  {time}', callback_data=main_callback.new(
                                    account_id=account.id, user_id=user_id, city_id=city_obj.site_id, date=date,
                                    time=time.replace(':', '.')
                                ))]
                            )
                    # inline_keyboard.append(
                    #     [InlineKeyboardButton(text='Пропуск', callback_data=main_callback.new(
                    #         account_id='-', user_id='-', city_id='-', date='-',
                    #         time='-'
                    #     ))]
                    # )
                    keyboard = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
                    message = await Parser.send_message(admin_id, STD_TEXT.format(login=account.login, city=city),
                                                        keyboard)
                    messages.append(message)
        return messages
        # else:
        #     await Parser.send_message(admin_id, STD_TEXT.format(login=account.login, city=city))
    @staticmethod
    def has_days(days):
        if not days:
            return False
        for day in days.values():
            if day:
                return True
        return False

    async def parse_account(self, account: Account, proxy: Proxy, db):
        print('account parse')
        try:
            try:
                accounts = Account.query.populate_existing().filter_by(login=account.login).all()
                if not accounts or accounts[0].status != 'SEARCH':
                    return True
                print('proxy: ', proxy.https)
                days, user_id, driver = await self.driver_process(account, proxy)
                if not days:
                    return False
                elif days == 'block':
                    return 'block'
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
            messages = await self.send_messages(days, account, user_id)

            i = 0
            self.wait = True
            while days and not self.appointment:
                time_.sleep(15)
                accounts = Account.query.populate_existing().filter_by(login=account.login).all()
                if not accounts or accounts[0].status != 'SEARCH':
                    return True
                # await asyncio.sleep(5)
                if i % 12 == 0:
                    old_days = deepcopy(days)
                    days, user_id, driver = await self.driver_process(account, proxy, driver, user_id)
                    if days == 'block':
                        return 'block'
                    if days and days != old_days:
                        for message in messages:
                            try:
                                await message.delete()
                            except Exception as e:
                                print(e)
                        messages = await self.send_messages(days, account, user_id)
                i += 1

            if not days:
                for message in messages:
                    try:
                        await message.delete()
                    except Exception as e:
                        print(e)
                return

            if self.appointment:
                for message in messages:
                    try:
                        await message.delete()
                    except Exception as e:
                        print(e)
                if isinstance(self.appointment, list):
                    Bot.set_current(Parser.bot)
                    callback = self.appointment.pop(0)
                    result = self.driver_do(*self.appointment, driver, account)
                    if not result:
                        await callback.message.answer(
                            'Date not available for recording or error',
                        )
                    else:
                        await callback.message.answer_photo(
                            open('last.png', 'rb'),
                        )
                else:
                    print('self.appointment not a list')
                self.appointment = False
                self.pass_appointment = False
                return True

            else:
                for admin_id in ADMIN_ID:
                    if self.pass_appointment:
                        try:
                            for message in messages:
                                await message.delete()
                        except Exception as e:
                            pass
                        await self.send_message(admin_id, 'Пропуск')

            self.wait = False

        except:
            self.accounts.append(account)
            print(traceback.format_exc())
            return False

        return True

    def shift_proxy(self):
        if len(self.proxies) > 1:
            proxies = copy(self.proxies)
            self.proxies = proxies[1:]
            self.proxies.append(proxies[0])
            print(self.proxies)

    def add_error(self, account):
        if self.errors.get(account):
            self.errors[account] += 1
        else:
            self.errors[account] = 1

    async def parse(self, loop, db):
        Parser.bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
        # storage = MemoryStorage()
        # dp = Dispatcher(bot, storage=storage)
        print('start_parse')
        while True:
            # print('cycle_start')
            try:
                print('loop')
                sleep_conf = Config.query.all()[0]
                accounts = Account.query.populate_existing().filter_by(status='SEARCH').all()
                while True:
                    proxies = Proxy.query.populate_existing().filter_by(status='OK').all()
                    if not proxies:
                        await asyncio.sleep(20)
                    else:
                        break
                # print('cycle')
                self.proxies = proxies
                self.accounts = accounts
                self.errors = {}

                i = 0

                while self.accounts:
                    # while self.appointment:
                    #     await asyncio.sleep(10)
                    if i == 0:
                        i = 1
                    account = self.accounts.pop(0)
                    # print(self.proxies)
                    #
                    # proxy = self.proxies[0]
                    # self.shift_proxy()
                    try:
                        print(account)
                        print(account.up_to_date)
                        print(account.proxy.http)
                    except Exception as e:
                        print(e)
                        continue

                    while True:
                        try:
                            # while self.appointment:
                            #     await asyncio.sleep(10)
                            self.search = True
                            result = await self.parse_account(account, account.proxy, db)
                            self.search = False
                            if not result:
                                self.add_error(account)
                                if self.errors.get(account) > ERRS_MAX:
                                    try:
                                        self.accounts.remove(account)
                                    except:
                                        pass
                                    break
                                else:
                                    continue
                            elif result == 'block':
                                break

                        except Exception as e:
                            self.search = False
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

                    print('sleep')
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
        self.proxies.remove(proxy)
        await asyncio.sleep(30)
        proxy.status = 'OK'
        db.session.commit()
        self.proxies.append(proxy)

    async def wait_account(self, account: Account, db):
        account.status = 'WAIT'
        db.session.commit()
        await asyncio.sleep(10800)
        acc = Account.query.get(account.id)

        if acc.status == 'WAIT':
            for admin_id in ADMIN_ID:
                await self.send_message(admin_id, f'{acc.login} разблокирован')
            acc.status = 'SEARCH'
            db.session.commit()


if __name__ == '__main__':
    pass
