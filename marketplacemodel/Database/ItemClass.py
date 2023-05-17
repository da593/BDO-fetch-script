from Database.DatabaseClass import DatabaseClass
class CookingItems(DatabaseClass):
    def __init__(self):
        super().__init__(["localhost", "root", "BDOProject"])
        self.setDatabase("marketplacedb")
        self.TABLE = "cooking_items"


class AlchemyItems(DatabaseClass):
    def __init__(self):
        super().__init__(["localhost", "root", "BDOProject"])
        self.setDatabase("marketplacedb")
        self.TABLE = "alchemy_items"