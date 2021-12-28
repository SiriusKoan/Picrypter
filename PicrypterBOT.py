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
password = "0"

def start(update: Update, context: CallbackContext):
    update.message.reply_text('Welcome to use this converter, '+ update.message.chat.username +".\nPlease follow the installation step on "+
    "https://github.com/SiriusKoan/NYCU-LA-final-project \n" +
    """
    /start - Introduction.
    /end - Clear all changes.
    /password - The random number sender and receiver choose.
    /encrypt - Encrypt your image according to your password.
    Image : The image you long to encrypt.
    """)


    end(update, context)

    
def end(update: Update, context: CallbackContext):
    update.message.reply_text(update.message.chat.username + ", thanks you!")
    password = "0"
    image = Image.new('RGB',size = (200,200))

def encrypt(update: Update, context: CallbackContext):
    global image
    global password
    if(password == "0"):
        update.message.reply_text("Please enter the password!")
        return

    context.bot.send_photo(chat_id=update.message.chat_id,photo=image)

    #this part is to encrypt the image that users give '''

    #init blank variable
    end(update, context)


def Password(update: Update, context: CallbackContext):
    global password
    password = update.message.text[10:].replace('\n', '')


def initImage(update: Update, context: CallbackContext):
    global image
    image = update.message.photo[-1] # the type is string PhotoType
    update.message.reply_text("Please enter the password.\nFormat : \"/password <password>\".")

    #image = Image.open("test.jpg")
    #image.save("test.png","png")

def main():
    updater = Updater('PUT TOKEN', use_context=True)
    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CommandHandler("end", end))
    updater.dispatcher.add_handler(CommandHandler("encrypt",encrypt))
    updater.dispatcher.add_handler(MessageHandler(Filters.photo, initImage))
    updater.dispatcher.add_handler(CommandHandler("password",Password))


    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
