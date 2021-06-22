import gensim
import flask
from gensim.models import word2vec
from conf import TOKEN, WEBHOOK_HOST, WEBHOOK_PORT
import telebot
from telebot import types
from collections import defaultdict
import random
import time
from pymystem3 import Mystem
import operator
import matplotlib.pyplot as plt
import os

m = Mystem()

WEBHOOK_URL_BASE = "https://{}:{}".format(WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/{}/".format(TOKEN)

bot = telebot.TeleBot(TOKEN, threaded=False)

bot.remove_webhook()
bot.set_webhook(url=str(WEBHOOK_URL_BASE + WEBHOOK_URL_PATH))

app = flask.Flask(__name__)

model = gensim.models.KeyedVectors.load_word2vec_format('/home/IgorCigoreta/mysite/winx.bin', binary=True)
model.init_sims(replace=True)

state = 0

WinxClub = {'Блум': '{блум}',
            'Стелла': '{стелла}',
            'Текна': '{текн?}',
            'Флора': '{флора}',
            'Муза': '{муза}',
            'Лейла': '{лейла}'
            }
WinxClubReversed = {'{блум}': 'Блум',
                    '{стелла}': 'Стелла',
                    '{текн?}': 'Текна',
                    '{флора}': 'Флора',
                    '{муза}': 'Муза',
                    '{лейла}': 'Лейла'
                    }

Planets = {'Линфея': '{линфея?}»',
           'Андрос': '{андрос}',
           'Солярия': '{солярий}',
           'Домино': '{домино}',
           'Обсидиан': '{обсидиан}',
           'Даймонд': '{даймонд?}',
           'Мелодия': '{мелодия}',
           'Эраклион': '{эраклион?}»',
           'Зенит': '{зенит}'
           }

Fairies = {'Несса': '{несс?}',
           'Мирта': '{мирт}',
           'Нова': '«{новый}',
           'Галатея': '{галатея}',
           'Миели': '{миель?}',
           'Дафна': '{дафна}',
           'Политея': '{политей?}',
           'Мавилла': '{мавилла?}'
           }

Earth_Fairies = {'Рокси': '{рокси?}',
                 'Моргана': '{морган}',
                 'Диана': '{диана}',
                 'Небула': '{небула?}',
                 'Аврора': '{аврора}',
                 'Сибилла': '{сибилла}'
                 }

Specialists = {'Скай': '{скай}',
               'Ривен': '{ривен?}',
               'Некс': '{некс?}',
               'Гелия': '{гелия}',
               'Брендон': '{брендон}',
               'Рой': '{рой}',
               'Набу': '{наб}',
               'Тимми': '{тимми}'
               }

users = defaultdict()

with open('/home/IgorCigoreta/mysite/adj.txt', 'r', encoding='utf-8') as f:
    all_adj = f.read().split(', ')
    adj = set()
    adj.add(random.choice(all_adj))
    adj.add(random.choice(all_adj))
    adj.add(random.choice(all_adj))
    adj.add(random.choice(all_adj))
    if len(adj) < 4:
        while len(adj) < 4:
            adj.add(random.choice(all_adj))
            adj.add(random.choice(all_adj))
            adj.add(random.choice(all_adj))
            adj.add(random.choice(all_adj))
    adj_list = list()
    for i in adj:
        adj_list.append(i)


@bot.message_handler(commands=['start', 'help'])
def send_help_or_start(message):
    global state
    state = 0
    keyboard = types.InlineKeyboardMarkup()
    starting = types.InlineKeyboardButton(text='НАЧАТЬ', callback_data='starting')
    keyboard.add(starting)
    bot.send_message(message.chat.id,
                     'Здравствуйте! Это бот, который оценивает Вас, Ваши личностные качества и который '
                     'дает ответ на животрепещущий вопрос - Какая же Вы феечка Винкс?',
                     reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def send_buttons(message):
    global state
    global adj_list
    if state == 0:
        keyboard_start = types.ReplyKeyboardMarkup()
        start = types.InlineKeyboardButton(text='/start')
        our_help = types.InlineKeyboardButton(text='/help')
        keyboard_start.add(start, our_help)
        bot.send_message(message.chat.id, 'Начало работы бота',
                         reply_markup=keyboard_start)
    elif state == 1:
        users[str(message.chat.id)] = {'{блум}': 0,
                                       '{стелла}': 0,
                                       '{текн?}': 0,
                                       '{флора}': 0,
                                       '{муза}': 0,
                                       '{лейла}': 0
                                       }
        text = str(message.text)
        lemmas = m.lemmatize(text)
        for one in lemmas:
            try:
                users[str(message.chat.id)]['{блум}'] += float(model.similarity('{' + str(one) + '}', '{блум}'))
                users[str(message.chat.id)]['{стелла}'] += float(model.similarity('{' + str(one) + '}', '{стелла}'))
                users[str(message.chat.id)]['{текн?}'] += float(model.similarity('{' + str(one) + '}', '{текн?}'))
                users[str(message.chat.id)]['{флора}'] += float(model.similarity('{' + str(one) + '}', '{флора}'))
                users[str(message.chat.id)]['{муза}'] += float(model.similarity('{' + str(one) + '}', '{муза}'))
                users[str(message.chat.id)]['{лейла}'] += float(model.similarity('{' + str(one) + '}', '{лейла}'))
            except KeyError:
                continue
        keyboard_2 = types.InlineKeyboardMarkup()
        after_first = types.InlineKeyboardButton(text='ПРОДОЛЖИТЬ', callback_data='after_first')
        keyboard_2.add(after_first)
        bot.send_message(message.chat.id, 'Ответ принят! Нажмите на кнопку, чтобы продолжить', reply_markup=keyboard_2)
        state = 0.5
    elif state == 2:
        text = str(message.text)
        adj_list.remove(text)
        removed = str('{' + text + '}')
        removed = removed.replace("'", '')
        try:
            users[str(message.chat.id)]['{блум}'] += float(model.similarity(removed, '{блум}') - 1)
            users[str(message.chat.id)]['{стелла}'] += float(model.similarity(removed, '{стелла}') - 1)
            users[str(message.chat.id)]['{текн?}'] += float(model.similarity(removed, '{текн?}') - 1)
            users[str(message.chat.id)]['{флора}'] += float(model.similarity(removed, '{флора}') - 1)
            users[str(message.chat.id)]['{муза}'] += float(model.similarity(removed, '{муза}') - 1)
            users[str(message.chat.id)]['{лейла}'] += float(model.similarity(removed, '{лейла}') - 1)
        except KeyError:
            users[str(message.chat.id)]['{блум}'] -= 0.5
            users[str(message.chat.id)]['{стелла}'] -= 0.5
            users[str(message.chat.id)]['{текн?}'] -= 0.5
            users[str(message.chat.id)]['{флора}'] -= 0.5
            users[str(message.chat.id)]['{муза}'] -= 0.5
            users[str(message.chat.id)]['{лейла}'] -= 0.5
        for elem in adj_list:
            our_elem = str('{' + elem + '}')
            our_elem = our_elem.replace("'", '')
            try:
                users[str(message.chat.id)]['{блум}'] += float(model.similarity(our_elem, '{блум}'))
                users[str(message.chat.id)]['{стелла}'] += float(model.similarity(our_elem, '{стелла}'))
                users[str(message.chat.id)]['{текн?}'] += float(model.similarity(our_elem, '{текн?}'))
                users[str(message.chat.id)]['{флора}'] += float(model.similarity(our_elem, '{флора}'))
                users[str(message.chat.id)]['{муза}'] += float(model.similarity(our_elem, '{муза}'))
                users[str(message.chat.id)]['{лейла}'] += float(model.similarity(our_elem, '{лейла}'))
            except KeyError:
                users[str(message.chat.id)]['{блум}'] += 0.5
                users[str(message.chat.id)]['{стелла}'] += 0.5
                users[str(message.chat.id)]['{текн?}'] += 0.5
                users[str(message.chat.id)]['{флора}'] += 0.5
                users[str(message.chat.id)]['{муза}'] += 0.5
                users[str(message.chat.id)]['{лейла}'] += 0.5
        keyboard_3 = types.InlineKeyboardMarkup()
        after_second = types.InlineKeyboardButton(text='ПРОДОЛЖИТЬ', callback_data='after_second')
        keyboard_3.add(after_second)
        bot.send_message(message.chat.id, 'Ответ принят! Нажмите на кнопку, чтобы продолжить', reply_markup=keyboard_3)
        state = 0.5
    elif state == 3:
        text = str(message.text)
        users[str(message.chat.id)]['{блум}'] += float(model.similarity(Planets[text], '{блум}'))
        users[str(message.chat.id)]['{стелла}'] += float(model.similarity(Planets[text], '{стелла}'))
        users[str(message.chat.id)]['{текн?}'] += float(model.similarity(Planets[text], '{текн?}'))
        users[str(message.chat.id)]['{флора}'] += float(model.similarity(Planets[text], '{флора}'))
        users[str(message.chat.id)]['{муза}'] += float(model.similarity(Planets[text], '{муза}'))
        users[str(message.chat.id)]['{лейла}'] += float(model.similarity(Planets[text], '{лейла}'))
        keyboard_4 = types.InlineKeyboardMarkup()
        after_third = types.InlineKeyboardButton(text='ПРОДОЛЖИТЬ', callback_data='after_third')
        keyboard_4.add(after_third)
        bot.send_message(message.chat.id, 'Ответ принят! Нажмите на кнопку, чтобы продолжить', reply_markup=keyboard_4)
        state = 0.5
    elif state == 4:
        text = str(message.text)
        users[str(message.chat.id)]['{блум}'] += float(model.similarity(Fairies[text], '{блум}'))
        users[str(message.chat.id)]['{стелла}'] += float(model.similarity(Fairies[text], '{стелла}'))
        users[str(message.chat.id)]['{текн?}'] += float(model.similarity(Fairies[text], '{текн?}'))
        users[str(message.chat.id)]['{флора}'] += float(model.similarity(Fairies[text], '{флора}'))
        users[str(message.chat.id)]['{муза}'] += float(model.similarity(Fairies[text], '{муза}'))
        users[str(message.chat.id)]['{лейла}'] += float(model.similarity(Fairies[text], '{лейла}'))
        keyboard = types.InlineKeyboardMarkup()
        next = types.InlineKeyboardButton(text='СЛЕДУЮЩИЙ ВОПРОС', callback_data='smh')
        keyboard.add(next)
        bot.send_message(message.chat.id, 'Нажмите на кнопку, чтобы перейти на следующий вопрос',
                         reply_markup=keyboard)
        state = 0.5
    elif state == 4.5:
        text = str(message.text)
        users[str(message.chat.id)]['{блум}'] += float(model.similarity(Earth_Fairies[text], '{блум}'))
        users[str(message.chat.id)]['{стелла}'] += float(model.similarity(Earth_Fairies[text], '{стелла}'))
        users[str(message.chat.id)]['{текн?}'] += float(model.similarity(Earth_Fairies[text], '{текн?}'))
        users[str(message.chat.id)]['{флора}'] += float(model.similarity(Earth_Fairies[text], '{флора}'))
        users[str(message.chat.id)]['{муза}'] += float(model.similarity(Earth_Fairies[text], '{муза}'))
        users[str(message.chat.id)]['{лейла}'] += float(model.similarity(Earth_Fairies[text], '{лейла}'))
        keyboard = types.InlineKeyboardMarkup()
        next = types.InlineKeyboardButton(text='СЛЕДУЮЩИЙ ВОПРОС', callback_data='after_fifth')
        keyboard.add(next)
        bot.send_message(message.chat.id, 'Нажмите на кнопку, чтобы перейти на следующий вопрос',
                         reply_markup=keyboard)
        state = 0.5
    elif state == 6:
        text = str(message.text)
        users[str(message.chat.id)]['{блум}'] += float(model.similarity(Specialists[text], '{блум}'))
        users[str(message.chat.id)]['{стелла}'] += float(model.similarity(Specialists[text], '{стелла}'))
        users[str(message.chat.id)]['{текн?}'] += float(model.similarity(Specialists[text], '{текн?}'))
        users[str(message.chat.id)]['{флора}'] += float(model.similarity(Specialists[text], '{флора}'))
        users[str(message.chat.id)]['{муза}'] += float(model.similarity(Specialists[text], '{муза}'))
        users[str(message.chat.id)]['{лейла}'] += float(model.similarity(Specialists[text], '{лейла}'))
        keyboard_7 = types.InlineKeyboardMarkup()
        after_sixth = types.InlineKeyboardButton(text='ПРОДОЛЖИТЬ', callback_data='after_sixth')
        keyboard_7.add(after_sixth)
        bot.send_message(message.chat.id, 'Переходим к последнему вопросу?', reply_markup=keyboard_7)
        state = 0.5
    elif state == 7:
        text = str(message.text)
        users[str(message.chat.id)][WinxClub[text]] += 0.4
        keyboard_8 = types.InlineKeyboardMarkup()
        final = types.InlineKeyboardButton(text='ФИНАЛЬНЫЙ ПОДСЧЕТ', callback_data='final')
        keyboard_8.add(final)
        bot.send_message(message.chat.id, 'Нажмите на кнопку, чтобы узнать, какая Вы фея Винкс!',
                         reply_markup=keyboard_8)
        state = 0.5


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    global state
    global adj_list
    if call.message:
        if call.data == 'starting':
            call.data = 'waiting'
            state = 1
            bot.send_message(call.message.chat.id, 'Начинаем квиз!', reply_markup=types.ReplyKeyboardRemove())
            time.sleep(2)
            bot.send_message(call.message.chat.id, 'Давайте сначала поговорим о Вас! Как Вы себя можете описать?')
        elif call.data == 'after_first':
            call.data = 'waiting'
            state = 2
            bot.send_message(call.message.chat.id, 'Продолжаем квиз!')
            qbord = types.ReplyKeyboardMarkup()
            second_1 = types.InlineKeyboardButton(text=adj_list[0], callback_data='second')
            second_2 = types.InlineKeyboardButton(text=adj_list[1], callback_data='second')
            second_3 = types.InlineKeyboardButton(text=adj_list[2], callback_data='second')
            second_4 = types.InlineKeyboardButton(text=adj_list[3], callback_data='second')
            qbord.add(second_1)
            qbord.add(second_2)
            qbord.add(second_3)
            qbord.add(second_4)
            bot.send_message(call.message.chat.id, 'Какое из слов лишнее?',
                             reply_markup=qbord)
        elif call.data == 'after_second':
            call.data = 'waiting'
            bot.send_message(call.message.chat.id, 'Продолжаем квиз!')
            qbord = types.ReplyKeyboardMarkup()
            third_1 = types.InlineKeyboardButton(text='Линфея', callback_data='third')
            third_2 = types.InlineKeyboardButton(text='Андрос', callback_data='third')
            third_3 = types.InlineKeyboardButton(text='Солярия', callback_data='third')
            third_4 = types.InlineKeyboardButton(text='Домино', callback_data='third')
            third_5 = types.InlineKeyboardButton(text='Обсидиан', callback_data='third')
            third_6 = types.InlineKeyboardButton(text='Даймонд', callback_data='third')
            third_7 = types.InlineKeyboardButton(text='Мелодия', callback_data='third')
            third_8 = types.InlineKeyboardButton(text='Эраклион', callback_data='third')
            third_9 = types.InlineKeyboardButton(text='Зенит', callback_data='third')
            qbord.add(third_1)
            qbord.add(third_2)
            qbord.add(third_3)
            qbord.add(third_4)
            qbord.add(third_5)
            qbord.add(third_6)
            qbord.add(third_7)
            qbord.add(third_8)
            qbord.add(third_9)
            bot.send_message(call.message.chat.id, 'Какая планета из мира Винкс нравится Вам больше всего?',
                             reply_markup=qbord)
            state = 3
        elif call.data == 'after_third':
            call.data = 'waiting'
            bot.send_message(call.message.chat.id, 'Продолжаем квиз!')
            qbord = types.ReplyKeyboardMarkup()
            fourth_1 = types.InlineKeyboardButton(text='Несса', callback_data='fourth')
            fourth_2 = types.InlineKeyboardButton(text='Мирта', callback_data='fourth')
            fourth_3 = types.InlineKeyboardButton(text='Нова', callback_data='fourth')
            fourth_4 = types.InlineKeyboardButton(text='Галатея', callback_data='fourth')
            fourth_5 = types.InlineKeyboardButton(text='Миели', callback_data='fourth')
            fourth_6 = types.InlineKeyboardButton(text='Дафна', callback_data='fourth')
            fourth_7 = types.InlineKeyboardButton(text='Политея', callback_data='fourth')
            fourth_8 = types.InlineKeyboardButton(text='Мавилла', callback_data='fourth')
            qbord.add(fourth_1)
            qbord.add(fourth_2)
            qbord.add(fourth_3)
            qbord.add(fourth_4)
            qbord.add(fourth_5)
            qbord.add(fourth_6)
            qbord.add(fourth_7)
            qbord.add(fourth_8)
            bot.send_message(call.message.chat.id, 'А какая фея среди представленных Вам нравится больше всего?',
                             reply_markup=qbord)
            state = 4
        elif call.data == 'after_fourth':
            call.data = 'waiting'
            state = 5
            bot.send_message(call.message.chat.id, 'Продолжаем тестирование!', reply_markup=types.ReplyKeyboardRemove())
            bot.send_message(call.message.chat.id, 'Сколько Вам лет?')
        elif call.data == 'smh':
            call.data = 'waiting'
            qbord = types.ReplyKeyboardMarkup()
            fifth_1 = types.InlineKeyboardButton(text='Рокси', callback_data='smh tho')
            fifth_2 = types.InlineKeyboardButton(text='Моргана', callback_data='smh tho')
            fifth_3 = types.InlineKeyboardButton(text='Диана', callback_data='smh tho')
            fifth_4 = types.InlineKeyboardButton(text='Небула', callback_data='smh tho')
            fifth_5 = types.InlineKeyboardButton(text='Аврора', callback_data='smh tho')
            fifth_6 = types.InlineKeyboardButton(text='Сибилла', callback_data='smh tho')
            qbord.add(fifth_1)
            qbord.add(fifth_2)
            qbord.add(fifth_3)
            qbord.add(fifth_4)
            qbord.add(fifth_5)
            qbord.add(fifth_6)
            bot.send_message(call.message.chat.id, 'А из этих фей?',
                             reply_markup=qbord)
            state = 4.5
        elif call.data == 'after_fifth':
            call.data = 'waiting'
            qbord = types.ReplyKeyboardMarkup()
            sixth_1 = types.InlineKeyboardButton(text='Скай', callback_data='sixth')
            sixth_2 = types.InlineKeyboardButton(text='Ривен', callback_data='sixth')
            sixth_3 = types.InlineKeyboardButton(text='Некс', callback_data='sixth')
            sixth_4 = types.InlineKeyboardButton(text='Гелия', callback_data='sixth')
            sixth_5 = types.InlineKeyboardButton(text='Рой', callback_data='sixth')
            sixth_6 = types.InlineKeyboardButton(text='Брендон', callback_data='sixth')
            sixth_7 = types.InlineKeyboardButton(text='Тимми', callback_data='sixth')
            sixth_8 = types.InlineKeyboardButton(text='Набу', callback_data='sixth')
            qbord.add(sixth_1)
            qbord.add(sixth_2)
            qbord.add(sixth_3)
            qbord.add(sixth_4)
            qbord.add(sixth_5)
            qbord.add(sixth_6)
            qbord.add(sixth_7)
            qbord.add(sixth_8)
            bot.send_message(call.message.chat.id, 'Кто из этих персонажей Вам нравится больше всего?',
                             reply_markup=qbord)
            state = 6
        elif call.data == 'after_sixth':
            call.data = 'waiting'
            qbord = types.ReplyKeyboardMarkup()
            seventh_1 = types.InlineKeyboardButton(text='Блум', callback_data='seventh')
            seventh_2 = types.InlineKeyboardButton(text='Стелла', callback_data='seventh')
            seventh_3 = types.InlineKeyboardButton(text='Текна', callback_data='seventh')
            seventh_4 = types.InlineKeyboardButton(text='Муза', callback_data='seventh')
            seventh_5 = types.InlineKeyboardButton(text='Лейла', callback_data='seventh')
            seventh_6 = types.InlineKeyboardButton(text='Флора', callback_data='seventh')
            qbord.add(seventh_1)
            qbord.add(seventh_2)
            qbord.add(seventh_3)
            qbord.add(seventh_4)
            qbord.add(seventh_5)
            qbord.add(seventh_6)
            bot.send_message(call.message.chat.id, 'Отметьте Вашу любимую фею Винкс',
                             reply_markup=qbord)
            state = 7
        elif call.data == 'final':
            bot.send_message(call.message.chat.id, 'Вы прошли квиз! Вы:')
            time.sleep(2)
            bot.send_message(call.message.chat.id, '...')
            time.sleep(2)
            sorted_probability = dict(
                sorted(users[str(call.message.chat.id)].items(), key=operator.itemgetter(1), reverse=True))
            fairy = WinxClubReversed[list(sorted_probability.keys())[0]]
            bot.send_message(call.message.chat.id, fairy + '!')
            X = list()
            Y = list()
            number = sum(list(sorted_probability.values()))
            for i in list(sorted_probability.keys()):
                print(i)
                i_fairy = WinxClubReversed[i]
                X.append(i_fairy)
            for i in list(sorted_probability.values()):
                i_percent = i / number * 100
                Y.append(i_percent)
            plt.plot(X, Y)
            plt.title('Как сильно Вы похожи на феечек?')
            plt.ylabel('Процент схожести')
            plt.xlabel('Феечки')
            if os.path.exists('/home/IgorCigoreta/mysite/' + str(call.message.chat.id) + '.png'):
                os.remove('/home/IgorCigoreta/mysite/' + str(call.message.chat.id) + '.png')
            plt.savefig('/home/IgorCigoreta/mysite/' + str(call.message.chat.id) + '.png')
            plot = open('/home/IgorCigoreta/mysite/' + str(call.message.chat.id) + '.png', 'rb')
            bot.send_photo(call.message.chat.id, plot)
            plt.clf()
            time.sleep(3)
            with open('/home/IgorCigoreta/mysite/adj.txt', 'r', encoding='utf-8') as f:
                all_adj = f.read().split(', ')
                adj = set()
                adj.add(random.choice(all_adj))
                adj.add(random.choice(all_adj))
                adj.add(random.choice(all_adj))
                adj.add(random.choice(all_adj))
                if len(adj) < 4:
                    while len(adj) < 4:
                        adj.add(random.choice(all_adj))
                        adj.add(random.choice(all_adj))
                        adj.add(random.choice(all_adj))
                        adj.add(random.choice(all_adj))
                adj_list = list()
                for i in adj:
                    adj_list.append(i)
            keyboard_final = types.InlineKeyboardMarkup()
            another_try = types.InlineKeyboardButton(text='ДА', callback_data='starting')
            leave_me = types.InlineKeyboardButton(text='НЕТ', callback_data='leave_me')
            keyboard_final.add(another_try)
            keyboard_final.add(leave_me)
            bot.send_message(call.message.chat.id, 'Спасибо, что прошли опрос! Хотите пройти его еще раз?',
                             reply_markup=keyboard_final)
        elif call.data == 'leave_me':
            state = 0.5
            call.data = 'waiting'
            bot.send_message(call.message.chat.id, 'Спасибо еще раз!')


@app.route('/', methods=['GET', 'HEAD'])
def index():
    return 'ok'


@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)

if __name__ == '__main__':
    bot.polling(none_stop=True)