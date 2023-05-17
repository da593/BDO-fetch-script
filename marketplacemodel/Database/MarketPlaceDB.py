from Database.DatabaseClass import DatabaseClass
from RequestAPI.getResponse import getVolatileListResponse
from RequestAPI.getResponse import getSubListResponse
from RequestAPI.getResponse import findItemIDsResponse
from RequestAPI.parseResponse import *
import time

#A class to handle the marketplace db with specialize CRUD methods
class MarketPlaceDB(DatabaseClass):
    #Connect to marketplacedb
    def __init__(self):
        super().__init__(["localhost", "root", "BDOProject"])
        self.setDatabase("marketplacedb")

    def create(self,tuple_values):
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
        self.cursor.execute(sql,tuple_values)
        self.cnx.commit()

    def insertItemID(self,tuple_values):
        sql = (
                "INSERT IGNORE INTO {}".format(self.TABLE) +
                " (item_id,item_name,min_enhance,max_enhance)"
                "VALUES (%s, %s,%s,%s)"

               )

        self.cursor.execute(sql,tuple_values)
        self.cnx.commit()


    def getItemNames(self,item_name):
        if item_name == "ALL":
            sql = ("SELECT * FROM {}".format(self.TABLE))

        else:
            sql = ("SELECT * FROM {} WHERE item_name={}".format(self.TABLE,item_name))

        return self.fetchAll(sql)




    def updateVolatileItems(self):
        response = getVolatileListResponse()
        items = parseVolatileItems(response)
        start_time = time.time()
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


        self.displayLastUpdate()

    def updateSpecificID(self,file):
        Lines = file.readlines()
        for line in Lines:
            payload = {
                "keyType": 0,
                "mainKey": line
            }
            response = getSubListResponse(payload)
            if (response == "0"):
                continue
            else:
                items = parseMarketplaceItem(response)
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
    def displayLastUpdate(self):

        t = datetime.now()
        timestr = t.strftime("%H:%M:%S")
        print("Items updated on {}".format(timestr))



    def createTable(self,headers):
        for table_name in headers:
            table_description = headers[table_name]
            try:
                print("Creating table {}: ".format(table_name), end='')
                self.cursor.execute(table_description)
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print("already exists.")
                else:
                    print(err.msg)
            else:
                print("OK")