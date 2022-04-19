from sqlite3 import Connection, Cursor

class Product:
    def __init__(self, id, name, pic, measure, 
        cost_per_unit, description, availability):
        self.id = id
        self.name = name
        self.pic = pic
        self.measure = measure
        self.cost_per_unit = cost_per_unit
        self.description = description
        self.availability = availability

    def get_string(self):
        return f'''
        ИД: {self.id}
        Название: {self.name}
        Фото: {self.pic}
        Единица измерения: {self.measure}
        Цена за единицу: {self.cost_per_unit}
        Описание: {self.description}
        Наличие товара: {self.availability}
        '''

    def SetAvailability(self, conn: Connection, cursor: Cursor, availability):
        try:
            query = """
            UPDATE Products SET Availability = 1
            WHERE id = ?;
            """
            item_tuple = (availability, self.id)
            cursor.execute(query, item_tuple)
            conn.commit()
        except Exception as err:
            return err
    def SetNotAvailability(self, conn: Connection, cursor: Cursor, availability):
        try:
            query = """
            UPDATE Products SET Availability = 0
            WHERE id = ?;
            """
            item_tuple = (availability, self.id)
            cursor.execute(query, item_tuple)
            conn.commit()
        except Exception as err:
            return err
