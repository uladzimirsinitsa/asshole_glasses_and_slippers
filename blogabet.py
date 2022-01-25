
import os
import sys
import time
import pickle

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from dotenv import load_dotenv

import pymongo

load_dotenv()

PATH_DRIVER = os.environ['PATH_DRIVER']
URL = 'https://sabobic.blogabet.com/'
SERVER = os.environ['SERVER']


#service = Service(PATH_DRIVER)
#driver = webdriver.Firefox(service=service)
#driver.get('https://blogabet.com/')
#cookies = pickle.load(open("cookies_BLOGABET.pkl", "rb"))
#for cookie in cookies:
    #driver.add_cookie(cookie)


client = pymongo.MongoClient(SERVER, serverSelectionTimeoutMS=5000)
db = client.blogabet_DB
lines = db.lines


def read_file():
    with open('C:\\Projects\\blogabet_row.txt', 'r', encoding='utf-8') as file:
        text = file.read()
    return text

def read_profile():
    with open('C:\\Projects\\sabobic.html', 'r', encoding='utf-8') as file:
        text_profile = file.read()
    return text_profile


def parsing_data(text) -> tuple:
    soup = BeautifulSoup(text, 'lxml')
    names = soup.select('span > a')
    return [name.getText() for name in names]


def get_data(text_profile):
    soup = BeautifulSoup(text_profile, 'lxml')

    name = URL[8:-14]

    url = URL

    number_of_bets = int(soup.find('h4').find('span').getText())

    roi =  int(soup.find(id="header-yield").getText()[1:-1])

    profit = soup.find(id='header-profit').getText()
    if profit[0] == '+':
        profit = int(profit[1:])

    odds_avg = 2.016
    winrate = 53
    bets = soup.find_all('div', attrs={'class': 'col-xs-12 no-padding'})

    while any(bets):

        item = bets.pop()

        bet = item.find('a').text

        res = item.find('#text')
        print(res)

        url_bet = item.find('a').get('href')

        coef = float(item.find('span', class_='feed-odd').text)

        book = item.find('a', class_='label label-primary').text

        for_date = soup.find_all('li', attrs={'class': 'block media _feedPick feed-pick'})
        date = for_date.pop().find('small', class_='bet-age text-muted').text

        data = {
        'name': name,
        'url': url,
        'number_of_bets': number_of_bets,
        'roi': roi,
        'profit': profit,
        'odds_avg': odds_avg,
        'winrate': winrate,
        'bet': bet,
        'coef': coef,
        'book': book,
        'date': date,
        'url_bet': url_bet
        }

        lines.insert_one(data)




def main():
    text = read_file()
    data = parsing_data(text)
    text_profile = read_profile()
    get_data(text_profile)


if __name__ == '__main__':
    main()
