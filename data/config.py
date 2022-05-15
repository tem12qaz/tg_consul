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

TELEGRAM_URL = 'http://t.me/{username}'