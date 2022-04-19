import pandas as pd
from sqlite3 import Connection, Cursor
from models.Sail import Sail
from models.Company import Company



class Sails:
    def __init__(self, conn: Connection, cursor: Cursor):
        super().__init__()
        self.__conn = conn
        self.__cursor = cursor

    def get_by_id(self, id: int):
        self.__cursor.execute("""
        SELECT SailID, CompanyID, ProductSailDate, PaymentTerm, Discount FROM Sails
        WHERE SailID = ?;
        """, [id])  
        res = self.__cursor.fetchone()
        try:
            return Sail(res[0], res[1], res[2], res[3], res[4])
        except:
            return None
    def get_by_CompanyId(self, id : int):
            self.__cursor.execute("""
            SELECT SailID, CompanyID, ProductSailDate, PaymentTerm, Discount FROM Sails
            WHERE CompanyID = ?;
            """, [id])
            res = self.__cursor.fetchall()
            if res:
                sailID_arr=[]
                productsaildate_arr=[]
                paymentterm_arr=[]
                discount=[]
                products_arr = []
                costs_arr = []
                for re in res:
                    sail = self.get_by_id(re[0])
                    sailID_arr.append(re[0])
                    productsaildate_arr.append(re[2])
                    paymentterm_arr.append(re[3])
                    discount.append(re[4])
                    products_arr.append(sail.get_products_str(self.__cursor))
                    costs_arr.append(sail.get_cost(self.__cursor))
                return pd.DataFrame(
                    {"ИД продажи": sailID_arr,
                    "Дата продажи": productsaildate_arr,
                    "Условия оплаты": paymentterm_arr,
                    "Cкидка": discount,
                    "Товары": products_arr,
                    "Цена": costs_arr},
                    index=None)
            else:
                return ("У компании с заданным ID нет продаж!")
   
    def get_all(self):
        self.__cursor.execute("SELECT SailID FROM Sails;")  
        rows = self.__cursor.fetchall()
        id_arr = []
        products_arr = []
        companies_arr = []
        productSailDate_arr = []
        paymentTerm_arr = []
        discount_arr = []
        costs_arr = []
        for row in rows:
            sail = self.get_by_id(row[0])
            id_arr.append(sail.id)
            products_arr.append(sail.get_products_str(self.__cursor))
            companies_arr.append(sail.get_company_str(self.__cursor))
            productSailDate_arr.append(sail.get_productSailDate(self.__cursor))
            paymentTerm_arr.append(sail.paymentTerm)
            discount_arr.append(sail.discount)
            costs_arr.append(sail.get_cost(self.__cursor))
            
        return pd.DataFrame(
            {"ИД": id_arr,
            "Товары": products_arr,
            "Компания": companies_arr,
            "Дата продажи": productSailDate_arr,
            "Условия оплаты": paymentTerm_arr,
            "Скидка": discount_arr,
            "Стоимость": costs_arr},
            index=None)

    def get_next_id(self):
        self.__cursor.execute("""
        SELECT seq from sqlite_sequence WHERE name = 'Sails';
        """)  
        res = self.__cursor.fetchone()
        return int(res[0]) + 1

    def add(self, sail: Sail):
        query = """
        INSERT INTO Sails (CompanyID, PaymentTerm, Discount) 
        VALUES (?, ?, ?);
        """
        item_tuple = (sail.companyID, sail.paymentTerm, sail.discount)
        self.__cursor.execute(query, item_tuple)
        self.__conn.commit()
    
    def delete(self, id: int):
        try:
            query = """DELETE from Sails where SailID = ?;""" 
            self.__cursor.execute(query, [id])
            self.__conn.commit()
            return None
        except Exception as err:
            return err
    
    def edit(self, id: int, sail : Sail):
        query = """
        UPDATE Sails SET CompanyID = ?, PaymentTerm = ?, Discount = ?
        WHERE SailID = ?;
        """
        item_tuple = (sail.companyID, sail.paymentTerm, sail.discount, id)
        self.__cursor.execute(query, item_tuple)
        self.__conn.commit()