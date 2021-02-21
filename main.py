import discord
from bs4 import BeautifulSoup
import requests

client = discord.Client()
import mysql.connector

mydb = mysql.connector.connect(
    host="MYSQL-HOST",
    database="DATABASE",
    user="USER",
    password="PASSWORD"
)
results = 5


@client.event
async def on_ready():
    """
      print botname
    """
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    """
    :param message:
    """
    msg = message.content

    #if the message is hi
    if msg.startswith("hi"):
        await message.channel.send("Hey.")

    #if the message is to get recent searches
    if msg.startswith("!recent"):
        search = msg.split("!recent ", 1)[1]
        mycursor = mydb.cursor()

        mycursor.execute("""SELECT keyword FROM Searches WHERE keyword LIKE '%{search}%'""".format(search=search))
        myresult = mycursor.fetchall()
        await message.channel.send('Your recent searches are {result}'.format(result=myresult))

    #if the message is to get google top 5 links
    if msg.startswith("!google"):
        search = msg.split("!google ", 1)[1]
        mycursor = mydb.cursor()

        sql = """REPLACE INTO Searches (keyword) VALUES ('{search}')""".format(search=search)
        print(sql)
        mycursor.execute(sql)
        mydb.commit()
        page = requests.get(f"https://www.google.com/search?q={search}&num={results}")
        soup = BeautifulSoup(page.content, "html5lib")
        links = soup.findAll("a")
        link_list = []
        for link in links:
            if len(link_list) >= results:
                break
            link_href = link.get('href')
            if "url?q=" in link_href and not "webcache" in link_href:
                link = link.get('href').split("?q=")[1].split("&sa=U")[0]
                link_list.append(link)
        await message.channel.send('Your Search results are {links}'.format(links=str(link_list)))


client.run("KEY")
