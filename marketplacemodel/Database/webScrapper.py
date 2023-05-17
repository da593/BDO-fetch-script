#This file scrapes bdodatabase for item names if it is null by comparing the item id
#Run this script if the game is updated and new items are added to update database

from Database.MarketPlaceDB import MarketPlaceDB
import requests
from bs4 import BeautifulSoup
import time


#Make request seem like a browser
headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }

#Get all item ids in the database and find the item name for it
#sql = ("SELECT item_id FROM marketplace_items WHERE item_name = '' ")
#item_ids = db.fetchAll(sql)
db = MarketPlaceDB()
#Loop through all ids and parse the html for item name
#having a 1 second pause between each iteration to prevent heavy request load



i = 10003
url = "https://bdocodex.com/us/item/"+str(i)+"/"
response = requests.get(url,headers)
html_ref = str(BeautifulSoup(response.text,"html.parser").find("title")).split("|")
print(response.text)

headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }
sql = ("SELECT item_id FROM pearl_items WHERE item_name is Null ")
item_ids = pearl.fetchAll(sql)

for i in item_ids:
    url = "https://bdocodex.com/us/item/" + str(i[0]) + "/"
    response = requests.get(url, headers)
    html_ref = str(BeautifulSoup(response.text, "html.parser").find("title")).split(" -")
    name = html_ref[0][7::]
    print(i[0],name)
    s = (
        "UPDATE pearl_items SET item_name = %s WHERE item_id= %s"
    )
    pearl.addName(s,(name,i[0]))