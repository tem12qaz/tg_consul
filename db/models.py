import asyncio
import time

from tortoise.models import Model
from tortoise import fields
from flask_security import UserMixin, RoleMixin


class TelegramUser(Model):
    id = fields.IntField(pk=True)
    telegram_id = fields.BigIntField(unique=True, index=True)
    username = fields.CharField(128, unique=True, null=True)
    active = fields.BooleanField(default=False)
    inviter = fields.ForeignKeyField('models.TelegramUser', related_name='referrals', index=True, null=True)
    referral_url = fields.CharField(32, null=True)

    start_block = fields.IntField(null=True)
    wood_block = fields.IntField(null=True)
    bronze_block = fields.IntField(null=True)
    silver_block = fields.IntField(null=True)
    gold_block = fields.IntField(null=True)
    platinum_block = fields.IntField(null=True)
    legendary_block = fields.IntField(null=True)

    wood_key = fields.SmallIntField(default=0)
    bronze_key = fields.SmallIntField(default=0)
    silver_key = fields.SmallIntField(default=0)
    gold_key = fields.SmallIntField(default=0)
    platinum_key = fields.SmallIntField(default=0)
    legendary_key = fields.SmallIntField(default=0)

    async def games(self):
        await asyncio.sleep(1)
        pass
        # donors = (
        #     await self.game_donor1,
        #     await self.game_donor2,
        #     await self.game_donor3,
        #     await self.game_donor4,
        #     await self.game_donor5,
        #     await self.game_donor6,
        #     await self.game_donor7,
        #     await self.game_donor8,
        # )
        # partners = (
        #     await self.game_partner1,
        #     await self.game_partner2,
        #     await self.game_partner3,
        #     await self.game_partner4,
        # )
        # mentors = (
        #     await self.game_mentor1,
        #     await self.game_mentor2,
        # )
        # master = await self.game_master
        #
        # games = {}
        #
        # for i in donors:
        #     if i:
        #         games[i] = f'donor{donors.index(i)+1}'
        #
        # for i in partners:
        #     if i:
        #         games[i] = f'partner{partners.index(i)+1}'
        #
        # for i in mentors:
        #     if i:
        #         games[i] = f'mentor{mentors.index(i)+1}'
        #
        # if master:
        #     games[master] = 'master'
        #
        # return games


class Table(Model):
    id = fields.IntField(pk=True)
    type = fields.CharField(32, default='start', index=True)
    donor1 = fields.OneToOneField('models.TelegramUser', related_name='game_donor1', null=True)
    donor2 = fields.OneToOneField('models.TelegramUser', related_name='game_donor2', null=True)
    donor3 = fields.OneToOneField('models.TelegramUser', related_name='game_donor3', null=True)
    donor4 = fields.OneToOneField('models.TelegramUser', related_name='game_donor4', null=True)
    donor5 = fields.OneToOneField('models.TelegramUser', related_name='game_donor5', null=True)
    donor6 = fields.OneToOneField('models.TelegramUser', related_name='game_donor6', null=True)
    donor7 = fields.OneToOneField('models.TelegramUser', related_name='game_donor7', null=True)
    donor8 = fields.OneToOneField('models.TelegramUser', related_name='game_donor8', null=True)

    partner1 = fields.OneToOneField('models.TelegramUser', related_name='game_partner1', null=True)
    partner2 = fields.OneToOneField('models.TelegramUser', related_name='game_partner2', null=True)
    partner3 = fields.OneToOneField('models.TelegramUser', related_name='game_partner3', null=True)
    partner4 = fields.OneToOneField('models.TelegramUser', related_name='game_partner4', null=True)

    mentor1 = fields.OneToOneField('models.TelegramUser', related_name='game_mentor1', null=True)
    mentor2 = fields.OneToOneField('models.TelegramUser', related_name='game_mentor2', null=True)

    master = fields.OneToOneField('models.TelegramUser', related_name='game_master', null=True)

    donor1_time = fields.IntField(null=True, index=True)
    donor2_time = fields.IntField(null=True, index=True)
    donor3_time = fields.IntField(null=True, index=True)
    donor5_time = fields.IntField(null=True, index=True)
    donor6_time = fields.IntField(null=True, index=True)
    donor7_time = fields.IntField(null=True, index=True)
    donor8_time = fields.IntField(null=True, index=True)

    donor1_notify = fields.BooleanField(default=False)
    donor2_notify = fields.BooleanField(default=False)
    donor3_notify = fields.BooleanField(default=False)
    donor4_notify = fields.BooleanField(default=False)
    donor5_notify = fields.BooleanField(default=False)
    donor6_notify = fields.BooleanField(default=False)
    donor7_notify = fields.BooleanField(default=False)
    donor8_notify = fields.BooleanField(default=False)

    donor_1_mentor1 = fields.BooleanField(default=False)
    donor_1_mentor2 = fields.BooleanField(default=False)
    donor_1_master = fields.BooleanField(default=False)

    donor_2_mentor1 = fields.BooleanField(default=False)
    donor_2_mentor2 = fields.BooleanField(default=False)
    donor_2_master = fields.BooleanField(default=False)

    donor_3_mentor1 = fields.BooleanField(default=False)
    donor_3_mentor2 = fields.BooleanField(default=False)
    donor_3_master = fields.BooleanField(default=False)

    donor_4_mentor1 = fields.BooleanField(default=False)
    donor_4_mentor2 = fields.BooleanField(default=False)
    donor_4_master = fields.BooleanField(default=False)

    donor_5_mentor1 = fields.BooleanField(default=False)
    donor_5_mentor2 = fields.BooleanField(default=False)
    donor_5_master = fields.BooleanField(default=False)

    donor_6_mentor1 = fields.BooleanField(default=False)
    donor_6_mentor2 = fields.BooleanField(default=False)
    donor_6_master = fields.BooleanField(default=False)

    donor_7_mentor1 = fields.BooleanField(default=False)
    donor_7_mentor2 = fields.BooleanField(default=False)
    donor_7_master = fields.BooleanField(default=False)

    donor_8_mentor1 = fields.BooleanField(default=False)
    donor_8_mentor2 = fields.BooleanField(default=False)
    donor_8_master = fields.BooleanField(default=False)

    async def add_donor(self, user: TelegramUser):
        for i in range(1, 8):
            if await getattr(self, f'donor{i}') is None:
                setattr(self, f'donor{i}', user)
                shift = (await Config.get(id=1)).delete_time * 3600
                block_time = time.time() + shift
                setattr(self, f'donor{i}', user)
                setattr(self, f'donor{i}_time', block_time)
                await self.save()

    async def remove_donor(self, user: TelegramUser):
        for i in range(1, 8):
            if await getattr(self, f'donor{i}') == user:
                setattr(self, f'donor{i}', None)
                await self.save()

    def donor_valid(self, donor_num: int):
        if not (1 <= donor_num <= 8):
            return False

        if self.type == 'start':
            return getattr(self, f'donor_{donor_num}_master')

        partner_valid = getattr(self, f'donor_{donor_num}_mentor1')
        mentor_valid = getattr(self, f'donor_{donor_num}_mentor2')
        master_valid = getattr(self, f'donor_{donor_num}_master')

        return partner_valid and mentor_valid and master_valid

    async def users(self, list_=False):
        users = {
            'donors': (
                await self.donor1,
                await self.donor2,
                await self.donor3,
                await self.donor4,
                await self.donor5,
                await self.donor6,
                await self.donor7,
                await self.donor8,
            ),
            'partners': (
                await self.partner1,
                await self.partner2,
                await self.partner3,
                await self.partner4,
            ),
            'mentors': (
                await self.mentor1,
                await self.mentor2,
            ),
            'master': [await self.master] if list_ else await self.master
        }
        return users

    # @property
    async def is_full(self):
        if self.type == 'start':
            if await self.donor1 and await self.donor2 and await self.donor3 and await self.donor4:
                return True
            else:
                return False
        else:
            if (await self.donor1 and await self.donor2 and await self.donor3 and await self.donor4 and
                    await self.donor5 and await self.donor6 and await self.donor7 and await self.donor8):
                return True
            else:
                return False

    @property
    async def not_full(self):
        if self.type == 'start':
            if not await self.donor1 or not await self.donor2 or not await self.donor3 or not await self.donor4:
                return True
            else:
                return False
        else:
            if (not await self.donor1 or not await self.donor2 or not await self.donor3 or not await self.donor4 or
                    not await self.donor5 or not await self.donor6 or not await self.donor7 or not await self.donor8):
                return True
            else:
                return False

    # def donor_count(self):
    #     return len([await getattr(self, f'donor{i}') for i in range(1, 8) if await getattr(self, f'donor{i}')])


class Message(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(64, unique=True, index=True)
    text = fields.TextField()

    @classmethod
    async def from_name(cls, name):
        return (await cls.get_or_none(name=name)).text


class Button(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(64, unique=True, index=True)
    text = fields.CharField(128)

    @classmethod
    async def from_name(cls, name):
        return (await cls.get_or_none(name=name)).text


class Config(Model):
    id = fields.IntField(pk=True)
    support_url = fields.CharField(128)
    pdf = fields.CharField(256)
    about_photo = fields.CharField(256)
    channel = fields.CharField(128)
    chat = fields.CharField(128)
    keys_system = fields.BooleanField(default=True)
    delete_time = fields.IntField()
    block_time = fields.IntField()


class TablePrice(Model):
    id = fields.IntField(pk=True)
    start = fields.IntField()
    wood = fields.IntField()
    bronze = fields.IntField()
    silver = fields.IntField()
    gold = fields.IntField()
    platinum = fields.IntField()
    legendary = fields.IntField()


class User(Model, UserMixin):
    id = fields.IntField(pk=True)
    email = fields.CharField(254, unique=True)
    password = fields.CharField(255)
    active = fields.BooleanField()
    roles = fields.ManyToManyField(
        'models.Role', related_name='users', through='roles_users'
    )


class Role(Model, RoleMixin):
    id = fields.IntField(pk=True)
    name = fields.CharField(100, unique=True)
    description = fields.CharField(255)


get_message = Message.from_name
get_button = Button.from_name
