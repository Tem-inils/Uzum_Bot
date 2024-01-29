import telebot.types
from database import Database

data = Database()


def menu_btn():
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

    btn1 = telebot.types.KeyboardButton(text='Добавить контакт 👤')
    btn2 = telebot.types.KeyboardButton(text='Удалить контакты ⛔️')
    btn3 = telebot.types.KeyboardButton(text='Обновить ссылку 🆕')
    btn4 = telebot.types.KeyboardButton(text='Получить весь список контактов 👥')
    btn5 = telebot.types.KeyboardButton(text='Разослать новую ссылку 🖇️')

    markup.add(btn1, btn2, btn3, btn4)
    markup.row(btn5)

    return markup


def user_menu():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)

    btn1 = telebot.types.InlineKeyboardButton(text='Получить ссылку на урок 🖇️')

    markup.add(btn1)

    return markup


def get_user_contact():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)

    btn1 = telebot.types.KeyboardButton(text='Отправить контакт 📞', request_contact=True)

    markup.add(btn1)

    return markup


def get_lesson_link():
    try:
        link = data.get_link()[0][0]

        markup = telebot.types.InlineKeyboardMarkup()

        btn1 = telebot.types.InlineKeyboardButton(text='Ссылка 🖇️', url=str(link))

        markup.add(btn1)

        return markup
    except Exception as e:
        print(e)
        pass


def get_contact_btn():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)

    contacts = data.get_all_contact()

    markup.row('Назад 🔙')
    markup.row('Удалить все 🫂')

    for i in range(0, len(contacts)):
        markup.add(telebot.types.KeyboardButton(text=f'{contacts[i][0]}'))

    return markup


def back_btn():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)

    markup.row('Назад 🔙')

    return markup
