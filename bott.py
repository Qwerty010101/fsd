import telebot
from telebot import types

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.cryptocurrencies import CryptoCurrencies
from alpha_vantage.sectorperformance import SectorPerformances
from alpha_vantage.techindicators import TechIndicators
import pandas as pd
import os, sys
import pymongo
from alphaVantageAPI.alphavantage import AlphaVantage

token = "616826761:AAG_BonntZ-MRGhcZSLSQZQ6YPzCWTmJWUQ"
bot = telebot.TeleBot(token)

items = []


@bot.message_handler(func=lambda message: True, commands=['start'])
def Start(message):
    try:
        markup = types.ReplyKeyboardMarkup()
        markup.row('info', 'rate', 'tech', 'portfolio')
        bot.send_message(message.chat.id, "chose one option", reply_markup=markup)
    except Exception as e:
        markup = types.ReplyKeyboardMarkup()
        markup.row('get back')
        bot.send_message(message.chat.id, "ooops... something got wrong", reply_markup=markup)


@bot.message_handler(regexp="get back")
def back(message):
    try:
        markup = types.ReplyKeyboardMarkup()
        markup.row('info', 'rate', 'tech', 'portfolio')
        bot.send_message(message.chat.id, "chose one option", reply_markup=markup)
    except Exception as e:
        markup = types.ReplyKeyboardMarkup()
        markup.row('get back')
        bot.send_message(message.chat.id, "ooops... something got wrong", reply_markup=markup)

@bot.message_handler(regexp="info")
def info(message):
    bot.send_message(message.chat.id, "")


@bot.message_handler(regexp="rate")
def stocks(message):
    try:
        markup = types.ReplyKeyboardMarkup()
        markup.row('info', 'tech', 'portfolio', 'get back')
        msg = bot.send_message(message.chat.id, "symbol", reply_markup=markup)
        bot.register_next_step_handler(msg, stock_info)
    except Exception as e:
        markup = types.ReplyKeyboardMarkup()
        markup.row('get back')
        bot.send_message(message.chat.id, "ooops... something got wrong", reply_markup=markup)

def stock_info(message):
    try:
        slovo = message.text
        ts = TimeSeries(key='ZBRM5PCHPIYQV8BY', output_format='pandas')
        data, meta_data = ts.get_daily(slovo, outputsize='full')
        data['4. close'].plot()
        plt.title('Intraday Times Series for the ' + slovo + 'stock (1 day)')
        plt.savefig('graph.png')
        plt.close()
        photo = open("graph.png", 'rb')
        bot.send_photo(message.chat.id, photo)
        data, meta_data = ts.get_intraday(slovo, interval='1min', outputsize='full')
        dat, meta_dat = ts.get_daily(slovo, outputsize='full')
        now = pd.DataFrame(data.tail(1))
        now1 = now['4. close']
        nw = str(now1)
        nw1 = nw[28:34]
        nw2 = float(nw1)
        openn = pd.DataFrame(dat.tail(2))
        openn1 = openn['4. close']
        op = str(openn1)
        op1 = op[19:23]
        op2 = float(op1)
        if nw2 >= op2:
            proc = round(100 - ((op2 / nw2) * 100), 2)
            proc1 = str(proc)
            bot.send_message(message.chat.id, slovo + " - $" + nw1 + ' +' + proc1 + '%')
        elif nw2 < op2:
            proc = round(100 - ((nw2 / op2) * 100), 2)
            proc1 = str(proc)
            bot.send_message(message.chat.id, slovo + " - $" + nw1 + ' -' + proc1 + '%')
    except Exception as e:
        markup = types.ReplyKeyboardMarkup()
        markup.row('get back')
        bot.send_message(message.chat.id, "ooops... something got wrong", reply_markup=markup)

@bot.message_handler(regexp="tech")
def technical(message):
    try:
        markup = types.ReplyKeyboardMarkup()
        markup.row('info', 'rate', 'portfolio', 'get back')
        msg = bot.send_message(message.chat.id, "Fill ticker in: ", )
        bot.register_next_step_handler(msg, ticker)
    except Exception as e:
        markup = types.ReplyKeyboardMarkup()
        markup.row('get back')
        bot.send_message(message.chat.id, "ooops... something got wrong", reply_markup=markup)


def ticker(message):
    try:
        global tic
        tic = message.text
        mesg = bot.send_message(message.chat.id, "Fill interval in: ", )
        bot.register_next_step_handler(mesg, graph)
    except Exception as e:
        markup = types.ReplyKeyboardMarkup()
        markup.row('get back')
        bot.send_message(message.chat.id, "ooops... something got wrong", reply_markup=markup)


def graph(message):
    try:
        global interval
        interval = message.text
        markup = types.ReplyKeyboardMarkup()
        markup.row('sma', 'getEMA', 'checkMACD', 'stoch', 'rsi', 'adx')
        bot.send_message(message.chat.id, "_____________", reply_markup=markup)
    except Exception as e:
        markup = types.ReplyKeyboardMarkup()
        markup.row('get back')
        bot.send_message(message.chat.id, "ooops... something got wrong", reply_markup=markup)

@bot.message_handler(regexp="sma")
def tech_info(message):
    try:
        ts = TechIndicators(key='ZBRM5PCHPIYQV8BY', output_format='pandas')
        data, meta_data = ts.get_sma(tic, interval=interval, time_period=60)
        data.plot()
        plt.title('sma indicator for ' + tic + ' stock ' + interval)
        plt.savefig('sma.png')
        plt.close()
        photo = open("sma.png", 'rb')
        bot.send_photo(message.chat.id, photo)
    except Exception as e:
        markup = types.ReplyKeyboardMarkup()
        markup.row('get back')
        bot.send_message(message.chat.id, "ooops... something got wrong", reply_markup=markup)


@bot.message_handler(regexp="getEMA")
def getEMA(message):
    try:
        ts = TechIndicators(key='ZBRM5PCHPIYQV8BY', output_format='pandas')
        data, meta_data = ts.get_ema(tic, interval=interval, time_period=60)
        data.plot()
        plt.title('ema indicator for ' + tic + ' stock')
        plt.savefig('ema.png')
        plt.close()
        photo = open("ema.png", 'rb')
        bot.send_photo(message.chat.id, photo)
    except Exception as e:
        markup = types.ReplyKeyboardMarkup()
        markup.row('get back')
        bot.send_message(message.chat.id, "ooops... something got wrong", reply_markup=markup)


@bot.message_handler(regexp="checkMACD")
def checkMACD(message):
    try:
        ts = TechIndicators(key='ZBRM5PCHPIYQV8BY', output_format='pandas')
        data, meta_data = ts.get_macd(tic, interval=interval)
        data.plot()
        plt.title('MACD indicator for ' + tic + ' stock')
        plt.savefig('MACD.png')
        plt.close()
        photo = open("MACD.png", 'rb')
        bot.send_photo(message.chat.id, photo)
    except Exception as e:
        markup = types.ReplyKeyboardMarkup()
        markup.row('get back')
        bot.send_message(message.chat.id, "ooops... something got wrong", reply_markup=markup)


@bot.message_handler(regexp="stoch")
def stoch(message):
    try:
        ts = TechIndicators(key='ZBRM5PCHPIYQV8BY', output_format='pandas')
        data, meta_data = ts.get_stoch(tic, interval=interval)
        data.plot()
        plt.title('stoch indicator for ' + tic + ' stock')
        plt.savefig('stoch.png')
        plt.close()
        photo = open("stoch.png", 'rb')
        bot.send_photo(message.chat.id, photo)
    except Exception as e:
        markup = types.ReplyKeyboardMarkup()
        markup.row('get back')
        bot.send_message(message.chat.id, "ooops... something got wrong", reply_markup=markup)


@bot.message_handler(regexp="rsi")
def rsi(message):
    try:
        ts = TechIndicators(key='ZBRM5PCHPIYQV8BY', output_format='pandas')
        data, meta_data = ts.get_rsi(tic, interval=interval)
        data.plot()
        plt.title('rsi indicator for ' + tic + ' stock')
        plt.savefig('rsi.png')
        plt.close()
        photo = open("rsi.png", 'rb')
        bot.send_photo(message.chat.id, photo)
    except Exception as e:
        markup = types.ReplyKeyboardMarkup()
        markup.row('get back')
        bot.send_message(message.chat.id, "ooops... something got wrong", reply_markup=markup)


@bot.message_handler(regexp="adx")
def adx(message):
    try:
        ts = TechIndicators(key='ZBRM5PCHPIYQV8BY', output_format='pandas')
        data, meta_data = ts.get_adx(tic, interval=interval)
        data.plot()
        plt.title('adx indicator for ' + tic + ' stock')
        plt.savefig('adx.png')
        plt.close()
        photo = open("adx.png", 'rb')
        bot.send_photo(message.chat.id, photo)
    except Exception as e:
        markup = types.ReplyKeyboardMarkup()
        markup.row('get back')
        bot.send_message(message.chat.id, "ooops... something got wrong", reply_markup=markup)


@bot.message_handler(regexp="portfolio")
def portfolio(message):
    try:
        markup = types.ReplyKeyboardMarkup()
        markup.row('edit', 'show all', 'get back')
        bot.send_message(message.chat.id, "Choose one of options:", reply_markup=markup)
    except Exception as e:
        markup = types.ReplyKeyboardMarkup()
        markup.row('get back')
        bot.send_message(message.chat.id, "ooops... something got wrong", reply_markup=markup)

@bot.message_handler(regexp="edit")
def edit_portfolio(message):
    try:
        markup = types.ReplyKeyboardMarkup()
        markup.row('add stocks', 'clean', 'delete one', 'portfolio')
        bot.send_message(message.chat.id, "Choose one of options:", reply_markup=markup)
    except Exception as e:
        markup = types.ReplyKeyboardMarkup()
        markup.row('get back')
        bot.send_message(message.chat.id, "ooops... something got wrong", reply_markup=markup)

@bot.message_handler(regexp="clean")
def clean(message):
    try:
        msg = bot.send_message(message.chat.id, "removing...")
        items.clear()
        msg = bot.send_message(message.chat.id, "removed")
    except Exception as e:
        markup = types.ReplyKeyboardMarkup()
        markup.row('get back')
        bot.send_message(message.chat.id, "ooops... something got wrong", reply_markup=markup)

@bot.message_handler(regexp="delete one")
def dl(message):
    try:
        msg = bot.send_message(message.chat.id, "write stock that should be deleted" )
        bot.register_next_step_handler(msg, dl_stock)
    except Exception as e:
        markup = types.ReplyKeyboardMarkup()
        markup.row('get back')
        bot.send_message(message.chat.id, "ooops... something got wrong", reply_markup=markup)

def dl_stock(message):
    try:
        dls = message.text
        for i in items:
            if i == dls:
                items.remove(i)
        bot.send_message(message.chat.id, "stock is removed")
    except Exception as e:
        markup = types.ReplyKeyboardMarkup()
        markup.row('get back')
        bot.send_message(message.chat.id, "ooops... something got wrong", reply_markup=markup)

@bot.message_handler(regexp="add stock")
def get_ticket(message):
    try:
        msge = bot.send_message(message.chat.id, "ticket" )
        bot.register_next_step_handler(msge, add_ticket)
        bot.send_message(message.chat.id, "_________")
    except Exception as e:
        markup = types.ReplyKeyboardMarkup()
        markup.row('get back')
        bot.send_message(message.chat.id, "ooops... something got wrong", reply_markup=markup)


def add_ticket(message):
    try:
        global items
        item = message.text
        items.append(item)
    except Exception as e:
        markup = types.ReplyKeyboardMarkup()
        markup.row('get back')
        bot.send_message(message.chat.id, "ooops... something got wrong", reply_markup=markup)

@bot.message_handler(regexp="show all")
def show_stocks(message):
    try:
        ts = TimeSeries(key='ZBRM5PCHPIYQV8BY', output_format='pandas')
        x = 0
        for x in items:
            data, meta_data = ts.get_intraday(x, interval='1min', outputsize='full')
            dat, meta_dat = ts.get_daily(x, outputsize='full')
            now = pd.DataFrame(data.tail(1))
            now1 = now['4. close']
            nw = str(now1)
            nw1 = nw[28:34]
            nw2 = float(nw1)
            openn = pd.DataFrame(dat.tail(2))
            openn1 = openn['4. close']
            op = str(openn1)
            op1 = op[19:23]
            op2 = float(op1)
            if nw2 >= op2:
                proc = round(100 - ((op2 / nw2) * 100), 2)
                proc1 = str(proc)
                bot.send_message(message.chat.id, x + " - $" + nw1 + ' +' + proc1 + '%')
            elif nw2 < op2:
                proc = round(100 - ((nw2 / op2) * 100), 2)
                proc1 = str(proc)
                bot.send_message(message.chat.id, x + " - $" + nw1 + ' -' + proc1 + '%')
    except Exception as e:
        markup = types.ReplyKeyboardMarkup()
        markup.row('get back')
        bot.send_message(message.chat.id, "ooops... something got wrong", reply_markup=markup)


if __name__ == '__main__':
    bot.polling(none_stop=True)

