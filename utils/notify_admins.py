import logging

from aiogram import Dispatcher

from utils.config import ADMINS


async def on_startup_notify(dp: Dispatcher):
    for admin in ADMINS:
        try:
            await dp.bot.send_message(admin, "Привіт, я бот вікіпедія. Пиши мені слово наприклад 'Python' і я знайду інформацію про нього🧐🧠🤓\n"
                                             "Що тебе цікавить?")

        except Exception as err:
            logging.exception(err)
