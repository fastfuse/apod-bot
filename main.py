from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import apod_bot
import config


def main():
    """
    Main loop function to start the bot.
    """
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(config.TOKEN)
    job_queue = updater.job_queue

    job_queue.run_repeating(apod_bot.send_apod, interval=30)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", apod_bot.start_handler))
    dp.add_handler(CommandHandler("help", apod_bot.help_handler))

    # on non-command i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, apod_bot.echo_handler))

    # log all errors
    dp.add_error_handler(apod_bot.error_cb)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
