# Housefinder
PURPOSE:
It can be really challanging to find housing in the Netherlands. The number of available offers is usually low, therefore many students apply for the same room. This result in the landlord considering only the first couple applicants. Thus being fast plays a crucial role in your journey.
This program aims to help you with that. Kamernet sends you emails about new listings but these are usually a couple minutes late, for pararius its even worse. This program scrapes these websites every 1-2 minutes and if a new item shows up it sends you an instant message via telegram. (see the attached photo to get an idea of what these messages look like)

HOW TO USE:  
  Running it on your local computer:
  This is the easier way, but this result in the app only working when you are running it on your computer.
  1. You need to download telegram.windows.py
  2. You need to set up a new bot in telegram
    2.1 message @botfather in telegram and create a new bot (just follow the instructions given by the bot)
    2.2 copy the api you recieved into the corresponding variable in your code
    2.3 meessage @userinfobot and place your user id into the corresponding variable in your code
  3. Set your search preferences in the code
    3.1 IMPORTANT: the city name must be written in the way they are found the site's link for example https://kamernet.nl/en/for-rent/rooms-den-bosch => den-bosch
  4. Dowload the necessary libraries for python using pip (beautifulsoup and telegram)
  6. Run your program

  Running it on a virtual machine:
  This is a more complicated method but once you set it up you dont have to mess with it again (this is how I used the program)
  1. create an account on oracle - they offer a free tier subscription which has enough resources to run your program
  2. Create a new linux instance and connect to it via an ssh sever using your private key that you received when creating the virtual machine
  3. download telegram.linnux.py and
  4. You need to set up a new bot in telegram
    4.1 message @botfather in telegram and create a new bot (just follow the instructions given by the bot)
    4.2 copy the api you recieved into the corresponding variable in your code
    4.3 meessage @userinfobot and place your user id into the corresponding variable in your code
  5. Set your search preferences in the code
     5.1 IMPORTANT: the city name must be written in the way they are found the site's link for example https://kamernet.nl/en/for-rent/rooms-den-bosch => den-bosch
  6. Upload telegram.linux.py to your virtual machine - again use chatgpt if you are stuck
  7. Run your program on the cloud using this line: nohup python3 telegram.linux.py & - this ensures to keep your program running after disconnecting from the VM
  8. You can easily add more people to your bot:
    8.1 Have them message your bot via telegram
    8.2 save their userid in the program
    8.3 create another instance of the line bot.send_message(chat_id=chat_id, text=message)
    8.4 set the chat_id for the other persons user id
    8.5 upload the modified code to the vm and run it
