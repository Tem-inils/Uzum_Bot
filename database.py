import sqlite3

connection = sqlite3.connect('mydb.db')
cursor = connection.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS contacts (name TEXT, contact TEXT, tg_id INTEGER);')
cursor.execute('CREATE TABLE IF NOT EXISTS links (link TEXT);')


class Database:
    def __init__(self):
        self.connection = sqlite3.connect('mydb.db', check_same_thread=False)
        self.cursor = self.connection.cursor()

    """CHECKERS"""

    # Проверка пользователя на запись в бд возвращает всю инфу о пользователе
    def checker_user(self, tg_id: int):
        try:
            with self.connection:
                return self.cursor.execute('SELECT * FROM contacts WHERE tg_id = ?;', (tg_id,)).fetchone()

        except Exception as e:
            print(e)

    # Проверяет наличие контакта в бд на курсе при первой регистрации если да
    # то до записывает tg_id и проходит регистрацию возврощает True or False
    def register_user_db(self, tg_id: int, contact: str):
        try:
            with self.connection:
                checker = self.cursor.execute('SELECT contact FROM contacts WHERE contact = ?;', (contact,)).fetchone()
                if checker:
                    self.cursor.execute('UPDATE contacts SET tg_id = ? WHERE contact = ?;', (tg_id, contact))
                    return True
                else:
                    return False

        except Exception as e:
            print(e)

    # Проверяет наличие ссылки в бд если есть обновляет если нет записывает
    def add_link_db(self, link: str = 'None'):
        try:
            with self.connection:
                checker = self.cursor.execute('SELECT link FROM links').fetchone()
                if checker:
                    return self.cursor.execute('UPDATE links SET link = ? WHERE link = ?;', (link, checker[0]))
                else:
                    return self.cursor.execute('INSERT INTO links (link) VALUES (?);', (link,))
        except Exception as e:
            print(e)

    """ADMIN USAGE"""

    # Возврощает id всех студентов
    def get_all_tg_id(self):
        try:
            with self.connection:
                return self.cursor.execute('SELECT tg_id FROM contacts').fetchall()

        except Exception as e:
            print(e)

    # Позволяет получить ссылку
    def get_link(self):
        try:
            with self.connection:
                return self.cursor.execute('SELECT * FROM links').fetchall()
        except Exception as e:
            print(e)

    # Позволяет записать контакт имя в таблицу контактов
    def add_user_contact(self, name: str, contact: [str, list]):
        try:
            with self.connection:
                return self.cursor.execute('INSERT INTO contacts (name, contact) VALUES (?,?);', (name, contact))

        except Exception as e:
            print(e)

    # Все контакты
    def get_all_contact(self):
        try:
            with self.connection:
                contact = self.cursor.execute('SELECT * FROM contacts').fetchall()
                if contact:
                    return contact

                return 'Контактов нету'

        except Exception as e:
            print(e)

    # Удаление 1 или всех контактов
    def delete_all_contact(self, contact=None):
        try:
            # Реализовать удаленни либо всех контактов либо одного
            with self.connection:
                if contact:
                    return self.cursor.execute('DELETE FROM contacts WHERE name = ?;', (contact,))
                else:
                    return self.cursor.execute("DELETE FROM contacts").fetchall()

        except Exception as e:
            print(e)


