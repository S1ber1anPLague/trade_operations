class Company:
    def __init__(self, id, companyName, firstName, lastName, createdAt, patronymic,address,phoneNumber,
    fax, email, checkingAccount ):
        self.id = id
        self.companyName = companyName
        self.firstName = firstName
        self.lastName = lastName
        self.createdAt = createdAt
        self.patronymic = patronymic
        self.address = address
        self.phoneNumber = phoneNumber
        self.fax = fax
        self.email = email
        self.checkingAccount = checkingAccount

    def get_string(self):
        return f'''
        id: {self.id}
        Название фирмы-клиента: {self.companyName}
        Имя руководителя: {self.firstName}
        Фамилия руководителя: {self.lastName}
        Дата создания: {self.createdAt}
        Отчество руководителя: {self.patronymic}
        Юридический адрес фирмы: {self.address}
        Контактный телефон фирмы клиента: {self.phoneNumber}
        Факс фирмы клиента: {self.fax}
        Адрес электронной почты клиента: {self.email}
        Наличие расчетного счета в банке: {self.checkingAccount}
        '''