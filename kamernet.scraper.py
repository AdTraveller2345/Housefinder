from bs4 import BeautifulSoup
import requests
import sqlite3

html_text = requests.get('https://kamernet.nl/en/for-rent/rooms-eindhoven').text
soup = BeautifulSoup(html_text, 'lxml')

connection = sqlite3.connect("D:/room.finder/rooms.db")
cursor = connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS room (link TEXT PRIMARY KEY, name TEXT, type TEXT, applied BOOLEAN, UNIQUE(link))")
for number in range(0,18):
    room = soup.find('div', id = 'roomAdvert_'+str(number))
    name = room.find('a', class_="tile-title truncate")
    room_name = room.find('a', class_="tile-title truncate").text.strip()
    room_link = name['href']
    room.style = room.find('div', class_="tile-room-type").text.strip()[2:]
    info = [room_name, room_link, room.style,False]
    cursor.execute("INSERT OR IGNORE INTO room (link, name, type, applied) VALUES (?,?,?,?)",info)
rows = cursor.execute("SELECT * FROM room order by name").fetchall()
for row in rows:
    print(row)

connection.commit()
connection.close()
