import telebot
from telebot import types
import sqlite3

bot = telebot.TeleBot('token')
conn = sqlite3.connect('db_bot.db', check_same_thread=False)
cursor = conn.cursor()


def db_table_val(message):
    cursor.execute(f'SELECT * from notes WHERE user_id = {message.chat.id}')
    for result in cursor:
        bot.send_message(message.chat.id, result)


def db_table_add(note: str, user_id: int):
    cursor.execute('INSERT INTO notes (note, user_id) VALUES (?,?)', (note, user_id))
    conn.commit()


def del_notes(message):
    de_note = message.text
    query = 'DELETE FROM notes WHERE note  = ? and  (user_id = ?)'
    cursor.execute(query, (de_note, message.chat.id,))
    conn.commit()
    bot.send_message(message.chat.id, 'Заметка удалена')


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, '<b>Hello, this is test message</b>', parse_mode='html')
    bot.send_message(message.chat.id, 'Руководство на русском:')
    bot.send_message(message.chat.id,
                     'Если нужно добавить заметку напиши рандомный текст в чат, заметка будет добавлена')
    bot.send_message(message.chat.id, 'Посмотреть все заметки - All Notes')
    bot.send_message(message.chat.id, 'Создать новую заметку - Create Note')


@bot.message_handler(commands=['notes'])
def get_notes(message):
    murkup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    up = types.KeyboardButton('Create Note')
    de = types.KeyboardButton('Delete')
    all = types.KeyboardButton('All Notes')
    murkup.add(up, de, all)

    bot.send_message(message.chat.id, 'choice', reply_markup=murkup)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == 'All Notes':
        bot.send_message(message.chat.id, 'Ваши заметки')
        db_table_val(message)
    elif message.text == 'Create Note':
        bot.send_message(message.chat.id, 'Введите текст')

    elif message.text == 'Delete':
        bot.send_message(message.chat.id, 'Скопируйте ненужную заметку для удаления')
        bot.register_next_step_handler(message, del_notes)
    else:
        try:
            db_table_add(note=message.text, user_id=message.chat.id)

            bot.send_message(message.chat.id, 'Заметка добавлена')
        except:
            bot.send_message(message.chat.id, 'Заметка уже существует')


bot.polling(none_stop=True)
