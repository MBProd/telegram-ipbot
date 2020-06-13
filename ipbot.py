from telegram.ext import Updater, CommandHandler
from requests.exceptions import RequestException
from config import load_json
import requests


class IPBot:

    def __init__(self):
        self.config = load_json()
        self.updater = Updater(self.config['token'], use_context=True)
        dp = self.updater.dispatcher
        dp.add_handler(CommandHandler('getip', self.ip_handler))
        self.updater.start_polling()

    def ip_handler(self, update, context):
        if update.message:
            if str(update.message.chat.id) == str(self.config['chat_id']):
                try:
                    request = requests.get(self.config['ip_service'])
                    print(f'IP requested. ({request.text})')
                    update.message.reply_text(text=request.text)
                except RequestException as e:
                    update.message.reply_text(f'Can\'t get external IP! {e}')

    def idle(self):
        self.updater.idle()


if __name__ == '__main__':
    bot = IPBot()
    bot.idle()
