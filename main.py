import telebot
import openai

openai.api_key = 'KEY'

BOT_TOKEN = 'TOKEN'
bot = telebot.TeleBot(BOT_TOKEN)


def get_response(msg):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "Дай топ-5 синонімів до слова: " + msg + ". Синоніми в топі не можуть повторюватись"
            }
        ],
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return completion.choices[0]['message']['content']


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привіт, це бот для пошуку синонімів. Для пошуку скористуйся командою /synonyms з меню")


@bot.message_handler(commands=['synonyms'])
def synonyms_command_handler(message):
    text = "Введи *одне* слово для пошуку синонімів: "
    sent_msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
    bot.register_next_step_handler(sent_msg, synonyms_search)


def synonyms_search(message):
    word = message.text
    word_count = len(word.split())
    if word_count != 1:
        sent_msg = bot.send_message(message.chat.id, "Будь ласка, введіть лише одне слово")
        bot.register_next_step_handler(sent_msg, synonyms_search)
    else:
        bot.send_message(message.chat.id, "Знайдено синоніми:")
        bot.send_message(message.chat.id, get_response(word), parse_mode="Markdown")


@bot.message_handler(commands=['help'])
def help_command_handler(message):
    text = "Це бот для пошуку синонімів з використанням моделі ChatGPT. Для пошуку скористуйся командою /synonyms з " \
           "меню "
    bot.send_message(message.chat.id, text, parse_mode="Markdown")


@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, "На жаль, дана команда не підримується ботом. Будь ласка, скористайся командами з меню")


bot.infinity_polling()
