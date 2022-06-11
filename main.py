import time
import datetime

import schedule
from dotenv import load_dotenv

import attr_parser_selenium
import db
import telegram_bot


def every_week_work():
    # Find date week ago.
    date = datetime.datetime.today() - datetime.timedelta(7)
    today = datetime.datetime.today()
    date_from = f'{date.day :02d}.{date.month:02d}.{date.year}'
    date_to = f'{today.day:02d}.{today.month:02d}.{today.year}'
    # Get courts decisions for week
    parser = attr_parser_selenium.sudrf_parser(date_from=date_from, date_for=date_to)
    parser_result = parser.all_parse_response()
    # Add data to database
    data_base = db.data_base()
    data_base.write_to_database(parser_result)
    # Send message to telegram bot
    message = []
    for court_name in parser_result:
        if parser_result[court_name]:
            for row in parser_result[court_name]:
                date_adoption = row[1]
                full_name, article = row[2].split('-')
                message.append(f'{parser.title_dict.get(court_name)}: {full_name}, {article}, дата: {date_adoption}.')
        else:
            continue
    message.insert(0, 'Данные по административным делам за прошедшую неделю:')
    message = '\n'.join(message)
    bot = telegram_bot.bot()
    bot.send_message(message)


if __name__ == "__main__":
    load_dotenv()
    schedule.every().saturday.do(every_week_work)

    while True:
        schedule.run_pending()
        time.sleep(1)
