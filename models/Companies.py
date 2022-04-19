from sqlite3 import Connection, Cursor
from models.Company import Company
import pandas as pd 

class Companies:
    def __init__(self, conn: Connection, cursor: Cursor):
        super().__init__()
        self.__conn = conn
        self.__cursor = cursor

    def get_by_id(self, id: int):
        self.__cursor.execute("""
        SELECT CompanyID , CompanyName, FirstName, LastName,
        created_at, Patronymic, address, phoneNumber, Fax, Email, checkingAccount FROM Companies
        WHERE CompanyID = ?;
        """, [id])
        res = self.__cursor.fetchone()
        try:
            return Company(res[0], res[1], res[2], res[3],
            res[4], res[5], res[6], res[7], res[8], res[9], res[10])
        except:
            return None

    def get_all(self):
        self.__cursor.execute("SELECT * FROM Companies;")  
        rows = self.__cursor.fetchall()
        id_arr = []
        first_name_arr = []
        name_arr = []
        last_name_arr = []
        patronymic_arr = []
        created_at_arr = []
        address_arr = []
        phone_number_arr = []
        fax_arr = []
        email_arr = []
        checkingAccount_arr = []
        for row in rows:  
            id_arr.append(row[0])
            name_arr.append(row[1])
            first_name_arr.append(row[2])
            last_name_arr.append(row[3])
            created_at_arr.append(row[4])
            patronymic_arr.append(row[5])
            address_arr.append(row[6])
            phone_number_arr.append(row[7])
            fax_arr.append(row[8])
            email_arr.append(row[9])
            checkingAccount_arr.append(row[10])
            
        return pd.DataFrame(
            {"ИД": id_arr,
            "Название": name_arr,
            "Имя руководителя": first_name_arr,
            "Фамилия руководителя": last_name_arr,
            "Отчество руководитель": patronymic_arr,
            "Дата создания": created_at_arr,
            "Адрес": address_arr,
            "Номер телефона": phone_number_arr,
            "Факс": fax_arr,
            "Электронная почта": email_arr,
            "Счет в банке": checkingAccount_arr},
            index=None)

    def add(self, company: Company):
        query = """
        INSERT INTO Companies (CompanyName, FirstName, LastName, 
        Patronymic, Address, PhoneNumber, Fax, Email, checkingAccount) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
        """
        item_tuple = (company.companyName, company.firstName, company.lastName, 
            company.patronymic, company.address, company.phoneNumber, company.fax, company.email,
            company.checkingAccount)
        self.__cursor.execute(query, item_tuple)
        self.__conn.commit()
    
    def delete(self, id: int):
        try:
            query = "DELETE FROM Companies WHERE CompanyID = ?;" 
            self.__cursor.execute(query, [id])
            self.__conn.commit()
            return None
        except Exception as err:
            return err
    
    def edit(self, id: int, company: Company):
        query = """
        UPDATE Companies SET CompanyName = ?, FirstName = ?, LastName = ?, 
        Patronymic = ?, Address = ?, phoneNumber = ?, Fax = ?, Email = ?, checkingAccount = ?
        WHERE CompanyID = ?;
        """
        item_tuple = (company.companyName, company.firstName, company.lastName, 
            company.patronymic, company.address, company.phoneNumber, company.fax, company.email,
            company.checkingAccount, id)
        self.__cursor.execute(query, item_tuple)
        self.__conn.commit()