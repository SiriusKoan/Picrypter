import json
import os
import requests
import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram import Update, Bot ,Message
from telegram import KeyboardButton,ReplyKeyboardMarkup
from PIL import Image
from functions import encrypt, decrypt

# import telebot
#from telebot import types

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level = logging.INFO)

image = Image.new('RGB',size = (200,200))
password = "0"
default_image = Image.new('RGB',size = (200,200))

def start(update: Update, context: CallbackContext):
    update.message.reply_text('Welcome to use this converter, '+ update.message.chat.username +".\nPlease follow the installation step on "+
    "https://github.com/SiriusKoan/NYCU-LA-final-project \n" +
    """
    /start - Introduction.
    /end - Clear all changes.
    /password - The random number sender and receiver choose.
    /encrypt - Encrypt your image according to password.
    /decrypt - Decrypt your image according to password.
    Image file : The image you want to encrypt or decrypt.
    """)

    kb = [[KeyboardButton('/image')],
          [KeyboardButton('/password')],
          [KeyboardButton('/encrypt')],
          [KeyboardButton('/decrypt')]]
    kb_markup = ReplyKeyboardMarkup(kb)
    context.bot.send_message(chat_id = update.message.chat_id,
                     text = "Wellcome to use this BOT! ",
                     reply_markup=kb_markup)

    Reset()

    
def end(update: Update, context: CallbackContext):
    global password
    global image
    update.message.reply_text(update.message.chat.username + ", thanks you!")
    password = "0"
    image = Image.new('RGB',size = (200,200))

def Encrypt(update: Update, context: CallbackContext):
    global image
    global password
    if(password == "0"):
        update.message.reply_text("Warning! Fail to encrypt!")
        update.message.reply_text("Remember to press to /encrypt again!\n")
        tellToSendPassword(update,context)
        return

    if(image == default_image):
        update.message.reply_text("Warning! Fail to encrypt!")
        update.message.reply_text("Remember to press to /encrypt again!\n")
        tellToSendImage(update, context)
        return

    update.message.reply_text("Wait a moment...")

    image = encrypt(image,password) # encrypt it
    # init blank variable
    open("after_encryption", "w").write(str(image))
    context.bot.send_document(chat_id = update.message.chat_id, document=image)

    end(update, context)

def Decrypt(update: Update, context: CallbackContext):
    global image
    global password
    if(password == "0"):
        update.message.reply_text("Warning! Fail to decrypt!\n")
        update.message.reply_text("Remember to press to /decrypt again!\n")
        tellToSendPassword(update,context)
        return
    if(image == default_image):
        update.message.reply_text("Warning! Fail to decrypt!")
        update.message.reply_text("Remember to press to /decrypt again!\n")
        tellToSendImage(update, context)
        return

    update.message.reply_text("Wait a moment...")
    # print("test")
    image = decrypt(image,password) # decrypt it
    context.bot.send_document(chat_id=update.message.chat_id, document=image)

    # reset blank variable
    end(update, context)
    


# This part is to remind user to send password or image
def tellToSendImage(update: Update, context: CallbackContext):
    if(image == default_image):
        update.message.reply_text("Please send the image file.")


def tellToSendPassword(update: Update, context: CallbackContext):
    if(password == "0"):
        update.message.reply_text("Please enter the password.")


# This part is to init password or image
def initPassword(update: Update, context: CallbackContext):
    global password
    global image
    if(update.message.text[0] != '/'):
        password = update.message.text[:].replace('\n', '')
        update.message.reply_text("Your password is : " + password + ".")

        if(image == default_image):
           tellToSendImage( update, context ) 
        else :
            update.message.reply_text("/encrypt or /decrypt?")

def initImage(update: Update, context: CallbackContext):
    global image
    global size
    print(update.message)
    image = context.bot.getFile(update.message.document.file_id) # the type is string PhotoType
    print(image,dir(image))
    # print(update.message.photo[-1], dir(update.message.photo[-1]))
    image = requests.get(image.file_path).content
    # context.bot.send_photo(chat_id=update.message.chat_id, photo=image)
    open("before", "w").write(str(image))
    # print(image)
    # image = context.bot.getFile(update.message.photo[-1].file_id)
    # image = Image.open("test.jpg")
    # image.save("test.png","png")
    update.message.reply_text("Image received.")
    if(password == "0"):
        tellToSendPassword(update, context)
    else :
        update.message.reply_text("/encrypt or /decrypt?")

def warningImage(update: Update, context: CallbackContext):
    update.message.reply_text(update.message.chat.username,', please send the image file！')

def Reset():
    global password
    global image
    password = "0"
    image = Image.new('RGB',size = (200,200))

def main():
    updater = Updater('5044835888:AAFHiSZo-LLZggskwgsORYFnBn-eTMTC2b8', use_context=True)
    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CommandHandler("end", end))
    updater.dispatcher.add_handler(CommandHandler("encrypt",Encrypt))
    updater.dispatcher.add_handler(CommandHandler("decrypt",Decrypt))

    updater.dispatcher.add_handler(CommandHandler("password",tellToSendPassword))
    updater.dispatcher.add_handler(CommandHandler("image",tellToSendImage))
    
    updater.dispatcher.add_handler(MessageHandler(Filters.document, initImage))
    updater.dispatcher.add_handler(MessageHandler(Filters.photo, warningImage))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, initPassword))


    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()