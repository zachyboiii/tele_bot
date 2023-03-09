import pandas as pd
import telebot
import time
from flask import Flask
from datetime import date

app = Flask(__name__)

@app.route('/hello')
def hello():
    return 'Hello'

token = "5967749948:AAHYTwy8L3bDP2sdkAEVkCgAmE3s643Fmao" 
bot = telebot.TeleBot(token)
   
@bot.message_handler(commands = ['start']) #create /start command
def help(message):
    bot.send_message(message.chat.id,"Welcome to NYCG events reminder by Zac!\nThis bot helps send scheduled reminders on birthdays or other stuff.\nHow to use: /help")
#What the bot sends on /start command
    
@bot.message_handler(commands = ['help'])
def help(message):
    bot.send_message(message.chat.id, "To start scheduled reminders: /remind")

@bot.message_handler(commands = ['remind'])
def remind(message):
    while True:
        df = pd.read_excel(r'C:\Users\USER\Desktop\Coding\python\NYCG_telebot\NYCG_special_events.xlsx') #read excel data
        df["message"] = df["Who's Involved"]+"'s "+df["Type"] #append to create fully message
        df["Day"] = pd.to_datetime(df['Day'])
        current_day = date.today().day
        current_month = date.today().month
        new = df.loc[(df['Day'].dt.day == current_day) & (df["Day"].dt.month == current_month)]
        all_events = new["message"]
        if new.empty == True:
            bot.send_message(message.chat.id, "No events today :)")
        else:
            bot.send_message(message.chat.id, "Events today:\n" + "\n".join(all_events.values))
        time.sleep(86400) #sends reminder every 24h

#@bot.message_handler(commands = ['end'])
#def end(message):
    #bot.send_message(message.chat.id, "Bot has been terminated. \nThank you for using NYCG Special Events bot, God bless :)")
    #bot.stop_polling()

if __name__ == '__main__':
    app.run()

bot.polling() #keeps bot constantly running


        
