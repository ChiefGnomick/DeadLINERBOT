import telebot
from main import *

# Обработчик текстовых сообщений (удаляет последнее сообщение пользователя)
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        # Удаляем сообщение пользователя
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        print(f"Сообщение от пользователя {message.from_user.username} удалено.")
    except Exception as e:
        print(f"Не удалось удалить сообщение: {e}")