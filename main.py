import sqlite3
from models.Companies import Companies
from models.Company import Company
from models.Products import Products
from models.Product import Product
from models.Sails import Sails
from models.Sail import Sail

main_commands = {
    "q": -1,
    "help": 0,
    "companies" : 1,
    "products" : 2,
    "sails" : 3,
}

def help():
    print(
"""
- Чтобы перейти в управление компаниями введите "companies"
- Чтобы перейти в управление товарами введите "products"
- Чтобы перейти в управление продажами введите "sails"
- Чтобы посмотреть инструкцию, введите "help"
- Чтобы выйти, введите "q"
""")

cur = None
conn = None
companies = Companies(None, None)
sails = Sails(None, None)
products = Products(None, None)

def init_connection():
    global conn, cur
    conn = sqlite3.connect("Database/Sailsoperations.db")
    cur = conn.cursor()

    global companies, sails, products
    companies = Companies(conn, cur)
    sails = Sails(conn, cur)
    products = Products(conn, cur)


def main_menu():
    init_connection()
    help()
    command = input("Введите команду: ")
    if command in main_commands:
        i = main_commands[command]
        if i == -1:
            exit()
        elif i == 0:
            help()
            main_menu()
        elif i == 1:
            companies_menu()
        elif i == 2:
            products_menu()
        elif i == 3:
            sails_menu()
    else:
        print('''\nНекорректный ввод... 
        Прочитайте инструкцию по использованию данной программы:''')
        
        main_menu()

def companies_menu():
    try:
        global clients
        answer = int(input("Для того чтобы просмотреть список всех компаний, введите 1. Чтобы добавить компанию, введите 2. Чтобы удалить компанию, введите 3. Чтобы редактировать компанию, введите 4. (Чтобы вернуться назад нажмите 0)\n"))
        if answer == -1:
            exit()
        if answer == 0:
            main_menu()
        if answer == 1:
            get_companies()
        if answer == 2:
            add_company()
        if answer == 3:
            del_company()
        if answer == 4:
            edit_company()
    except:
        print('Что-то пошло не так!')
        main_menu()

def get_companies():
    global companies
    print()
    print(companies.get_all())
    companies_menu()

def get_company():
    global companies
    try:
        id = int(input('Введите ID компании: '))
        company = companies.get_by_id(id)
        if company:
            print(company.get_string())
            companies_menu()
        else:
            print('\nНет компании с заданным ИД.')
            companies_menu()
    except:
        print('\nЧто-то пошло не так!')
        companies_menu()

def add_company():
    companyName = input('Введите название компании: ')
    firstName = input('Введите имя руководителя: ')
    lastName = input('Введите фамилию руководителя: ')
    patronymic = input('Введите отчество руководителя: ')
    address = input('Введите адрес компании: ')
    phone = input('Введите номер телефона компании: ')
    fax = input('Введите факс компании: ')
    email = input('Введите эл.почту компании: ')
    checkingAccount = input('Введите наличие расчетного счета в банке: ')
    global companies
    company = Company(0, companyName, firstName, lastName, None, patronymic, 
        address, phone, fax, email, checkingAccount)
    companies.add(company)
    print('Компания успешно создана.') 
    companies_menu()

def del_company():
    try:
        global companies
        id = int(input('Введите ID компании: '))
        company = companies.get_by_id(id)
        if not company:
            print('Нет компании с таким ИД.') 
            companies_menu()
        ans = input(f'Вы точно хотите удалить компанию №{id}? (y/n)\n')
        if ans == 'y':
            err = companies.delete(id)
            if err is None:
                print('Компания успешно удалена!')
                companies_menu()
            else:
                print('Произошла ошибка при удалении компании: ' + str(err))
                companies_menu()
        else:
            companies_menu()
    except:
        print('Что-то пошло не так!')
        companies_menu()

def edit_company():
    try:
        global companies
        id = int(input('Введите ID компании: '))
        company = companies.get_by_id(id)
        if not company:
            print('Нет компании с таким ИД.') 
            companies_menu()
        companyName = input('Введите название компании: ')
        firstName = input('Введите имя руководителя: ')
        lastName = input('Введите фамилию руководителя: ')
        patronymic = input('Введите отчество руководителя: ')
        address = input('Введите адрес компании: ')
        phone = input('Введите номер телефона компании: ')
        fax = input('Введите факс компании: ')
        email = input('Введите эл.почту компании: ')
        checkingAccount = input('Введите наличие расчетного счета в банке: ')
        company = Company(0, companyName, firstName, lastName, None, patronymic, 
            address, phone, fax, email, checkingAccount)
        companies.edit(id, company)
        print('Компания успешно изменена.') 
        companies_menu()
    except:
        print('Что-то пошло не так!')
        companies_menu()

def products_menu():
    try:
        global clients
        answer = int(input("Для того чтобы просмотреть список всех товаров, введите 1. Чтобы добавить товар, введите 2. Чтобы удалить товар, введите 3. Чтобы редактировать товар, введите 4. (Чтобы вернуться назад нажмите 0)\n"))
        if answer == -1:
            exit()
        if answer == 0:
            main_menu()
        if answer == 1:
            get_products()
        if answer == 2:
            add_product()
        if answer == 3:
            del_product()
        if answer == 4:
            edit_product()
    except:
        print('Что-то пошло не так!')
        main_menu()

def get_products():
    global products
    print()
    print(products.get_all())
    products_menu()

def get_product():
    global products
    try:
        id = int(input('Введите ID товара: '))
        product = products.get_by_id(id)
        if product:
            print(product.get_string())
            products_menu()
        else:
            print('\nНет товара с заданным ИД.')
            products_menu()
    except:
        print('\nЧто-то пошло не так!')
        products_menu()

def add_product():
    try:
        name = input('Введите название товара: ')
        pic = input('Введите ссылку на фото: ')
        measure = input('Введите единицу изерения: ')
        cost_per_unit = float(input('Введите цену за единицу: '))
        description = input('Введите описание: ')
        availability = int(input('Введите наличие товара: '))
    except:
        print('\nВы ввели данные неправильного формата')
        products_menu()
    global products
    product = Product(0, name, pic, measure, cost_per_unit, description, availability)
    products.add(product)
    print('Товар успешно создан.') 
    products_menu()

def del_product():
    try:
        global products
        id = int(input('Введите ID товара: '))
        product = products.get_by_id(id)
        if not product:
            print('Нет товара с таким ИД.') 
            products_menu()
        ans = input(f'Вы точно хотите удалить компанию №{id}? (y/n)\n')
        if ans == 'y':
            err = products.delete(id)
            if err is None:
                print('Товар успешно удален.')
                products_menu()
            else:
                print('Произошла ошибка при удалении товара: ' + str(err))
                products_menu()
        else:
            products_menu()
    except:
        print('Что-то пошло не так!')
        products_menu()


def edit_product():
    try:
        global products
        id = int(input('Введите ID товара: '))
        product = products.get_by_id(id)
        if not product:
            print('Нет товара с таким ИД.') 
            products_menu()
        name = input('Введите название товара: ')
        pic = input('Введите ссылку на фото: ')
        measure = input('Введите единицу изерения: ')
        cost_per_unit = float(input('Введите цену за единицу: '))
        description = input('Введите описание: ')
        availability = int(input('Введите наличие товара: '))
        product = Product(0, name, pic, measure, cost_per_unit, description, availability)
        products.edit(id, product)
        print('Товар успешно изменен.') 
        products_menu()
    except:
        print('\nЧто-то пошло не так!')
        products_menu()

def change_availability():
    global products, conn, cur
    try:
        id = int(input('Введите ID товара: '))
        product = products.get_by_id(id)
        if not product:
            print('Нет товара с таким ИД.') 
            products_menu()
        availability = int(input('Введите наличие товара: '))
        err = product.SetAvailability(conn, cur, availability)
        if err is None:
            print('Наличие успешно изменено.') 
            products_menu()
        else:
            print('Произошла ошибка при изменении информации о товаре!')
            products_menu()
    except ValueError:
        print('Вы ввели данные неправильного формата')
        products_menu()


def sails_menu():
    # try:
        global clients
        answer = int(input("Для того чтобы просмотреть список всех продаж, введите 1. Чтобы добавить продажу, введите 2. Чтобы удалить продажу, введите 3. Чтобы редактировать продажу, введите 4. Чтобы просмотреть продажи конкретной компании, введите 5. (Чтобы вернуться назад нажмите 0)\n"))
        if answer == -1:
            exit()
        if answer == 0:
            main_menu()
        if answer == 1:
            get_sails()
        if answer == 2:
            add_sail()
        if answer == 3:
            del_sail()
        if answer == 4:
            edit_sail()
        if answer == 5:
            get_company_sail()
    # except:
    #     print('Что-то пошло не так!')
    #     sails_menu()
def get_company_sails():
    global sails
    print(sails.get_all_company_sails())
    sails_menu()
def get_sails():
    global sails
    print()
    print(sails.get_all())
    sails_menu()

def get_sail():
    global sails
    try:
        id = int(input('Введите ID продажи: '))
        operation = sails.get_by_id(id)
        if operation:
            print(operation.get_string(cur))
            sails_menu()
        else:
            print('\nНет продажи с заданным ИД.')
            sails_menu()
    except:
        print('\nЧто-то пошло не так!')
        sails_menu()
def get_company_sail():
    global sails
    id = int(input('Введите ID компании: '))
    operation = sails.get_by_CompanyId(id)
    print(operation)
    sails_menu()


def add_sail():
    try:
        global companies, products
        print(companies.get_all())
        company_id = int(input('Введите ИД компании: '))
        paymentTerm = input('Введите условия оплаты: ')
        products_dict = {}
        print(products.get_all())
        products_dict = add_product_toSail(products_dict)
        discount = float(input('Введите скидку: '))
    except:
        print('\nВы ввели данные неправильного формата')
        sails_menu()       
    global sails, conn, cur
    sail = Sail(sails.get_next_id(), company_id, None, paymentTerm, discount)
    sails.add(sail)
    for key in products_dict:
        err = sail.add_product(conn, cur, key, products_dict[key])
        if err is not None:
            break
    if err is None:
        print('Продажа успешно совершена.')
        sails_menu()
    else:
        print('Произошла ошибка при совершении продажи: ' + str(err))
        sails_menu()

def add_product_toSail(products_dict):
    while(True):
        try:
            pr_id = int(input('Введите ID товара: '))
            q = int(input('Введите количество единиц товара с ИД=' + str(pr_id) + ': '))
            products_dict[pr_id] = q
            print("Товар добавлен")
            answ = input("Хотите добавить еще один товар? (y/n): ")
            if(answ !="y"):
                break
        except:
            print("Некорректный ввод")
    return products_dict

def del_sail():
    try:
        global sails
        id = int(input('Введите ID продажи: '))
        sail = sails.get_by_id(id)
        if not sail:
            print('Нет продажи с таким ИД.')
            sails_menu()
        ans = input(f'Вы точно хотите удалить продажу №{id}? (y/n)\n')
        if ans == 'y':
            err = sails.delete(id)
            if err is None:
                print('Продажа успешно удалена.')
                sails_menu()
            else:
                print('Произошла ошибка при удалении продажи: ' + str(err))
                sails_menu()
        else:
            sails_menu()
    except:
        print('\nЧто-то пошло не так!')
        sails_menu()

def edit_sail():
    try:
        global sails, conn, cur
        id = int(input('Введите ИД продажи: '))
        sail = sails.get_by_id(id)
        if not sail:
            print('Нет продажи с таким ИД.') 
            sails_menu()
        global companies, products
        print(companies.get_all())
        company_id = int(input('Введите ИД компании: '))
        paymentTerm = input('Введите условия оплаты: ')
        discount = input('Введите скидку: ')
        sail = Sail(id, company_id, None, paymentTerm, discount)
        sails.edit(id, sail)
        print('Продажа успешно изменена.') 
        sails_menu()
    except:
        print('\nЧто-то пошло не так!')
        sails_menu()

main_menu()