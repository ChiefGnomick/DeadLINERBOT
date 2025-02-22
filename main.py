from IMGcreator import *
from Deleter import *
import telebot
from telebot import types

bot = telebot.TeleBot('7723354892:AAEh8K98-gViX0kY9SrejcCu2KWxbYpV6ec')

key_menu = bool(True)

# Словарь для хранения состояний пользователей
user_state = {}

# Словарь для хранения данных пользователей
user_data = {}

example_dict = {
    "Матанал": 0,
    "Физика": 0,
    "Дискретка": 0,
    "Линейка": 0
}
# Обработчик для фото
@bot.message_handler(content_types=['photo'])
def get_photo(message):
    bot.reply_to(message, "Нормис")  # Ответ на сообщение

@bot.message_handler(commands=['start'])
def message_start(message):
    bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name}. Укажи номер своей группы.")
    user_state[message.chat.id] = "waiting_for_group_id"  # Устанавливаем состояние
    if message.text:
        print(message.text)

def send_buttons_from_dict(message, data_dict):
    """
    Отправляет сообщение с кнопками, где количество кнопок зависит от длины словаря.
    :param message: Объект сообщения (для получения chat_id).
    :param data_dict: Словарь, где ключи — названия кнопок, а значения — 0 или 1.
    """
    markup = types.InlineKeyboardMarkup()  # Создаем разметку для кнопок

    # Динамически создаем кнопки на основе ключей словаря, где значение равно 0
    for key, value in data_dict.items():
        if value == 0:  # Отображаем только те кнопки, у которых значение 0
            button = types.InlineKeyboardButton(text=key, callback_data=key)
            markup.add(button)  # Добавляем кнопку в разметку

    # Отправляем сообщение с кнопками
    bot.send_message(message.chat.id, "————————————Выберите задание——————————", reply_markup=markup)

# Обработчик команды /menu
@bot.message_handler(commands=['menu'])
def message_menu(message):
    markup = types.InlineKeyboardMarkup()

    btn_preWeek = types.InlineKeyboardButton("◀️", callback_data='preWeek')
    btn_currentWeek = types.InlineKeyboardButton("🔄", callback_data='currentWeek')
    btn_nextWeek = types.InlineKeyboardButton("▶️", callback_data='nextWeek')

    markup.row(btn_preWeek, btn_currentWeek, btn_nextWeek)

    if key_menu:
        btn_schedule = types.InlineKeyboardButton("Мое расписание 📅", callback_data='schedule')
        btn_scheduleOrHomework = btn_schedule
    else:
        btn_homework = types.InlineKeyboardButton("Мое Д/З 📚️", callback_data='homework')
        btn_scheduleOrHomework = btn_homework

    btn_progress = types.InlineKeyboardButton("Прогресс ✅", callback_data='progress')
    markup.row(btn_scheduleOrHomework, btn_progress)

    btn_lookSchedule = types.InlineKeyboardButton("Конспекты 📝", callback_data='lookAbstract')
    btn_homeworkManage = types.InlineKeyboardButton("Управление Д/З 📋️", callback_data='homeworkManage')
    markup.row(btn_lookSchedule, btn_homeworkManage)

    table_menu = open('table.png', 'rb')
    bot.send_photo(message.chat.id, table_menu, reply_markup=markup)


# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    chat_id = message.chat.id

    # Проверяем состояние пользователя
    if user_state.get(chat_id) == "waiting_for_subject":
        # Сохраняем название предмета
        user_data[chat_id] = {"subject": message.text}
        bot.send_message(chat_id, "Теперь введите дату (например, 2023-10-15):")
        user_state[chat_id] = "waiting_for_date"  # Переходим в состояние ожидания даты

    elif user_state.get(chat_id) == "waiting_for_date":
        # Сохраняем дату
        user_data[chat_id]["date"] = message.text
        bot.send_message(chat_id, f"Данные сохранены: Предмет - {user_data[chat_id]['subject']}, Дата - {user_data[chat_id]['date']}")
        user_state[chat_id] = None  # Сбрасываем состояние


@bot.message_handler(func=lambda message: True)
def handle_text(message):
    chat_id = message.chat.id

    # Проверяем состояние пользователя
    if user_state.get(chat_id) == "waiting_for_group_id":
        # Сохраняем номер группы в словарь user_data
        user_data[chat_id] = {"group_id": message.text}
        bot.send_message(chat_id, f"Номер группы '{message.text}' сохранен!")
        user_state[chat_id] = None  # Сбрасываем состояние


# Метод для запроса названия предмета
def lesson_message(message):
    bot.send_message(message.chat.id, "Введите название предмета:")
    user_state[message.chat.id] = "waiting_for_subject"  # Устанавливаем состояние


# Метод для удаления сообщений
def delete_message(message):
    try:
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    except Exception as e:
        print(f"Ошибка при удалении сообщения: {e}")

# Обработчик callback-запросов
@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    global key_menu
    if callback.data == 'preWeek':
        print()
    if callback.data == 'currentWeek':
        print()
    if callback.data == 'nextWeek':
        print()
    if callback.data == "schedule":
        key_menu = False
        delete_message(callback.message)
        message_menu(callback.message)
    if callback.data == "homework":
        key_menu = True
        delete_message(callback.message)
        message_menu(callback.message)
    if callback.data == "lookAbstract":
        lesson_message(callback.message)
    if callback.data == "homeworkManage":
        send_buttons_from_dict(callback.message, example_dict)
    else:
        # Обработка нажатий на кнопки, созданные из словаря
        selected_key = callback.data
        if selected_key in example_dict:
            example_dict[selected_key] = 1  # Меняем значение на 1
            bot.send_message(callback.message.chat.id, f"Задание: [{selected_key}] выполнено✅")
            # Повторно отправляем кнопки (теперь без выбранной)
            send_buttons_from_dict(callback.message, example_dict)

# Обработчик команды /info
@bot.message_handler(commands=['info'])
def message_info(message):
    bot.send_message(message.chat.id, f"Информация о пользователе:\n {message}")


# Запуск бота
bot.polling(none_stop=True)