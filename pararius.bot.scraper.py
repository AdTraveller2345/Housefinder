from bs4 import BeautifulSoup
import requests
import sqlite3

#set your search preferences
city_names = ('eindhoven', 'tilburg','helmond','den-bosch') #preferred cities
room_types = ('a','h','r','s') #preferred type of accommodation 'a' = apartman, 'h' = house, 'r' = room 's' = studio

#set up connection with the database
connection = sqlite3.connect("D:/parariusrooms.db") #you can specify the location
cursor = connection.cursor()

#create table and fill it with contents from pararius
cursor.execute("CREATE TABLE IF NOT EXISTS room (link TEXT PRIMARY KEY, city TEXT,type TEXT, applied BOOLEAN, UNIQUE(link))")
for city in city_names:
    html_text = requests.get('https://www.pararius.com/apartments/' + city).text
    soup = BeautifulSoup(html_text, 'lxml')
    listings = soup.find_all('a', class_="listing-search-item__link listing-search-item__link--title")
    for a in listings:
        link = 'https://www.pararius.com' + a['href']
        roomtype = a['href'][1]
        if roomtype in room_types:
            info = [link, city,roomtype, False]
            cursor.execute("INSERT OR IGNORE INTO room (link, city, type, applied) VALUES (?,?,?,?)",info)

# uncomment the following lines to see the current data in the database
# rows = cursor.execute("SELECT * FROM room ").fetchall()
# for row in rows:
#     print(row)

#finalize the changes and exit the database
connection.commit()
connection.close()
