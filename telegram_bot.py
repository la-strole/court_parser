import os
import logging
import sqlite3
from sqlite3 import Error

import telebot


class bot:
    def __init__(self):
        # Add Telegram bot.
        bot_token = os.environ.get('bot_TOKEN')
        self.bot = telebot.TeleBot(bot_token, parse_mode=None)

        # Add logger.
        self.logger_telebot = logging.getLogger('telebot')
        f_handler = logging.FileHandler('file.log')
        f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        f_handler.setFormatter(f_format)
        self.logger_telebot.addHandler(f_handler)

    def send_message(self, message):
        """ Connect to database to get chat ids and send message with environment variables.

        """

        try:
            with sqlite3.connect(f'{os.environ.get("db_path")}/{os.environ.get("isalive_bot_database")}') \
                    as con:
                con.row_factory = sqlite3.Row
                rows = con.execute("SELECT * FROM users")
                result = [dict(row) for row in rows.fetchall()]
        except Error as e:
            self.logger_telebot.exception(f"Can not get users. {e}")
            return None

        for user in result:
            try:
                self.bot.send_message(user.get('chat_id'), message)
            except Exception as e:
                self.logger_telebot.exception(f'{e}')
                return None



