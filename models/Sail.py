from sqlite3 import Connection, Cursor
from models.Company import Company


class Sail:
    def __init__(self, id ,companyID, productSailDate, paymentTerm,
    discount):
        self.id = id
        self.companyID = companyID
        self.productSailDate = productSailDate
        self.paymentTerm = paymentTerm
        self.discount = discount

    def get_products(self, cursor: Cursor):
        cursor.execute("""
        SELECT p.name, pis.SailQuantity
        FROM Products as p JOIN ProductsInSails as pis ON p.ProductID = pis.ProductID
        WHERE pis.SailID = ?;
        """, [self.id])  
        rows = cursor.fetchall()
        products = dict()
        for row in rows:
            products[row[0]] = row[1]
        return products

    def get_company(self, cursor: Cursor):
        cursor.execute("""
        SELECT CompanyID, CompanyName, FirstName, LastName,
        Patronymic, created_at, Address, phoneNumber, Fax, Email, checkingAccount FROM Companies
        WHERE CompanyID = ?;
        """, [self.companyID])
        res = cursor.fetchone()
        return Company(res[0], res[1], res[2], res[3],
            res[4], res[5], res[6], res[7], res[8], res[9], res[10])

    def get_cost(self, cursor: Cursor):
        cursor.execute("""
        SELECT SUM(p.CostPerUnit * pis.SailQuantity) - s.Discount as cost
		FROM Sails AS s
		JOIN ProductsInSails AS pis ON pis.SailID = s.SailID
        JOIN Products AS p ON pis.ProductID = p.ProductID
        WHERE pis.SailID = ?
        GROUP BY pis.SailID;""", [self.id])
        return cursor.fetchone()

    def get_productSailDate(self, cursor : Cursor):
        cursor.execute("""
        SELECT ProductSailDate FROM Sails WHERE SailID = ?
        """, [self.id])
        return cursor.fetchone()
        
    def get_products_str(self, cursor: Cursor):
        return str(self.get_products(cursor))

    def get_company_str(self, cursor: Cursor):
        company = self.get_company(cursor)
        return f"{company.companyName} (ИД:{company.id})"

    def get_string(self, cursor: Cursor):
        products = self.get_products_str(cursor)
        company = self.get_company_str(cursor)
        cost = self.get_cost(cursor)
        return f'''
        ИД: {self.id}
        Товары: {products}
        Компания: {company}
        Cкидка: {self.discount}
        Дата: {self.productSailDate}
        Стоимость: {str(cost)}
        '''

    def get_quantity(self, conn: Connection, cursor: Cursor, pr_id: int):
        cursor.execute("""
        SELECT SailQuantity FROM ProductsInSails
        WHERE SailID = ? AND ProductID = ?;""", (self.id, pr_id))
        return cursor.fetchone()

    def add_product(self, conn: Connection, cursor: Cursor, pr_id: int, quantity: int):
        query = """
        INSERT INTO ProductsInSails (SailID, ProductID, SailQuantity) 
        VALUES (?, ?, ?);
        """
        cursor.execute(query, (self.id, pr_id, quantity))
        conn.commit()