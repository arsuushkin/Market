import telebot
from telebot import types
#from telethon import TelegramClient, events

# Замените 'YOUR_BOT_TOKEN' на фактический токен вашего бота
bot = telebot.TeleBot('6057765064:AAEjWqOFQ23yjdxKn-VSoG7FWSdp1Iujsq4')

# Задайте идентификатор чата администратора
admin_chat_id = '455499371'

api_id = 'YOUR_API_ID'
api_hash = 'YOUR_API_HASH'

user_data = {}
contact_data = {}
shop_rules = [
    f"Правило 1: 🚨 ПРИМЕРКИ НЕТ🚨(если померить одну вещь 20 раз, она будет терять товарный вид) просите замеры✅ \n",
    f"Правило 2: 🚨Обмена и Возврата нет🚨\n",
    f"Правило 3: По самовывозу разговаривать с администраторами(только по полной предоплате, без оплаты нет самовывоза) такие условия, чтобы отсечь людей которые просто договариваются и не приезжают в назначенное время и перестают отвечать! \n",
    f"Правило 4: Доставка так же осуществляется только по полной предоплате  \n"
]

@bot.message_handler(func=lambda message: message.text == '/start')
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('Сделать заказ')
    button2 = types.KeyboardButton('Статус заказа')
    button3 = types.KeyboardButton('Связаться с администратором')
    button4 = types.KeyboardButton('Выбрать нужный товар')
    markup.add(button4)
    markup.add(button1)
    markup.add(button2, button3)
    bot.send_message(message.chat.id, 'Добро пожаловать! Что вы хотите сделать?', reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'Выбрать нужный товар')
def start_choose(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_brand = types.KeyboardButton('Бренд')
    button_categori = types.KeyboardButton('Категория')
    markup.add(button_brand, button_categori)
    bot.send_message(message.chat.id, 'Здравствуйте, вы можете выбрать товар по категории или по бренду:', reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'Бренд')
def process_brand(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_Nike = types.KeyboardButton('Nike')
    button_Adidas = types.KeyboardButton('Adidas')
    button_Puma = types.KeyboardButton('Puma')
    button_Hoka = types.KeyboardButton('Hoka')
    button_Asics = types.KeyboardButton('Asics')
    button_New_Balance = types.KeyboardButton('New Balance')
    markup.add(button_Nike, button_Adidas)
    markup.add(button_New_Balance, button_Puma)
    markup.add(button_Asics, button_Hoka)
    bot.send_message(message.chat.id, 'Выберете нужный вам бренд:', reply_markup=markup)
    bot.register_next_step_handler(message, process_categori)

@bot.message_handler(func=lambda message: message.text == 'Категория')
def process_categori(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_Life_style = types.KeyboardButton('LifeStyle')
    button_Basketball = types.KeyboardButton('Баскетбол')
    button_football = types.KeyboardButton('Футбол')
    button_run = types.KeyboardButton('Бег')
    button_show = types.KeyboardButton('Показать Все')
    markup.add(button_Life_style, button_Basketball)
    markup.add( button_football, button_run)
    markup.add(button_show)
    bot.send_message(message.chat.id, 'Выберете нужную вам категорию:', reply_markup=markup)
    bot.register_next_step_handler(message,process_show)

def process_show(message):
    bot.send_message(message.chat.id,'я еще не допер, скоро все сделаю')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_main_menu = types.KeyboardButton('Вернуться в главное меню')
    markup.add(button_main_menu)
    bot.send_message(message.chat.id, 'Что вы хотите сделать дальше?', reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in ['Nike', 'Adidas', 'Puma', 'Hoka', 'Asics', 'New Balance'])
def process_brand_selected(message):
    # Здесь обработайте выбор бренда и отправьте результат пользователю
    #bot.send_message(message.chat.id, f'Вы выбрали бренд: {message.text}')
    bot.register_next_step_handler(message,process_categori_selected)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_main_menu = types.KeyboardButton('Вернуться в главное меню')
    markup.add(button_main_menu)
    bot.send_message(message.chat.id, 'Что вы хотите сделать дальше?', reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in ['LifeStyle', 'Баскетбол', 'Футбол', 'Бег','Показать Все'])
def process_categori_selected(message):
    # Здесь обработайте выбор категории и отправьте результат пользователю
    bot.send_message(message.chat.id, f'Вы выбрали категорию: {message.text}')

@bot.message_handler(func=lambda message: message.text == 'Сделать заказ')
def process_info(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_agree = types.KeyboardButton('Согласен')
    button_disagree = types.KeyboardButton('Не согласен')
    markup.add(button_agree, button_disagree)
    for i in range(len(shop_rules)):
        bot.send_message(message.chat.id, shop_rules[i], reply_markup=markup)
    bot.send_message(message.chat.id, 'Согласны ли вы с правилами магазина?', reply_markup=markup)
    bot.register_next_step_handler(message, process_agreement)

def process_agreement(message):
    agreement = message.text
    if agreement == 'Согласен':
        bot.send_message(message.chat.id, 'Введите номер артикула заказа:')
        bot.register_next_step_handler(message, process_article_number)
    else:
        bot.send_message(message.chat.id, 'Вы не согласны с правилами магазина.')
        start(message)

def process_article_number(message):
    article_number = message.text
    user_data[message.chat.id] = {'article_number': article_number}
    bot.send_message(message.chat.id, 'Введите размер ноги в сантиметрах:')
    bot.register_next_step_handler(message, process_foot_size)

def process_foot_size(message):
    foot_size = message.text
    user_data[message.chat.id]['foot_size'] = foot_size
    bot.send_message(message.chat.id, 'Введите ФИО (Фамилия Имя Отчество) в одной строке:')
    bot.register_next_step_handler(message, process_full_name)


def process_full_name(message):
    full_name = message.text
    user_data[message.chat.id]['full_name'] = full_name
    bot.send_message(message.chat.id, 'Введите адрес:')
    bot.register_next_step_handler(message, process_address)

def process_address(message):
    address = message.text
    user_data[message.chat.id]['address'] = address
    bot.send_message(message.chat.id, 'Введите ссылку на ваш профиль в Telegram для связи:')
    bot.register_next_step_handler(message, process_telegram_profile)

def process_telegram_profile(message):
    telegram_profile = message.text
    user_data[message.chat.id]['telegram_profile'] = telegram_profile
    send_order_form(message)

def send_order_form(message):
    if 'article_number' not in user_data[message.chat.id]:
        bot.send_message(message.chat.id, 'Не удалось получить информацию о номере артикула заказа.')
        return

    if 'foot_size' not in user_data[message.chat.id]:
        bot.send_message(message.chat.id, 'Не удалось получить информацию о размере ноги.')
        return


    if 'full_name' not in user_data[message.chat.id]:
        bot.send_message(message.chat.id, 'Не удалось получить информацию о ФИО.')
        return

    if 'address' not in user_data[message.chat.id]:
        bot.send_message(message.chat.id, 'Не удалось получить информацию об адресе.')
        return

    if 'telegram_profile' not in user_data[message.chat.id]:
        bot.send_message(message.chat.id, 'Не удалось получить информацию о профиле Telegram.')
        return

    order_details = f"Номер артикула: {user_data[message.chat.id]['article_number']}\n" \
                    f"Размер ноги: {user_data[message.chat.id]['foot_size']} см\n" \
                    f"ФИО: {user_data[message.chat.id]['full_name']}\n" \
                    f"Адрес: {user_data[message.chat.id]['address']}\n" \
                    f"Ссылка на Telegram профиль: {user_data[message.chat.id]['telegram_profile']}\n"

    bot.send_message(message.chat.id, 'Спасибо! Вот ваша анкета заказа:')
    bot.send_message(message.chat.id, order_details)

    bot.send_message(admin_chat_id, 'Новая анкета заказа:')
    bot.send_message(admin_chat_id, order_details)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_main_menu = types.KeyboardButton('Вернуться в главное меню')
    button_order_status = types.KeyboardButton('Статус заказа')
    markup.add(button_main_menu, button_order_status)
    bot.send_message(message.chat.id, 'Что вы хотите сделать дальше?', reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'Статус заказа')
def check_order_status(message):
    bot.send_message(message.chat.id, 'Введите номер заказа:')
    bot.register_next_step_handler(message, process_order_status)

def process_order_status(message):
    order_number = message.text
    user_data[message.chat.id] = {'order_number': order_number}
    bot.send_message(message.chat.id, 'Введите ФИО (Фамилия Имя Отчество) в одной строке:')
    bot.register_next_step_handler(message, process_full_name_status)

def process_full_name_status(message):
    full_name = message.text
    user_data[message.chat.id]['full_name'] = full_name
    bot.send_message(message.chat.id, 'Введите ссылку на ваш профиль в Telegram для связи:')
    bot.register_next_step_handler(message, process_telegram_profile_status)

def process_telegram_profile_status(message):
    telegram_profile = message.text
    user_data[message.chat.id]['telegram_profile'] = telegram_profile
    send_order_status(message)

def send_order_status(message):
    if 'order_number' not in user_data[message.chat.id]:
        bot.send_message(message.chat.id, 'Не удалось получить информацию о номере заказа.')
        return

    if 'full_name' not in user_data[message.chat.id]:
        bot.send_message(message.chat.id, 'Не удалось получить информацию о ФИО.')
        return

    if 'telegram_profile' not in user_data[message.chat.id]:
        bot.send_message(message.chat.id, 'Не удалось получить информацию о профиле Telegram.')
        return

    order_details = f"Номер заказа: {user_data[message.chat.id]['order_number']}\n" \
                    f"ФИО: {user_data[message.chat.id]['full_name']}\n" \
                    f"Ссылка на Telegram профиль: {user_data[message.chat.id]['telegram_profile']}\n"

    bot.send_message(message.chat.id, 'Спасибо! Вот ваша анкета заказа:')
    bot.send_message(message.chat.id, order_details)

    bot.send_message(admin_chat_id, 'Новая анкета заказа:')
    bot.send_message(admin_chat_id, order_details)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_main_menu = types.KeyboardButton('Вернуться в главное меню')
    button_order_status = types.KeyboardButton('Статус заказа')
    markup.add(button_main_menu, button_order_status)
    bot.send_message(message.chat.id, 'Что вы хотите сделать дальше?', reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'Связаться с администратором')
def process_call_reason(message):
    bot.send_message(message.chat.id, 'По какому вопросу вы хотите связаться с администратором?')
    bot.register_next_step_handler(message, process_call_reason_details)

def process_call_reason_details(message):
    call_reason = message.text
    contact_data[message.chat.id] = {'call_reason': call_reason}
    bot.send_message(message.chat.id, 'Введите ФИО (Фамилия Имя Отчество) в одной строке:')
    bot.register_next_step_handler(message, process_full_name_and_profile)

def process_full_name_and_profile(message):
    full_name = message.text
    contact_data[message.chat.id]['full_name'] = full_name
    bot.send_message(message.chat.id, 'Введите ссылку на ваш профиль в Telegram для связи:')
    bot.register_next_step_handler(message, process_telegram_profile_contact)

def process_telegram_profile_contact(message):
    telegram_profile = message.text
    contact_data[message.chat.id]['telegram_profile'] = telegram_profile
    send_contact_request(message)

def send_contact_request(message):
    if 'call_reason' not in contact_data[message.chat.id]:
        bot.send_message(message.chat.id, 'Не удалось получить информацию о причине обращения.')
        return

    if 'full_name' not in contact_data[message.chat.id]:
        bot.send_message(message.chat.id, 'Не удалось получить информацию о ФИО.')
        return

    if 'telegram_profile' not in contact_data[message.chat.id]:
        bot.send_message(message.chat.id, 'Не удалось получить информацию о профиле Telegram.')
        return

    contact_details = f"Причина обращения: {contact_data[message.chat.id]['call_reason']}\n" \
                      f"ФИО: {contact_data[message.chat.id]['full_name']}\n" \
                      f"Ссылка на Telegram профиль: {contact_data[message.chat.id]['telegram_profile']}\n"

    bot.send_message(message.chat.id, 'Спасибо за ваше обращение! С вами скоро свяжутся.')
    bot.send_message(admin_chat_id, 'С вами хотят связаться:')
    bot.send_message(admin_chat_id, contact_details)

@bot.message_handler(func=lambda message: message.text == 'Вернуться в главное меню')
def return_to_main_menu(message):
    start(message)

bot.polling(none_stop=True, timeout=60)
