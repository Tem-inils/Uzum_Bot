import telebot
import buttons

from database import Database

bot = telebot.TeleBot(token='YOUR_TOKEN_BOT')
data = Database()

admin = [302137006, 879360429]


@bot.message_handler(commands=['start'])
def message_start(message):
    user_id = message.from_user.id
    if user_id in admin:
        bot.send_message(user_id, 'Добро пожаловать', reply_markup=buttons.menu_btn())
    else:
        checker = data.checker_user(tg_id=user_id)
        if checker:
            bot.send_message(user_id, 'Добро пожаловать', reply_markup=buttons.user_menu())
        else:
            bot.send_message(user_id, 'Добро пожаловаьт отправьте свой номер используя кнопку.',
                             reply_markup=buttons.get_user_contact())
            bot.register_next_step_handler(message, get_user_contact_handler)


def get_user_contact_handler(message):
    user_id = message.from_user.id

    if message.contact:
        user_contact = message.contact.phone_number
        if '+' in user_contact:
            result = data.register_user_db(tg_id=user_id, contact=f'{user_contact}')
            if result is True:
                bot.send_message(user_id, 'Отлично вы прошли регистрацию 🤑')
                message_start(message)
            else:
                bot.send_message(user_id, 'Извените пока что вас нету в списках обратитесь к Администрации \n'
                                          'Жасур - https://t.me/Woodotaaa (+998 90 966 78 55)\n'
                                          'Или администрации TEHNIKUM',
                                 reply_markup=telebot.types.ReplyKeyboardRemove())
        else:
            result = data.register_user_db(tg_id=user_id, contact=f'+{user_contact}')
            if result is True:
                bot.send_message(user_id, 'Отлично вы прошли регистрацию 🤑')
                message_start(message)
            else:
                bot.send_message(user_id, 'Извените пока что вас нету в списках обратитесь к Администрации \n'
                                          'Жасур - https://t.me/Woodotaaa (+998 90 966 78 55)\n'
                                          'Или администрации TEHNIKUM',
                                 reply_markup=telebot.types.ReplyKeyboardRemove())


@bot.message_handler(content_types=['text'])
def check_button(message):
    user_id = message.from_user.id
    user_tg_id = data.checker_user(user_id)
    if user_id in admin:
        if message.text == 'Добавить контакт 👤':
            bot.delete_message(chat_id=user_id, message_id=message.message_id)
            # bot.delete_message(chat_id=user_id, message_id=message.message_id - 1)

            bot.send_message(text='Напишите контакт или список номеров через запятую что бы добавить.\n'
                                  'Example: Albert, +99890..., Pasha, +99897424...',
                             chat_id=user_id, reply_markup=buttons.back_btn())

            bot.register_next_step_handler(message, add_contact_handler)

        elif message.text == 'Удалить контакты ⛔️':
            bot.delete_message(chat_id=user_id, message_id=message.message_id)
            # bot.delete_message(chat_id=user_id, message_id=message.message_id - 1)

            bot.send_message(text='Отправьте ссылку для изменения', chat_id=user_id,
                             reply_markup=buttons.get_contact_btn())

            bot.register_next_step_handler(message, del_contact_handler)

        elif message.text == 'Обновить ссылку 🆕':
            bot.delete_message(chat_id=user_id, message_id=message.message_id)
            # bot.delete_message(chat_id=user_id, message_id=message.message_id - 1)

            bot.send_message(text='Отправьте новую ссылку', chat_id=user_id,
                             reply_markup=buttons.back_btn())

            bot.register_next_step_handler(message, get_link_handler)

        elif message.text == 'Получить весь список контактов 👥':
            bot.delete_message(chat_id=user_id, message_id=message.message_id)
            # bot.delete_message(chat_id=user_id, message_id=message.message_id - 1)

            bot.send_message(user_id,
                             text='\n'.join(' '.join(str(i) for i in contact) for contact in data.get_all_contact()),
                             reply_markup=buttons.menu_btn())
        elif message.text == 'Разослать новую ссылку 🖇️':
            bot.delete_message(chat_id=user_id, message_id=message.message_id)

            users_id = [i[0] for i in data.get_all_tg_id()]
            link = data.get_link()[0][0]
            for ids_user in users_id:
                bot.send_message(ids_user, f'Ссылка обновленна -> {link}',
                                 reply_markup=telebot.types.ReplyKeyboardRemove())

            bot.send_message(user_id, 'Разослали =)', reply_markup=buttons.menu_btn())
        else:
            bot.delete_message(chat_id=user_id, message_id=message.message_id)
            # bot.delete_message(chat_id=user_id, message_id=message.message_id - 1)

            bot.send_message(chat_id=user_id, text='Используйте кнопки =)', reply_markup=buttons.menu_btn())
    elif user_tg_id is not None:
        if message.text == 'Получить ссылку на урок 🖇️':
            bot.delete_message(chat_id=user_id, message_id=message.message_id)

            bot.send_message(user_id, f'Ваша ссылка на последний урок', reply_markup=buttons.get_lesson_link())

    else:
        pass


def del_contact_handler(message):
    user_id = message.from_user.id

    if user_id in admin:
        contacts_db = data.get_all_contact()
        contacts = [contacts_db[i][0] for i in range(0, len(contacts_db))]

        if message.text == 'Удалить все 🫂':
            data.delete_all_contact()
            bot.send_message(user_id, 'Все пользователи удаленны. Хорошего дня', reply_markup=buttons.menu_btn())

        elif message.text == 'Назад 🔙':
            bot.delete_message(chat_id=user_id, message_id=message.message_id)
            bot.delete_message(chat_id=user_id, message_id=message.message_id - 1)

            message_start(message)

        elif message.text in contacts:
            data.delete_all_contact(contact=message.text)
            bot.send_message(user_id, 'Пользователь удален. Хорошего дня', reply_markup=buttons.menu_btn())


def get_link_handler(message):
    user_id = message.from_user.id

    if user_id in admin:
        if message.text == 'Назад 🔙':
            bot.delete_message(chat_id=user_id, message_id=message.message_id)
            # bot.delete_message(chat_id=user_id, message_id=message.message_id - 1)

            message_start(message)

        else:
            new_link = message.text
            data.add_link_db(new_link)

            bot.send_message(user_id, 'Отлично ссылка обновлена !', reply_markup=buttons.menu_btn())


def add_contact_handler(message):
    user_id = message.from_user.id

    if user_id in admin:
        if message.text == 'Назад 🔙':
            bot.delete_message(chat_id=user_id, message_id=message.message_id)
            # bot.delete_message(chat_id=user_id, message_id=message.message_id - 1)

            message_start(message)
        else:
            list_contacts = str(message.text)
            elements = list_contacts.split(", ")
            for i in range(0, len(elements), 2):
                contact1 = elements[i]
                contact2 = elements[i + 1] if i + 1 < len(elements) else None

                data.add_user_contact(name=contact1, contact=contact2)

            bot.send_message(user_id, 'Все добовления прошли успешно =)', reply_markup=buttons.menu_btn())


if __name__ == '__main__':
    bot.polling(none_stop=True)
