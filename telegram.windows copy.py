from bs4 import BeautifulSoup
import requests
import asyncio
from telegram import Bot
import sqlite3
import time
import subprocess
import random
#1.In telegram search for the bot called Botfather
#2.Start a conversation with it and create a new bot
#3.Name your bot whatever you want
#4.Copy the API token you get for your bot. Paste into line 16
#5.Message userinfobot and paste your ID into line 17
#6.Set your search preferences and run the code

api_token = '7857522620:AAEuvfIEXoEy0RyfR445iUfKD1eCPGVeznA'  # API token for your bot
chat_id = '7724845710'  # Your Telegram chat ID
# set your search preferences
city_names = ('eindhoven','tilburg','helmond','den-bosch')  # preferred cities
room_types = ('a','h','r','s')  # preferred type of accommodation 'a' = apartment, 'h' = house, 'r' = room 's' = studio
refresh_interval = [1,2]  # set a random interval for how often should the program rerun itself
max_rent = 15000

roomtypes = {
    'a':'apartment',
    's':'studio',
    'h':'house',
    'r':'room'
}
def main():
    # set up connection with the database
    connection = sqlite3.connect("listings2.db")  # you can specify the location and name of the database
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
            #print(f"pararius {roomtype}")
            link = 'https://www.pararius.com' + link
            if roomtype in room_types and max_rent >= price:
                info = [link, city, roomtype, price, False]
                cursor.execute("INSERT OR IGNORE INTO room (link, city, type, price,notified) VALUES (?,?,?,?,?)", info)
    print("kuki")
    # get listings from kamernet
    for city in city_names:
        url = f'https://kamernet.nl/en/for-rent/rooms-{city}'
        html_text = requests.get(url).text
        soup = BeautifulSoup(html_text, 'lxml')

        # Updated <a> tag class to match new structure
        listings = soup.find_all('a', class_="MuiTypography-root MuiTypography-inherit MuiLink-root MuiLink-underlineNone MuiPaper-root MuiPaper-elevation MuiPaper-rounded MuiPaper-elevation0 MuiCard-root ListingCard_root__e9Z81 mui-style-i2963i")
        print(f"{city}: Found {len(listings)} listings")

        for listing in listings[:5]:  # Limit to first 5
            try:
                # Extract link
                link = listing['href']

                # Extract price
                price_tag = listing.find('span', class_="MuiTypography-root MuiTypography-h5 mui-style-1pios4g")
                price_text = price_tag.text.strip().replace('€', '').replace(',', '')
                price = int(''.join(filter(str.isdigit, price_text)))

                # Extract accommodation type
                type_tag = listing.find('p', class_="MuiTypography-root MuiTypography-body2 MuiTypography-noWrap mui-style-1i83cky")
                roomtype_raw = type_tag.text.strip().lower()
                #print(f"kamernet {roomtype_raw}")
                roomtype_code = roomtype_raw[0]  # Assuming first letter maps to 'r', 's', etc.

                if roomtype_code in room_types and price <= max_rent:
                    info = ['https://kamernet.nl/'+link, city, roomtype_code, price, False]
                    cursor.execute("INSERT OR IGNORE INTO room (link, city, type, price, notified) VALUES (?,?,?,?,?)", info)

            except Exception as e:
                print(f"Error parsing listing in {city}: {e}")

    url = "https://www.myhousing.nl/"
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'lxml')
    with open(f"{city}_listing_page.html.txt", "w", encoding="utf-8") as file:
        file.write(html_text)

    print(f"HTML saved to {city}_listing_page.html.txt")
    # Updated <a> tag class to match new structure
    listings = soup.find_all('a', class_="swiper-wrapper pg-carousel-container")
    print(f"Found {len(listings)} listings on myhousing")

    async def send_telegram_message(link,city, roomtype,price):
        bot = Bot(token=api_token)

        message = f'New {roomtypes[roomtype]} available for rent in {city} for {price}€! \nLink:\n{link}'
        await bot.send_message(chat_id=chat_id, text=message)

    advertinfo = cursor.execute("SELECT * FROM room WHERE notified == False").fetchone()
    while advertinfo is not None:
        update_query = "UPDATE room SET notified = ? WHERE link = ?"
        cursor.execute(update_query, (True, advertinfo[0]))
        # Create and run the event loop
        loop = asyncio.get_event_loop()
        loop.run_until_complete(send_telegram_message(advertinfo[0], advertinfo[1], advertinfo[2], advertinfo[3]))
        advertinfo = cursor.execute("SELECT * FROM room WHERE notified == False").fetchone()

    # finalize the changes and exit the database
    connection.commit()
    connection.close()


if __name__ == "__main__":
    while True:
        main()
        print('program is running')
        time.sleep(random.randint(refresh_interval[0]*60, refresh_interval[1]*60))
        # Restart the program
        subprocess.call(["python", __file__])
