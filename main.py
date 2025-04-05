import telebot
import requests
import jsons
from Class_ModelResponse import ModelResponse
from collections import defaultdict

# Замените 'YOUR_BOT_TOKEN' на ваш токен от BotFather
API_TOKEN = '8128722023:AAGfilz7eROksFesj8n2qTB60jf-CKQuAcA'
bot = telebot.TeleBot(API_TOKEN)
# Словарь для хранения контекста чатов
chat_contexts = defaultdict(list)

# Команды
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "Привет! Я ваш Telegram бот.\n"
        "Доступные команды:\n"
        "/start - вывод всех доступных команд\n"
        "/model - выводит название используемой языковой модели\n"
        "/hello - приветствие\n"
        "/clear - очистка контекста\n"
        "Отправьте любое сообщение, и я отвечу с помощью LLM модели."
    )
    bot.reply_to(message, welcome_text)


@bot.message_handler(commands=['model'])
def send_model_name(message):
    # Отправляем запрос к LM Studio для получения информации о модели
    response = requests.get('http://127.0.0.1:1234/v1/models') #http://localhost:1234/v1/models

    if response.status_code == 200:
        model_info = response.json()
        model_name = model_info['data'][0]['id']
        bot.reply_to(message, f"Используемая модель: {model_name}")
    else:
        bot.reply_to(message, 'Не удалось получить информацию о модели.')

@bot.message_handler(commands=['hello'])
def send_hello(message):
    bot.reply_to(message, "Привет! Чем я могу помочь?")


@bot.message_handler(commands=['clear'])
def clear_context(message):
    # Функция очистки контекста
    user_id = message.from_user.id
    chat_contexts[user_id] = []
    bot.reply_to(message, "Контекст чата очищен.")


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id  # id пользователя
    user_query = message.text
    request = {
        "messages": [
          *chat_contexts[user_id],
          {
            "role": "user",
            "content": user_query
          },
        ]
    }
    response = requests.post(
        'http://127.0.0.1:1234/v1/chat/completions',
        json=request
    )
    if response.status_code == 200:
        model_response: ModelResponse = jsons.loads(response.text, ModelResponse)
        bot_reply = model_response.choices[0].message.content
        # Сохраняем оба сообщения в контекст
        chat_contexts[user_id].append({
            "role": "user",
            "content": user_query
        })
        chat_contexts[user_id].append({
            "role": "assistant",
            "content": bot_reply
        })
        bot.reply_to(message, bot_reply)
        print(chat_contexts)
    else:
        bot.reply_to(message, 'Произошла ошибка при обращении к модели.')


# Запуск бота
if __name__ == '__main__':
    bot.polling(none_stop=True)