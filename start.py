import telebot
from telebot import custom_filters
from telebot import StateMemoryStorage
from telebot.handler_backends import StatesGroup, State


state_storage = StateMemoryStorage()
bot = telebot.TeleBot("",
                      state_storage=state_storage, parse_mode='Markdown')


class PollState(StatesGroup):
    name = State()
    love_cats = State()


class HelpState(StatesGroup):
    wait_text = State()


# список станций
text_button_1 = "Станция 1"
text_button_2 = "Станция 2"
text_button_3 = "Станция 3"
text_button_4 = "Станция 4"
text_button_5 = "Станция 5"
text_button_6 = "Станция 6"
text_button_7 = "Станция 7"

menu_keyboard_stations = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
menu_keyboard_stations.add(
    telebot.types.KeyboardButton(
        text_button_1,
    ),
    telebot.types.KeyboardButton(
        text_button_2,
    )
)

menu_keyboard_stations.add(
    telebot.types.KeyboardButton(
        text_button_3,
    ),
    telebot.types.KeyboardButton(
        text_button_4,
    )
)

menu_keyboard_stations.add(
    telebot.types.KeyboardButton(
        text_button_5,
    ),
    telebot.types.KeyboardButton(
        text_button_6,
    ),
    telebot.types.KeyboardButton(
        text_button_7,
    )
)

text_button_edit_data_yes = "Да, изменить название"
text_button_edit_data_no = "Нет, не изменять название"

menu_keyboard_edit_data = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
menu_keyboard_edit_data.add(
    telebot.types.KeyboardButton(
        text_button_edit_data_yes,
    )
)

menu_keyboard_edit_data.add(
    telebot.types.KeyboardButton(
        text_button_edit_data_no,
    )
)


@bot.message_handler(state="*", commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        f'Привет, {message.from_user.first_name}!\nХорошего дня^^',  # приветствие
        )


@bot.message_handler(commands=['edit_data'])
def main(message):
    bot.send_message(
        message.chat.id,
        'Изменить название команды?',
        reply_markup=menu_keyboard_edit_data)


@bot.message_handler(commands=['info'])
def main(message):
    bot.send_message(
        message.chat.id,
        'Информация о боте',   # Расписать информацию о боте
        )


@bot.message_handler(commands=['stations'])
def main(message):
    bot.send_message(
        message.chat.id,
        'Выберете станцию:',
        reply_markup=menu_keyboard_stations)


@bot.message_handler(commands=['scores'])
def main(message):
    bot.send_message(
        message.chat.id,
        'Текущие оценки:',   # Расписать + база данных
        )


@bot.message_handler()
def info(message):
    if message.text.lower() in ['да, изменить название']:
        bot.send_message(
            message.chat.id,
            'Введите новое название команды:',  # база данных
        )
        if message.text.lower() in ['нет, не изменять название']:
            bot.send_message(
                message.chat.id,
                'отмена',  # хз, нужно будет поменять
            )


bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.TextMatchFilter())

bot.infinity_polling()
