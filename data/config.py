PG_HOST = 'localhost'
PG_PASSWORD = 'fcgfTC545Kwed99erg6BHJfg'
PG_USER = 'tg_bot'
PG_DATABASE = 'tg_bot'
database_uri = f'postgres://{PG_USER}:{PG_PASSWORD}@{PG_HOST}/{PG_DATABASE}'

BOT_TOKEN = '5333769009:AAFpKnc9bagEyZ8mymEj-yUNukFrEizcULA'
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