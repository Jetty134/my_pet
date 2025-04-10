import telebot
from telebot import types
import random
import time
import requests
from bs4 import BeautifulSoup


token = '8024942469:AAFfNT4TWBsRTJiAkR8l_RotZ2DkocsgQfo'
bot = telebot.TeleBot(token=token)

name = ''
energy = 100
satiety = 100
hapiness = 100
remind = []
kw = ''



def feed():
    global satiety, energy, hapiness
    satiety += 15
    energy += 22
    hapiness += 11

def play():
    global satiety, energy, hapiness
    satiety -= 33
    energy -= 50
    hapiness += 10

def sleep():
    global satiety, energy, hapiness
    satiety -= 26
    energy += 44
    hapiness -= 32




def check(message):
    global satiety, energy, hapiness
    if satiety <= 0:
        bot.send_message(message.chat.id, f'{name} умер от голода. Не забывайте кормить питомца!')
    elif satiety >= 10:
        bot.send_message(message.chat.id, f'{name} наелся и счастлив!')
    if hapiness < 0:
        bot.send_message(message.chat.id, f'{name} умер от тоски. С питомцем нужно чаще играть!')
    elif hapiness > 100:
        bot.send_message(message.chat.id, f'{name} счастлив как никогда')
    if energy < 70:
        bot.send_message(message.chat.id, f'{name}) умер от истощения.')
    elif energy > 70:
        bot.send_message(message.chat.id, f'{name} полон сил и энергии!!!')


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,'Привет, я бот тамагочи, чем займемся сегодня?')
    keyboard = types.ReplyKeyboardMarkup(row_width=3)
    item1 = types.KeyboardButton('/feed')
    item2 = types.KeyboardButton('/play')
    item3 = types.KeyboardButton('/sleep')
    item4 = types.KeyboardButton('/number')
    item5 = types.KeyboardButton('/startremind')
    item6 = types.KeyboardButton('/play_with_me')
    item7 = types.KeyboardButton('/name')
    item8 = types.KeyboardButton('/remind_me')
    item9 = types.KeyboardButton('/remind')
    item10 = types.KeyboardButton('/history')
    item11 = types.KeyboardButton('/startplay')
    keyboard.add(item1, item2 ,item3 ,item4 ,item5 ,item6 ,item7 ,item8 ,item9, item10, item11)
    bot.send_message(message.chat.id, 'Выбери команду.', reply_markup=keyboard)

@bot.message_handler(commands=['feed'])
def f(message):
    feed()
    check(message)


@bot.message_handler(commands=['play'])
def p(message):
    play()
    check(message)



@bot.message_handler(commands=['sleep'])
def s(message):
    sleep()
    check(message)


@bot.message_handler(commands=['play_with_me'])
def f(message):
    emoji_to_choice = {
        '✂️': 'ножницы',
        '📄': 'бумага',
        '🪨': 'камень'
    }

    choice_to_emoji = {
        'ножницы': '✂️',
        'бумага': '📄',
        'камень': '🪨'
    }

    @bot.message_handler(commands=['startplay'])
    def start(message):
        bot.reply_to(message, 'Привет, я бот для игры в камень-ножницы-бумага! Нажми /play2 чтобы начать.')

    @bot.message_handler(commands=['play2'])
    def play(message):
        markup = types.ReplyKeyboardMarkup(row_width=3)
        item1 = types.KeyboardButton('✂️')
        item2 = types.KeyboardButton('📄')
        item3 = types.KeyboardButton('🪨')
        markup.add(item1, item2, item3)
        bot.send_message(message.chat.id, 'Выбери свой ход:', reply_markup=markup)

    def determine_winner(user_choice, bot_choice):
        if user_choice == bot_choice:
            return 'ничья'
        elif (user_choice == 'камень' and bot_choice == 'ножницы') or \
                (user_choice == 'ножницы' and bot_choice == 'бумага') or \
                (user_choice == 'бумага' and bot_choice == 'камень'):
            return 'игрок'
        else:
            return 'бот'

    @bot.message_handler(content_types=['text'])
    def handle_choice(message):
        if message.text not in emoji_to_choice:
            bot.send_message(message.chat.id, 'Пожалуйста, используйте кнопки для игры.')
            return

        # Получаем выбор игрока
        user_emoji = message.text
        user_choice = emoji_to_choice[user_emoji]

        # Бот делает случайный выбор
        bot_choice = random.choice(list(choice_to_emoji.keys()))
        bot_emoji = choice_to_emoji[bot_choice]

        # Определяем победителя
        result = determine_winner(user_choice, bot_choice)

        # Формируем сообщение
        response = f"""
    🎮 Ваш ход: {user_emoji} ({user_choice})
    🤖 Мой ход: {bot_emoji} ({bot_choice})
    """

        if result == 'игрок':
            response += "🏆 Вы победили!"
        elif result == 'бот':
            response += "💥 Я победил!"
        else:
            response += "🤝 Ничья!"

        # Отправляем результат и убираем клавиатуру
        bot.send_message(message.chat.id, response, reply_markup=types.ReplyKeyboardRemove())




@bot.message_handler(commands=['name'])
def name2(message):
    bot.send_message(message.chat.id, 'Введите имя питомца: ')
    bot.register_next_step_handler(message, second_step)
def second_step(message):
    global name
    name = message.text

@bot.message_handler(commands=['remind_me'])
def r(message):
    @bot.message_handler(commands=['startremind'])
    def start(message):
        bot.reply_to(message,
                     'Привет, я могу делать  напоминания, чтобы увидеть историю напоминаний введите команду /history или введите /remind , чтобы создать напоминание')

    @bot.message_handler(commands=['history'])
    def h(message):
        global remind
        for i in remind:
            bot.send_message(message.chat.id, i)

    @bot.message_handler(commands=['remind'])
    def set_reminder(message):
        bot.send_message(message.chat.id, f'Привет! Какаое напоминание надо сделать?')
        bot.register_next_step_handler(message, second_step)

    def second_step(message):
        global remind
        r = message.text
        remind.append(r)
        bot.send_message(message.chat.id, 'Через какое время должно сработать напоминание?')
        bot.register_next_step_handler(message, third_step, r)

    def third_step(message, r):
        t = int(message.text)
        chat_id = message.chat.id
        time.sleep(t)
        bot.send_message(chat_id, 'Напоминание!!!' + r)

    @bot.message_handler(commands=['history'])
    def h(message):
        global remind
        for i in remind:
            bot.send_message(message.chat.id, i)



@bot.message_handler(commands=['number'])
def n(message):
    bot.send_message(message.chat.id, 'Введите число, про которое вы хотите получить факт: ')
    bot.register_next_step_handler(message, second_step1)
def second_step1(message):
    global kw
    kw = message.text
    url = f'http://numbersapi.com/{kw}/trivia?fragment'
    response = requests.get(url + kw)
    bot.send_message(message.chat.id,response.text)



bot.polling()
