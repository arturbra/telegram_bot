#!/usr/bin/env python
# pylint: disable=C0116
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to send timed Telegram messages.
This Bot uses the Updater class to handle the bot and the JobQueue to send
timed messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Alarm Bot example, sends a message after a set time.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update: Update, _: CallbackContext) -> None:
    """Sends explanation on how to use the bot."""
    update.message.reply_text('Olá Lyoner, este bot está a sua disposição para avisar se a máquina e a secadora estão '
                              'desocupadas. Para aprender os comandos, digite /help')

def help(update: Update, _: CallbackContext) -> None:
    """Sends explanation about the commands."""
    pass

def alarm(context: CallbackContext) -> None:
    """Send the alarm message."""
    job = context.job
    context.bot.send_message(job.context, text='A máquina de lavar roupas acabou de acabar.')

# def remove_job_if_exists(name: str, context: CallbackContext) -> bool:
#     """Remove job with given name. Returns whether job was removed."""
#     current_jobs = context.job_queue.get_jobs_by_name(name)
#     if not current_jobs:
#         return False
#     for job in current_jobs:
#         job.schedule_removal()
#     return True


def set_timer(update: Update, context: CallbackContext) -> None:
    """Add a job to the queue."""
    chat_id = update.message.chat_id
    try:
        # args[0] should contain the time for the timer in seconds

        time = args[0].split(":")
        time_seconds = (int(time[0]) * 3600) + (int(time[1]) * 60)
        job_removed = remove_job_if_exists(str(chat_id), context)
        context.job_queue.run_once(alarm, time_seconds, context=chat_id, name=str(chat_id))

        text = 'Timer definido com sucesso!'
        if job_removed:
            text += 'O tempo antigo foi removido'
        update.message.reply_text(text)

    except (IndexError, ValueError):
        update.message.reply_text('Use /set <horas:minutos> para definir o alarme. Ex: /set 3:40 vai definir o alarme '
                                  'para 3 horas e 40 minutos')


def unset(update: Update, context: CallbackContext) -> None:
    """Remove the job if the user changed their mind."""
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = 'Timer successfully cancelled!' if job_removed else 'You have no active timer.'
    update.message.reply_text(text)


def main() -> None:
    """Run bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("insert the telegram bot key here")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", start))
    dispatcher.add_handler(CommandHandler("set_maquina", set_timer))
    dispatcher.add_handler(CommandHandler("unset_maquina", unset))

    # Start the Bot
    updater.start_polling()

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()