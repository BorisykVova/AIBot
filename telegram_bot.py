from telegram import Update
from telegram.ext import (Updater, CommandHandler, CallbackContext,
                          MessageHandler, ConversationHandler)
from telegram.ext.filters import Filters

import user_crud
from aibot import AIBot
from settings import TOKEN

CHANGE_TOPIC = 1


def hello(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f'Hello {update.effective_user.first_name}')


def get_bot_response(update: Update, context: CallbackContext) -> None:
    user = user_crud.get_or_create(update.effective_user.id)
    bot = AIBot(user.current_topic)
    user_input = update.message.text
    update.message.reply_text(bot.generate_response(user_input))


def start_change_topic(update: Update, context: CallbackContext):
    update.message.reply_text('Enter new topic:')
    return CHANGE_TOPIC


def change_topic(update: Update, context: CallbackContext):
    topic = update.message.text
    user = user_crud.get_or_create(update.effective_user.id, topic)
    user_updated = user_crud.update(user.id, topic)
    update.message.reply_text(f'Topic has been changed to {user_updated.current_topic!r}')
    return ConversationHandler.END

def cancel(update: Update, context: CallbackContext):
    update.message.reply_text('Good bye')
    return ConversationHandler.END

def get_topic(update: Update, context: CallbackContext):
    user = user_crud.get_or_create(update.effective_user.id)
    update.message.reply_text(f'We are talking about {user.current_topic!r}')


updater = Updater(TOKEN)


conv_handler = ConversationHandler(
    entry_points=[CommandHandler('change_topic', start_change_topic)],
    states={
        CHANGE_TOPIC: [CommandHandler('cancel', cancel), MessageHandler(Filters.text, change_topic)]
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)


updater.dispatcher.add_handler(CommandHandler('hello', hello))
updater.dispatcher.add_handler(CommandHandler('topic', get_topic))
updater.dispatcher.add_handler(conv_handler)
updater.dispatcher.add_handler(MessageHandler(Filters.text, get_bot_response))


if __name__ == '__main__':
    updater.start_polling()
    updater.idle()
