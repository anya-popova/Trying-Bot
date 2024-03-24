import telebot
# import sqlite3
# from telebot import types
from telebot import custom_filters
from telebot import StateMemoryStorage
from telebot.handler_backends import StatesGroup, State

# import sqlite3 as sq

# connection = sq.connect('database.db')


state_storage = StateMemoryStorage()
bot = telebot.TeleBot("",
                      state_storage=state_storage, parse_mode='Markdown')


class PollState(StatesGroup):
    name = State()
    love_cats = State()


class HelpState(StatesGroup):
    wait_text = State()


text_poll = "Давай поболтаем"
text_button_1 = "Практический курс"
text_button_2 = "Стоит посмотреть"
text_button_3 = "котек"

menu_keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_poll,
    )
)
menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_button_1,
    )
)

menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_button_2,
    ),
    telebot.types.KeyboardButton(
        text_button_3,
    )
)

privetstvie = ['привет', 'hello', 'hi', 'здравствуй', 'здравствуйте', 'начать']

# картинки для отправки пользователю
start_photo = open('./first_picture.jpg', 'rb')
cat_photo = open('./cat_photo.jpg', 'rb')
dog_photo = open('./dog_photo.jpg', 'rb')


# @bot.message_handler(commands=['start'])
# def startt(message):
#     conn = sqlite3.connect('trying.sql')
#     cur = conn.cursor()
#
#     cur.execute('CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, name varchar(50), pass varchar('
#                 '50)')
#     conn.commit()
#     cur.close()
#     conn.close()
#
#     bot.send_message(message.chat.id, 'Доброго времени суток! Введите своё имя')
#     bot.register_next_step_handler(message, user_name)


# приветсвие в ответ на приветствие пользователя
@bot.message_handler(state="*", commands=['start', 'hi', 'hello'])
def start(message):
    bot.send_message(
        message.chat.id,
        f'Привет, {message.from_user.first_name}!\nХорошего дня^^',  # приветствие
        reply_markup=menu_keyboard)
    bot.send_photo(
        message.chat.id,
        start_photo)


# если пользователь отправил фото, бот реагирует^^
@bot.message_handler(content_types=['photo'])
def get_photo(message, markup=None):
    bot.reply_to(message, 'О! Картинка)', reply_markup=markup)


@bot.message_handler(commands=['cat'])
def main(message):
    bot.send_message(
        message.chat.id,
        '[на Вас похож](https://ru.pinterest.com/pin/24769866693847486/)')  # картинка из Pinterest


@bot.message_handler(commands=['dog'])
def main(message):
    bot.send_message(
        message.chat.id,
        '*гав*')
    bot.send_photo(
        message.chat.id,
        dog_photo)


# пользователь грустит, отправляем ссылку на котиков в пинтерест
@bot.message_handler(commands=['sad'])
def main(message):
    bot.send_message(
        message.chat.id,
        '[тык](https://ru.pinterest.com/search/pins/?q=cat%20meme&rs=typed)')


# пользователь нажал на кнопку, чтобы поболтать, задаём 2 вопроса
@bot.message_handler(func=lambda message: text_poll == message.text)
def first(message):
    bot.send_message(message.chat.id, 'Как *Ваше* _имя_?')  # узнать имя
    bot.set_state(message.from_user.id, PollState.name, message.chat.id)


@bot.message_handler(state=PollState.name)
def name(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['name'] = message.text
    bot.send_message(message.chat.id,
                     f'nice to meet you <3\n {message.text}, на сколько вы любите котиков по шкале от 1 до 10?')
    bot.set_state(message.from_user.id, PollState.love_cats, message.chat.id)


@bot.message_handler(state=PollState.love_cats)
def age(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['love_cats'] = message.text
    bot.send_message(message.chat.id, 'Спасибо за ответ!\n Хорошего дня!',
                     reply_markup=menu_keyboard)  # реакция на ответ
    bot.delete_state(message.from_user.id, message.chat.id)


# кнопка, которая вызывает ссылку на практический курс
@bot.message_handler(func=lambda message: text_button_1 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, '[тык](https://opd.spbstu.ru/course/view.php?id=3346)')


# кнопка, которая вызывает ссылку на полезный видеоурок по созданию ботов
@bot.message_handler(func=lambda message: text_button_2 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, '[тык](https://www.youtube.com/playlist?list=PL0lO_mIqDDFUev1gp9yEwmwcy8SicqKbt'
                                      '&si=PMqSlBgEmVSUAXYE)')


# конопка, по которой пользователю отправляется картинка с котом
@bot.message_handler(func=lambda message: text_button_3 == message.text)
def help_command(message):
    bot.send_photo(
        message.chat.id,
        cat_photo)


# пользователь написал приветствие, которое не является предлагаемой командой
# приветствуем пользователя по нику
@bot.message_handler()
def info(message):
    if message.text.lower() in privetstvie:
        bot.send_message(
            message.chat.id,
            f'Привет, {message.from_user.first_name} ^^',  # приветствие
            reply_markup=menu_keyboard)


bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.TextMatchFilter())

bot.infinity_polling()
