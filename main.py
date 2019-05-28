import telebot
from telebot.apihelper import ApiException

import settings
from functions import *
from errors import *

bot = telebot.TeleBot(settings.TOKEN)
assets = get_asset_dictionary()
currencies = requests.get()


@bot.message_handler(commands=['start'])
def message_handler(message):
    bot.send_message(message.chat.id,
                     "Hello!\nI am a CurrencyConverterBot!")


@bot.message_handler(commands=['help'])
def message_handler(message):
    bot.send_message(message.chat.id,
                     "Type codes of currencies like `'usd to btc'` or `'UAH -> EUR'` to get recent currency rates.\n\n"
                     "Add some value to left currency to convert it to another.\nFor example: `'10 eur -> usd'`.",
                     parse_mode='markdown')


@bot.message_handler(content_types=['text'])
def message_handler(message):
    is_support = check_support(message)
    if is_support:
        return

    result = parse_text(message.text, assets)

    print(result)
    if not result == few_arguments \
            and asset_not_found not in result \
            and left_asset_value_error not in result:
        rate = get_rate(result[0][0], result[1][0])
        conversion = rate * float(result[0][1])
        out = "{0} {1} -> {2} {3}".format(result[0][1],
                                          result[0][0],
                                          conversion if conversion > 0.00001 else "%.6f" % conversion,
                                          result[1][0])
    else:
        out = result + "\n\nTry /help"

    bot.send_message(message.from_user.id,
                     out,
                     parse_mode='markdown')


def check_support(message):
    if message.text == '/support':
        bot.send_message(message.chat.id,
                         "Please, write your message text like this: `/support message`",
                         parse_mode='markdown')
        return True
    if '/support ' in message.text:
        try:
            bot.send_message(settings.support_id,
                             "[{0}](t.me/{1}) said:\n\n{2}".format(message.from_user.first_name,
                                                                   message.from_user.username,
                                                                   message.text.replace('/support ', '')),
                             parse_mode='markdown')
            bot.send_message(message.from_user.id,
                             "Your message was sent! Wait for answer.")
        except ApiException:
            bot.send_message(message.from_user.id,
                             "Something is wrong. Check if your message is correct and isn't empty.")
        return True
    return False


bot.send_message(settings.support_id, "I'm alive!")
bot.polling(none_stop=True, interval=0)
