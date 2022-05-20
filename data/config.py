PG_HOST = 'localhost'
PG_PASSWORD = 'hvg32hiu_6f5vgi_tf7'
PG_USER = 'gift'
PG_DATABASE = 'gift'
database_uri = f'postgres://{PG_USER}:{PG_PASSWORD}@{PG_HOST}/{PG_DATABASE}'

BOT_TOKEN = '5228715629:AAHkSptETXeVnNs-_I-AyqEsENNVAC5yfqQ'
SECRET_PATTERN = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_='

FLOOD_RATE = 0.2


# to_check = {
#     'partner1': ('donor1', 'donor2'),
#     'partner1': ('donor2', 'donor3'),
#     'partner1': ('donor1', 'donor2'),
#     'partner1': ('donor1', 'donor2'),
# }


tables_order = (
    'start',
    'wood',
    'bronze',
    'silver',
    'gold',
    'platinum',
    'legendary'
)

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

TELEGRAM_URL = 'http://t.me/{username}'