from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram import Update, Bot ,Message
import json
import os
import logging

from PIL import Image

# import telebot
#from telebot import types

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level = logging.INFO)

image = Image.new('RGB',size = (200,200))

def start(update: Update, context: CallbackContext):
    update.message.reply_text('Welcome to use this converter, '+ update.message.chat.username +", please follow the installation step on "+
    'https://github.com/wujoe0415/telegrambot_converter/blob/main/README.md')

    
def end(update: Update, context: CallbackContext):
    update.message.reply_text(update.message.chat.username + ", thanks you!")

def encrypt(update: Update, context: CallbackContext):
    update.message.reply_text(update.message.chat.username + ", thank you!")
    context.bot.send_photo(chat_id=update.message.chat_id,photo=image)
    #this part is to encrypt the image that users give '''

def initImage(update: Update, context: CallbackContext):
    global image
    image = update.message.photo[-1]
    #image = Image.open("test.jpg")
    #image.save("test.png","png")

def main():
    updater = Updater('5044835888:AAFHiSZo-LLZggskwgsORYFnBn-eTMTC2b8', use_context=True)
    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CommandHandler("end", end))
    updater.dispatcher.add_handler(CommandHandler("encrypt",encrypt))
    updater.dispatcher.add_handler(MessageHandler(Filters.photo, initImage))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()