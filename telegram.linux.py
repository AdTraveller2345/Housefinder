from bs4 import BeautifulSoup
import requests
from telegram import Bot
import sqlite3
import time
import random

api_token = ''  # API token for your bot
chat_id = ''  # Your Telegram chat ID
# set your search preferences
city_names = ('eindhoven','tilburg','helmond','den-bosch')  # preferred cities
room_types = ('a','h','r','s')  # preferred type of accommodation 'a' = apartment, 'h' = house, 'r' = room 's' = studio
refresh_interval = [1,2]  # set a random interval for how often should the program rerun itself
max_rent = 1100 #set your max rent
while True:
    # set up connection with the database
    connection = sqlite3.connect("listings.db")  # you can specify the location and name of the database
    cursor = connection.cursor()

    # create table and fill it with contents from pararius
    cursor.execute("CREATE TABLE IF NOT EXISTS room (link TEXT PRIMARY KEY, city TEXT,type TEXT, price INT, notified BOOLEAN, UNIQUE(link))")
    for city in city_names:
        html_text = requests.get('https://www.pararius.com/apartments/' + city).text
        soup = BeautifulSoup(html_text, 'lxml')
        listings = soup.find_all('li', class_="search-list__item search-list__item--listing")
        for a in listings[:5]:
            link = a.find('a', class_="listing-search-item__link listing-search-item__link--title")['href']
            for element in a.text.strip().split():
                if element.startswith('€'):
                    price = int(element.replace('€', '').replace(',', ''))
                    break
            roomtype = link[1]
            link = 'https://www.pararius.com' + link
            if roomtype in room_types and max_rent >= price:
                info = [link, city, roomtype, price, 0]
                cursor.execute("INSERT OR IGNORE INTO room (link, city, type, price,notified) VALUES (?,?,?,?,?)", info)

    # get listings from kamernet
    for city in city_names:
        html_text = requests.get('https://kamernet.nl/en/for-rent/rooms-' + city).text
        soup = BeautifulSoup(html_text, 'lxml')
        listings = soup.find_all('div', id=lambda value: value and value.startswith('roomAdvert_'))
        for a in listings[:5]:
            link = a.find('a', class_="tile-title truncate")['href']
            roomtype = a.find('div', class_="tile-room-type").text.strip()[2:3].lower()
            price = int(a.find('div', class_="tile-rent").text.strip().split()[1][:-2])
            if roomtype in room_types and max_rent >= price:
                info = [link, city, roomtype, price, 0]
                cursor.execute("INSERT OR IGNORE INTO room (link, city, type, price,notified) VALUES (?,?,?,?,?)", info)

    roomtypes = {
        'a':'apartment',
        's':'studio',
        'h':'house',
        'r':'room'
    }

    def send_telegram_message(link,city, roomtype,price):
        bot = Bot(token=api_token)

        message = f'New {roomtypes[roomtype]} available for rent in {city} for {price}€! \nLink:\n{link}'
        bot.send_message(chat_id=chat_id, text=message)

    advertinfo = cursor.execute("SELECT * FROM room WHERE notified = 0").fetchone()
    while advertinfo is not None:
        update_query = "UPDATE room SET notified = ? WHERE link = ?"
        cursor.execute(update_query, (1, advertinfo[0]))
        # Create and run the event loop
        send_telegram_message(advertinfo[0], advertinfo[1], advertinfo[2], advertinfo[3])
        advertinfo = cursor.execute("SELECT * FROM room WHERE notified = 0").fetchone()

    # finalize the changes and exit the database
    connection.commit()
    connection.close()
    time.sleep(random.randint(refresh_interval[0] * 60, refresh_interval[1] * 60))


