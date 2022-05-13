import asyncio
import time
import traceback

from db.models import Table, Config, get_message, get_button
from loader import bot


async def send_message(donor, field, now, block_time):
    setattr(donor, f'{field.type}_block', now + block_time)
    await donor.save()
    await bot.send_message(
        donor.telegram_id,
        (await get_message('you_excluded')).format(
            type=await get_button(f'{field.type}_name')
        )
    )


async def blocker():
    while True:
        try:
            now = time.time()
            block_time = (await Config.get(id=1)).block_time * 3600

            to_block = await Table.filter(donor1_time__lte=now).all()
            for field in to_block:
                donor = (await field.donor1)
                if not donor:
                    field.donor1_time = None
                    await field.save()
                    continue
                field.donor1 = None
                await field.save()
                await send_message(donor, field, now, block_time)

            to_block = await Table.filter(donor2_time__lte=now).all()
            for field in to_block:
                donor = (await field.donor2)
                if not donor:
                    field.donor2_time = None
                    await field.save()
                    continue
                field.donor2 = None
                await field.save()
                await send_message(donor, field, now, block_time)

            to_block = await Table.filter(donor3_time__lte=now).all()
            for field in to_block:
                donor = (await field.donor3)
                if not donor:
                    field.donor3_time = None
                    await field.save()
                    continue
                field.donor3 = None
                await field.save()
                await send_message(donor, field, now, block_time)

            to_block = await Table.filter(donor4_time__lte=now).all()
            for field in to_block:
                donor = (await field.donor4)
                if not donor:
                    field.donor4_time = None
                    await field.save()
                    continue
                field.donor4 = None
                await field.save()
                await send_message(donor, field, now, block_time)

            to_block = await Table.filter(donor5_time__lte=now).all()
            for field in to_block:
                donor = (await field.donor5)
                if not donor:
                    field.donor5_time = None
                    await field.save()
                    continue
                field.donor5 = None
                await field.save()
                await send_message(donor, field, now, block_time)

            to_block = await Table.filter(donor6_time__lte=now).all()
            for field in to_block:
                donor = (await field.donor6)
                if not donor:
                    field.donor6_time = None
                    await field.save()
                    continue
                field.donor6 = None
                await field.save()
                await send_message(donor, field, now, block_time)

            to_block = await Table.filter(donor7_time__lte=now).all()
            for field in to_block:
                donor = (await field.donor7)
                if not donor:
                    field.donor7_time = None
                    await field.save()
                    continue
                field.donor7 = None
                await field.save()
                await send_message(donor, field, now, block_time)

            to_block = await Table.filter(donor8_time__lte=now).all()
            for field in to_block:
                donor = (await field.donor8)
                if not donor:
                    field.donor8_time = None
                    await field.save()
                    continue
                field.donor8 = None
                await field.save()
                await send_message(donor, field, now, block_time)

            await asyncio.sleep(3600)

        except Exception as e:
            print(traceback.format_exc())
            await asyncio.sleep(300)

