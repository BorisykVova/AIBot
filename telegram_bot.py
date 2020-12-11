import random

from telegram import Update
from telegram.ext import (Updater, CommandHandler, CallbackContext,
                          MessageHandler, ConversationHandler)
from telegram.ext.filters import Filters

import logger
import user_crud
from aibot import AIBot
from settings import TOKEN

CHANGE_TOPIC = 1

log = logger.get_logger('Telegram')


GREETINGS = [
    'hi',
    'hello',
    'hey',
]


def is_greeting(user_input: str) -> bool:
    for word in user_input.split():
        if word in GREETINGS:
            return True
    return False


def hello(update: Update, context: CallbackContext) -> None:
    user_name = update.effective_user.first_name
    log.debug(f"User {user_name} sent command '/hello'.")
    update.message.reply_text(f'Hello {user_name}. I can answer to your question.\n'
                              f'Use command /change_topic to change topic. For example: tennis, economics, music ...')


def get_bot_response(update: Update, context: CallbackContext) -> None:
    user_input = update.message.text

    if is_greeting(user_input):
        update.message.reply_text(f'{random.choice(GREETINGS)} {update.effective_user.first_name}')
        return

    log.debug(f'User {update.effective_user.first_name} asked question.')
    user = user_crud.get_or_create(update.effective_user.id)
    bot = AIBot(user.current_topic)
    update.message.reply_text(bot.generate_response(user_input))


def start_change_topic(update: Update, context: CallbackContext):
    update.message.reply_text('About what do you want to talk?')
    return CHANGE_TOPIC


def change_topic(update: Update, context: CallbackContext):
    topic = update.message.text
    user = user_crud.get_or_create(update.effective_user.id, topic)
    user_updated = user_crud.update(user.id, topic)
    update.message.reply_text(f'Ok, lets talk about {user_updated.current_topic!r}')
    log.debug(f'User {update.effective_user.first_name!r} changed topic to : {user_updated.current_topic!r}.')
    return ConversationHandler.END

def cancel(update: Update, context: CallbackContext):
    update.message.reply_text('Good bye')
    log.debug(f'User {update.effective_user.first_name!r} canceled an action.')
    return ConversationHandler.END

def get_topic(update: Update, context: CallbackContext):
    user = user_crud.get_or_create(update.effective_user.id)
    update.message.reply_text(f'We are talking about {user.current_topic!r}')
    log.debug(f'User {update.effective_user.first_name!r} got current topic.')


updater = Updater(TOKEN)


conv_handler = ConversationHandler(
    entry_points=[CommandHandler('change_topic', start_change_topic)],
    states={
        CHANGE_TOPIC: [CommandHandler('cancel', cancel), MessageHandler(Filters.text, change_topic)]
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)


updater.dispatcher.add_handler(CommandHandler('hello', hello))
updater.dispatcher.add_handler(CommandHandler('start', hello))
updater.dispatcher.add_handler(CommandHandler('topic', get_topic))
updater.dispatcher.add_handler(conv_handler)
updater.dispatcher.add_handler(MessageHandler(Filters.text, get_bot_response))


if __name__ == '__main__':
    logger.logger_configure(level='DEBUG', root_level='WARNING')

    log.info('Bot has been stated...\n Press Ctr+C to STOP the bot.')
    updater.start_polling()
    updater.idle()
    log.info('Bot has been stopped.')
