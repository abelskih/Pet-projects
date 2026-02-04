KEY_MODE = "mode"
KEY_DIALOG_LIST = "dialog_list"
KEY_USER_DATE = "user_date"
KEY_DATE_PROFILE = "date_profile"

MODE_MAIN = "main"
MODE_PROFILE = "profile"
MODE_OPENER = "opener"
MODE_MESSAGE = "message"
MODE_DATE = "date"
MODE_GPT = "gpt"

FORM_STEPS = [
    ("age", "Сколько тебе лет?"),
    ("occupation", "Где ты работаешь?"),
    ("hobby", "У вас есть хобби?"),
    ("annoys", "Что вам НЕ нравиться в людях?"),
    ("goals", "Цели знакомства?")
]
FORM_QUESTIONS = dict(FORM_STEPS)

FORM_STEPS_OPENER = [
    ("name", "Назовите имя собеседника?"),
    ("age", "Сколько ему лет?"),
    ("handsome", "Оцените внешность: 1-10 баллов?"),
    ("occupation", "Кем работает?"),
    ("goals", "Цель знакомства?")
]
FORM_QUESTIONS_OPENER = dict(FORM_STEPS_OPENER)