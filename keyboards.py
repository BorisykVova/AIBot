from patterns import ButtonText

from telegram import ReplyKeyboardMarkup, KeyboardButton


hello_button = KeyboardButton(ButtonText.HELLO.value)
get_topic_button = KeyboardButton(ButtonText.TOPIC.value)
change_topic_button = KeyboardButton(ButtonText.CHANGE.value)
cancel_button = KeyboardButton(ButtonText.CANCEL.value)


keyboard = ReplyKeyboardMarkup([
    [hello_button, get_topic_button],
    [change_topic_button],
])

keyboard_only_cancel = ReplyKeyboardMarkup([[cancel_button]])
