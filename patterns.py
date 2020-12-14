from enum import Enum

class ButtonText(Enum):
    HELLO = 'Hello 🤚'
    TOPIC = 'Current Topic ℹ️'
    CHANGE = 'Change topic 🔄'
    CANCEL = 'Cancel 🔴'


class ButtonPattern(Enum):
    HELLO = f'^{ButtonText.HELLO.value}$'
    TOPIC = f'^{ButtonText.TOPIC.value}$'
    CHANGE = f'^{ButtonText.CHANGE.value}$'
    CANCEL = f'^{ButtonText.CANCEL.value}$'
