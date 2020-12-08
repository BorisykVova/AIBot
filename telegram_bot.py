from telegram import Update
from telegram.ext.filters import Filters
from telegram.ext import (Updater, CommandHandler, CallbackContext,
                          MessageHandler, ConversationHandler)

from aibot import AIBot

TOKEN = '1312220937:AAFfFoK2qDsoeyDEvSN3zK3RWOA20cQMdzY'
CHANGE_TOPIC = 1
DEFAULT_TOPIC = 'Tennis'

users_topics = {}


def hello(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f'Hello {update.effective_user.first_name}')


def get_bot_response(update: Update, context: CallbackContext) -> None:
    bot = users_topics.get(update.effective_user, AIBot(DEFAULT_TOPIC))
    user_input = update.message.text
    update.message.reply_text(bot.generate_response(user_input))


def start_change_topic(update: Update, context: CallbackContext):
    update.message.reply_text('Enter new topic:')
    return CHANGE_TOPIC


def change_topic(update: Update, context: CallbackContext):
    user = update.effective_user
    topic = update.message.text
    users_topics[user] = AIBot(topic)
    update.message.reply_text(f'Topic has been changed to {topic!r}')
    return ConversationHandler.END

def cancel(update: Update, context: CallbackContext):
    update.message.reply_text('Good bye')
    return ConversationHandler.END


updater = Updater(TOKEN)


conv_handler = ConversationHandler(
    entry_points=[CommandHandler('change_topic', start_change_topic)],
    states={
        CHANGE_TOPIC: [CommandHandler('cancel', cancel), MessageHandler(Filters.text, change_topic)]
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)


updater.dispatcher.add_handler(CommandHandler('hello', hello))
updater.dispatcher.add_handler(conv_handler)
updater.dispatcher.add_handler(MessageHandler(Filters.text, get_bot_response))


if __name__ == '__main__':
    updater.start_polling()
    updater.idle()
