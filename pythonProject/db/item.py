# items = [
#     {
#         "id": "08b1a75d945b436eb2926e38a9fa84f8",
#         "item": {
#             "name": "Oreo Shake",
#             "price": 60
#         },
#     },
#     {
#         "id": "5496b5058dc847588d1b7bbc6d8b5432",
#         "item": {
#             "name": "Coffee",
#             "price": 70
#         }
#     }
# ]


import pyodbc


class ItemDatabase:
    def __init__(self):
        self.conn = pyodbc.connect('Driver={SQL Server};Server=Isha;Database=cafe;')
        self.cursor = self.conn.cursor()

    def get_items(self):
        result = []
        query = "SELECT * FROM item"
        self.cursor.execute(query)
        for row in self.cursor.fetchall():
            item_dict = {}
            item_dict["id"] = row[0]
            item_dict["name"] = row[1]
            item_dict["price"] = row[2]
            result.append(item_dict)
        return result


    def get_item(self,id):
        query = f"SELECT * FROM item WHERE id = '{id}'"
        self.cursor.execute(query)
        for row in self.cursor.fetchall():
            item_dict = {}
            item_dict["id"] = row[0]
            item_dict["name"] = row[1]
            item_dict["price"] = row[2]
            return [item_dict]


    def add_item(self,id,body):
        query = f"INSERT INTO item(id,name,price) VALUES ('{id}','{body['name']}','{body['price']}')"
        self.cursor.execute(query)
        self.conn.commit()

    def update_item(self, id, body):
        query = f"UPDATE item SET name = '{body['name']}', price = '{body['price']}' WHERE id = '{id}'"
        self.cursor.execute(query)
        if self.cursor.rowcount == 0:
            return False
        else:
            self.conn.commit()
            return True

    def delete_item(self,id):
        query = f"delete from item where id = '{id}'"
        self.cursor.execute(query)
        if self.cursor.rowcount == 0:
            return False
        else:
            self.conn.commit()
            return True


# db = ItemDatabase()
# print(db.get_item('08b1a75d945b436eb2926e38a9fa84f8'))
