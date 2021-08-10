# This example show how to write an inline mode telegram bot use pyTelegramBotAPI.
import logging
import sys
import time
import re

import config

import telebot
from telebot import types

API_TOKEN = config.API_TOKEN

bot = telebot.TeleBot(API_TOKEN)
telebot.logger.setLevel(logging.DEBUG)


@bot.inline_handler(lambda query: len(query.query) != 0)
def query_text(inline_query):
    answers = {
        '1': 'Исправить текст чуть-чуть.',
        '2': 'Полное погружение!',
    }

    try:

        r1 = types.InlineQueryResultArticle('1', answers['1'], types.InputTextMessageContent(
            some_less_wrong(inline_query.query)
        ))
        r2 = types.InlineQueryResultArticle('2', answers['2'], types.InputTextMessageContent(
            more_less_wrong(inline_query.query)
        ))

        bot.answer_inline_query(inline_query.id, [r1, r2])
    except Exception as e:
        print(e)


@bot.inline_handler(lambda query: len(query.query) == 0)
def default_query(inline_query):
    try:
        answers = {
            '1': ['Пустой запрос', 'Тут нет текста, зачем жмешь?!']
        }

        r = types.InlineQueryResultArticle('1', answers['1'][0], types.InputTextMessageContent(answers['1'][1]))
        bot.answer_inline_query(inline_query.id, [r])
    except Exception as e:
        print(e)


def some_less_wrong(data: str):
    _data = re.sub(r'[^\s\w]', '', data)
    return _data.lower()


def more_less_wrong(data: str):
    _data = re.sub(r'\W', '', data)
    return _data.lower()


def main_loop():
    bot.polling(True)
    while 1:
        time.sleep(3)


if __name__ == '__main__':
    try:
        main_loop()
    except KeyboardInterrupt:
        print('\nExiting by user request.\n')
        sys.exit(0)
