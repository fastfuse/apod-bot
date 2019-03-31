import datetime
import logging

import peewee
import requests
from telegram import ParseMode

import config

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

db = peewee.SqliteDatabase('subscriptions.sqlite3')


class Subscriber(peewee.Model):
    class Meta:
        database = db

    chat_id = peewee.CharField()
    subscribed_on = peewee.DateTimeField(default=datetime.datetime.now)


# Define a few command handlers.
# These usually take the two arguments bot and update.
# Error handlers also receive the raised TelegramError object in error.

def start_handler(bot, update):
    """
    Send a message when the command '/start' is issued.
    """
    chat_id = update.message.chat_id

    logger.info(f"Start command received. Chat ID: {chat_id}")

    update.message.reply_text(config.START_MESSAGE)

    try:
        Subscriber.get(Subscriber.chat_id == chat_id)

    except peewee.DoesNotExist:
        logger.info(f"Storing new subscriber {chat_id} to DB")
        Subscriber(chat_id=chat_id).save()


def help_handler(bot, update):
    """
    Send a message when the command /help is issued.
    """
    logger.info(f"Help command received. Chat ID: {update.message.chat_id}")
    update.message.reply_text(config.HELP_MESSAGE)


def ping_handler(bot, update):
    """
    Ping command
    """
    logger.info(f"Ping command received. Chat ID: {update.message.chat_id}")

    update.message.reply_text("Pong")


def echo_handler(bot, update):
    """
    Reply to messages
    """
    logger.info(f"Text received. Chat ID: {update.message.chat_id}")

    update.message.reply_text("I can't chat...")


def send_apod(bot, job):
    """
    Function to get NASA APOD and send to subscribed users.
    """
    apod_data = requests.get(config.APOD_API_URL).json()

    title = apod_data['title']

    for subscriber in Subscriber.select():
        chat_id = subscriber.chat_id
        logger.info(f"Sending message to chat: {chat_id}")

        if apod_data["media_type"] == "video":
            bot.send_message(chat_id=chat_id,
                             text=apod_data['url'],
                             parse_mode=ParseMode.HTML)

        else:
            bot.send_photo(chat_id=chat_id,
                           photo=apod_data['hdurl'],
                           caption=f'<a href="{config.APOD_URL}">{title}</a>',
                           parse_mode=ParseMode.HTML)


def error_cb(bot, update, error):
    """
    Log Errors caused by Updates.
    """
    logger.error(f"Update {update} caused error {error}")
