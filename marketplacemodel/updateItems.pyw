import mysql.connector
from mysql.connector import errorcode
from datetime import datetime
import requests
import time
import subprocess
# Class that handles initializing the usage of a database and SQL statements
class DatabaseClass:
    # Initialize database by entering host, account info, and database name to connect to
    def __init__(self, config):
        try:
            self.user = config[0]
            self.password = config[1]
            self.host = config[2]

            self.cnx = mysql.connector.connect(user=self.user, password=self.password,host=self.host,database="marketplacedb")
            self.cursor = self.cnx.cursor()
        except mysql.connector.Error as err:
            self.error(err)

    def setDatabase(self, DB_NAME):
        # Try to create a database if it does not already exists
        try:
            self.cursor.execute(
                "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
            self.cursor.execute("USE {}".format(DB_NAME))
        except mysql.connector.Error as err:
            # Try to use database if it exists, create the database, or an unknown error occurred
            try:
                self.cursor.execute("USE {}".format(DB_NAME))

            except mysql.connector.Error as err:

                if err.errno == errorcode.ER_BAD_DB_ERROR:
                    self.setDatabase(DB_NAME)

                    self.cnx.database = DB_NAME
                else:

                    exit(1)

    def updateAll(self):
        item_ids = self.getItemNames("ALL")

        for i in item_ids:
            payload = {
                "keyType": 0,
                "mainKey": i[0]
            }

            # Get response from API, parse it, then update the database with response
            response = self.getSubListResponse(payload)
            if (response == "0"):
                continue
            else:
                items = self.parseMarketplaceItem(response)

                for item in items:
                    sql = (
                            "INSERT INTO {}".format(self.TABLE) +
                            " (item_id, min_enhance, max_enhance, base_price, in_stock, "
                            "total_trades, min_price_list,max_price_list,last_sale_price,last_sale_time)"
                            "VALUES (%s, %s, %s, %s, %s,%s, %s,%s,%s,%s)"
                            "ON DUPLICATE KEY UPDATE "
                            "base_price=VALUES(base_price), in_stock=VALUES(in_stock),total_trades=VALUES(total_trades),"
                            "min_price_list=VALUES(min_price_list),last_sale_price=VALUES(last_sale_price),"
                            "last_sale_time=VALUES(last_sale_time)"
                    )

                    self.cursor.execute(sql, tuple(item))
                    self.cnx.commit()

    def getItemNames(self, item_name):
        if item_name == "ALL":
            sql = ("SELECT * FROM {}".format(self.TABLE))

        else:
            sql = ("SELECT * FROM {} WHERE item_name={}".format(self.TABLE, item_name))

        return self.fetchAll(sql)

    def fetchAll(self, sqlStatement):
        try:
            self.cursor.execute(sqlStatement)
            rows = self.cursor.fetchall()
            if rows == None:
                return ""
            else:
                return rows
        except mysql.connector.Error as err:
            self.error(err)

    def parseMarketplaceItem(self, response):
        items = [item.split("-") for item in response.split("|")]
        for item in items:
            item[-1] = datetime.fromtimestamp(int(item[-1])).strftime('%Y-%m-%d %H:%M:%S')
        return items

    def getSubListResponse(self, payload):
        URL = 'https://na-trade.naeu.playblackdesert.com/Trademarket/GetWorldMarketSubList'
        HEADERS = {
            "Content-Type": "application/json",
            "User-Agent": "BlackDesert",
            "cookie": "visid_incap_2504216=1c%2FH2VetS%2FeZihDG6z7E9QIIoWAAAAAAQUIPAAAAAAA6X8M83f1Phv%2BPRqqkMjF%2F; nlbi_2504216=w0WTY261IhfxWhLpoDFtLwAAAACqkRKdV1p2v7vzexYYoVQg; incap_ses_876_2504216=G054LgVtC39mlu5grS0oDAIIoWAAAAAAHal%2FMOTTzoq4I6krrEwXCQ%3D%3D"
        }
        response = requests.request('POST', URL, json=payload, headers=HEADERS)
        return response.text[29:].rstrip(' |"} ')

    def getPearlItems(self,subCat):
        url = 'https://na-trade.naeu.playblackdesert.com/Trademarket/GetWorldMarketList'
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "BlackDesert"
        }
        payload = {
            "keyType": 0,
            "mainCategory": 55,
            "subCategory":subCat,

        }
        response = requests.request('POST', url, json=payload, headers=headers)
        return response.text[29:].rstrip(' |"} ')

    def parsePearlitem(self,response):
        items = [item.split("-") for item in response.split("|")]
        return items

    def addPearlItems(self):
        for i in range(1,9):
            response = self.getPearlItems(i)
            if (response == "0"):
                continue
            else:
                items = self.parsePearlitem(response)

                for item in items:
                    print(item)
                    sql = (
                            "INSERT INTO {}".format(self.TABLE) +
                            " (item_id, in_stock,total_trades,base_price)"
                            "VALUES (%s, %s, %s, %s)"
                            "ON DUPLICATE KEY UPDATE "
                            "base_price=VALUES(base_price), in_stock=VALUES(in_stock),total_trades=VALUES(total_trades)"
                    )

                    self.cursor.execute(sql, tuple(item))
                    self.cnx.commit()

    def error(self, err):
        return err

    def addName(self,sql,tuple):
        self.cursor.execute(sql,tuple)
        self.cnx.commit()

    def updatePearlItems(self):
        item_ids = self.getItemNames("ALL")

        for i in item_ids:
            payload = {
                "keyType": 0,
                "mainKey": i[0]
            }
            print(i[0])
            # Get response from API, parse it, then update the database with response
            response = self.getSubListResponse(payload)
            if (response == "0"):
                continue
            else:
                items = self.parsePearlItem(response)

                for item in items:
                    sql = (
                            "INSERT INTO {}".format(self.TABLE) +
                            " (item_id, base_price, in_stock,total_trades) "
                            "VALUES (%s, %s, %s, %s)"
                            "ON DUPLICATE KEY UPDATE "
                            "base_price=VALUES(base_price), in_stock=VALUES(in_stock),total_trades=VALUES(total_trades)"
                    )

                    self.cursor.execute(sql, tuple(item))
                    self.cnx.commit()
#Connect to cooking_items table
class CookingItems(DatabaseClass):
    def __init__(self):
        super().__init__([ "root", "BDOProject","localhost"])
        self.TABLE = "cooking_items"

#Connect to alchemy items table
class AlchemyItems(DatabaseClass):
    def __init__(self):
        super().__init__(["root", "BDOProject","localhost"])
        self.TABLE = "alchemy_items"
class PearlItems(DatabaseClass):
    def __init__(self):
        super().__init__(["root", "BDOProject","localhost"])

        self.TABLE = "pearl_items"

if __name__ == "__main__":
    start = time.time()
    #Connect and update cooking items
    cooking = CookingItems()
    cooking.updateAll()

    #Connect and update alchemy items
    alchemy = AlchemyItems()
    alchemy.updateAll()
    print(time.time()-start,"seconds to update")







