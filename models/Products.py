import pandas as pd
from sqlite3 import Connection, Cursor
from models.Product import Product


class Products:
    def __init__(self, conn: Connection, cursor: Cursor):
        super().__init__()
        self.__conn = conn
        self.__cursor = cursor
    
    def get_by_id(self, id: int):
        self.__cursor.execute("""
        SELECT ProductID, Name, Pic, Measure, CostPerUnit, Description, Availability
        FROM products
        WHERE ProductID = ?;
        """, [id])  
        res = self.__cursor.fetchone()
        try:
            return Product(res[0], res[1], res[2], res[3], res[4], res[5], res[6])
        except:
            return None

    def get_all(self):
        self.__cursor.execute("SELECT * FROM Products;")  
        rows = self.__cursor.fetchall()
        id_arr = []
        names_arr = []
        pics_arr = []
        measures_arr = []
        CostPerUnits_arr = []
        descriptions_arr = []
        availability_arr = []
        for row in rows:
            id_arr.append(row[0])
            names_arr.append(row[1])
            pics_arr.append(row[2])
            measures_arr.append(row[3])
            CostPerUnits_arr.append(row[4])
            descriptions_arr.append(row[5])
            availability_arr.append(row[6])
            
        return pd.DataFrame(
            {"ИД": id_arr,
            "Название": names_arr,
            "Фото": pics_arr,
            "Единица измерения": measures_arr,
            "Цена за единицу": CostPerUnits_arr,
            "Описание": descriptions_arr,
            "Наличие": availability_arr},
            index=None)

    def add(self, product: Product):
        query = """
        INSERT INTO products (Name, Pic, Measure, CostPerUnit, Description, Availability) 
        VALUES (?, ?, ?, ?, ?, ?);
        """
        item_tuple = (product.name, product.pic, product.measure, product.cost_per_unit,
            product.description, product.availability)
        self.__cursor.execute(query, item_tuple)
        self.__conn.commit()
    
    def delete(self, id: int):
        try:
            query = """DELETE from Products where ProductID = ?;"""
            self.__cursor.execute(query, [id])
            self.__conn.commit()
            return None
        except Exception as err:
            return err
    
    def edit(self, id: int, product: Product):
        query = """
        UPDATE Products SET Name = ?, Pic = ?, Measure = ?, 
        CostPerUnit = ?, Description = ?, Availability = ?
        WHERE ProductID = ?;
        """
        item_tuple = (product.name, product.pic, product.measure, product.cost_per_unit,
            product.description, product.availability, id)
        self.__cursor.execute(query, item_tuple)
        self.__conn.commit()