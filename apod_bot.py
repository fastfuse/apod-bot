import json
import logging

import redis as r
import requests
from telegram import ParseMode

# Enable logging
import config

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

redis = r.from_url(config.REDIS_URL)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start_handler(bot, update):
    """
    Send a message when the command /start is issued.
    """
    chat_id = update.message.chat_id

    logger.info(f"Start command received. Chat ID: {chat_id}")

    update.message.reply_text(config.START_MESSAGE)

    chat_ids = redis.get('chat_ids')

    if chat_ids is None:
        chat_ids = list()

    else:
        chat_ids = json.loads(chat_ids)

    chat_ids.append(chat_id)

    # redis.set('chat_ids', chat_ids)
    redis.set('chat_ids', list(set(chat_ids)))


def help_handler(bot, update):
    """
    Send a message when the command /help is issued.
    """
    logger.info(f"Help command received. Chat ID: {update.message.chat_id}")
    update.message.reply_text(config.HELP_MESSAGE)


def echo_handler(bot, update):
    """Echo the user message."""
    chat_id = update.message.chat_id

    apod_data = requests.get(config.APOD_API_URL).json()
    title = apod_data['title']

    logger.info(f"Sending message to chat: {chat_id}")

    if apod_data["media_type"] == "video":
        bot.send_message(chat_id=chat_id,
                         text=f'<a href="{config.APOD_URL}">{title}</a>',
                         parse_mode=ParseMode.HTML)

        # bot.send_video(chat_id=chat_id,
        #                video=apod_data['url'],
        #                parse_mode=ParseMode.HTML)

    else:
        bot.send_photo(chat_id=chat_id,
                       photo=apod_data['url'],
                       caption=f'<a href="{config.APOD_URL}">{title}</a>',
                       parse_mode=ParseMode.HTML)


def send_apod(bot, job):
    """
    Function to get NASA APOD and send to subscribed users.
    """
    apod_data = requests.get(config.APOD_API_URL).json()

    title = apod_data['title']

    chat_ids = json.loads(redis.get('chat_ids'))

    for chat_id in chat_ids:
        logger.info(f"Sending message to chat: {chat_id}")

        if apod_data["media_type"] == "video":
            bot.send_message(chat_id=chat_id,
                             text=f'<a href="{config.APOD_URL}">{title}</a>',
                             parse_mode=ParseMode.HTML)

        else:
            bot.send_photo(chat_id=chat_id,
                           photo=apod_data['url'],
                           caption=f'<a href="{config.APOD_URL}">{title}</a>',
                           parse_mode=ParseMode.HTML)


def error_cb(bot, update, error):
    """
    Log Errors caused by Updates.
    """
    logger.error(f"Update {update} caused error {error}")
