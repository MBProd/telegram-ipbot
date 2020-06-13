from telegram.ext import Updater, MessageHandler, Filters
from telegram.error import InvalidToken
from getpass import getpass
import json


def interactive_config():
    services = ['https://api.ipify.org/', 'https://ident.me/',
                'http://myip.dnsomatic.com/', 'https://checkip.amazonaws.com/']
    print('Hello! to start using ipbot, we need some information.')
    print('First, we need your token.')
    while True:
        token = getpass('token: ')
        try:
            updater = Updater(token, use_context=True)
            dp = updater.dispatcher
            dp.add_handler(MessageHandler(Filters.text, reply_handler))
            updater.start_polling()
            break
        except InvalidToken:
            print('Token is invalid!')
    print('Now input your User ID.\nThe bot will reply any messages with your User ID.'
          '\nSend a random message to get your User ID.')
    id = input('ID: ')
    print('Perfect! Which service do you want to use?')
    service = 1
    for s in services:
        print(f'{service}. {s}')
        service += 1
    while True:
        try:
            service = int(input('Service: '))
            if service < 1 or service > len(services):
                print('Please use a number within range.')
                continue
            break
        except ValueError:
            print('Please use a number.')
    print(f'Using {services[service - 1]}.')
    config = dict()
    config['token'] = token
    config['chat_id'] = id
    config['ip_service'] = services[service - 1]
    updater.stop()
    try:
        with open('config.json', 'w') as f:
            json.dump(config, f)
        print('You can now use this bot. Simply use command /getip to get the bot\'s current IP.')
    except Exception as e:
        print(f'Cant\' save config! The config setup will rerun next time.\n{e}')
    return config


def reply_handler(update, context):
    update.message.reply_text(text=f'User: {update.message.chat.username} ID: {update.message.chat.id}')


def load_json():
    try:
        with open('config.json') as f:
            dikt = json.load(f)
        if 'chat_id' not in dikt:
            raise Exception('Invalid config! no chat_id found.')
        if 'token' not in dikt:
            raise Exception('Invalid config! no token found.')
        if 'ip_service' not in dikt:
            raise Exception('Invalid config! no ip_service found.')
        return dikt
    except FileNotFoundError:
        print('Config not found. Let\'s create one!')
        return interactive_config()
    except Exception as e:
        print(f'Can\'t load config! {e}')
        return interactive_config()
