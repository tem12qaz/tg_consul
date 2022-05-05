import password_generator as passgen
from db.models import TelegramUser


def get_secret(user: TelegramUser):
    return passgen.generate(length=20) + '_' + str(user.id)
