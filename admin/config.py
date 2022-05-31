
PG_HOST = 'localhost'
PG_PASSWORD = 'zp443_eHssfghj344_Bfc75cy_v'
PG_USER = 'myuser'
PG_DATABASE = 'usa_embassy'

ERRS_MAX = 3

ADMIN_ID = '772311962'

STD_TEXT = '''Login: <b>{login}</b>
{city}
'''

BOT_TOKEN = '1671620851:AAHCEc74ng-uu4K-l6AT13slewux9cp3Zm8'

HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'ru-RU,ru;q=0.9,en;q=0.8,es;q=0.7',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Referer': 'https://ais.usvisa-info.com/en-ca/niv/users/sign_in',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Mobile Safari/537.36',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
}

DAYS_URL = 'https://ais.usvisa-info.com/en-ca/niv/schedule/38770842/appointment/days/94.json?appointments\\[expedite\\]=false'



class Configuration(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{PG_USER}:{PG_PASSWORD}@{PG_HOST}/{PG_DATABASE}'
    SQLALCHEMY_POOL_SIZE = 1

    SECRET_KEY = 'someth3489rh6&r65r^R#2$%GkBHJKN98secret'

    SECURITY_PASSWORD_SALT = 'lkpoopfdJBGYlkp_r65j_98eJKkjui890Khbh_jhb45ff_Vhgv769V7'
    SECURITY_PASSWORD_HASH = 'sha512_crypt'