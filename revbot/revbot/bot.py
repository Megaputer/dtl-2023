import polyanalyst6api as pa
from telebot import types, TeleBot

bot = TeleBot('YOUR_TELEGRAM_BOT_ID_GOES_HERE')

api = pa.API('https://dtl.pa6.megaputer.ru', 'YOUR_USERNAME', 'YOUR_PASSWORD')
api.login()
prj = api.project('8006a31b-f92e-4d61-a24a-d1d1fdea5aea')

reviews = {}


@bot.message_handler(commands=['start', 'help'])
def start(msg):
    bot.send_message(msg.from_user.id, f'👋 Привет, {msg.from_user.first_name}!')
    bot.send_message(msg.from_user.id, 'Введи номер постамата (число)')
    bot.register_next_step_handler(msg, get_review, userid=msg.from_user.id)


def get_review(msg, userid):
    bot.send_message(msg.from_user.id, 'Какой отзыв хочешь оставить? (латинница)')
    bot.register_next_step_handler(msg, save_review, userid=userid, address=msg.text)


def save_review(msg, userid, address):
    keyboard = types.InlineKeyboardMarkup()
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
    keyboard.add(key_yes)
    key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
    keyboard.add(key_no)

    review = msg.text
    reviews[userid] = [address, review]

    question = f'Ты хочешь оставить следующий отзыв?\nАдрес: `{address}`\nОтзыв: `{review}`'
    bot.send_message(msg.from_user.id, text=question, reply_markup=keyboard,  parse_mode='MarkdownV2')


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    _id = call.message.chat.id
    if call.data == 'yes':
        write_review(_id, reviews[_id][0], reviews[_id][1])
        bot.send_message(call.message.chat.id, 'Отзыв успешно создан')
    else:
        bot.send_message(call.message.chat.id, 'Попробуй заново, напиши /start')
        reviews[_id] = None


def write_review(userid, address, review):
    # prj.parameters('Parameters (2)').set('DataSource/MANUALINPUT', parameters={'userid': userid, 'address': address, 'review': review})
    # prj.execute('Parameters (2)', wait=True)  # ожидается только для текущего пользователя
    pass


bot.polling(none_stop=True, interval=0)
