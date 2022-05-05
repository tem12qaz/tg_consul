PG_HOST = 'localhost'
PG_PASSWORD = 'pass'
PG_USER = 'myuser'
PG_DATABASE = 'meal_db'
database_uri = f'postgres://{PG_USER}:{PG_PASSWORD}@{PG_HOST}/{PG_DATABASE}'

BOT_TOKEN = '1671620851:AAFJCnwlJXzMHyyc-E-mQ9ivXYpL9JVtwYU'
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

TELEGRAM_URL = 'htttp://t.me/{username}'