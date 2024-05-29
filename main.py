import os
from dotenv import load_dotenv
import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publishers, Books, Shops, Stocks, Sales

load_dotenv()
driver = os.getenv('DRIVER')
login = os.getenv('LOGIN')
password = os.getenv('PASSWORD')
host = os.getenv('HOST')
port = os.getenv('PORT')
db_name = os.getenv('DB_NAME')
DSN = f"{driver}://{login}:{password}@{host}:{port}/{db_name}"
engine = sq.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

publisher1 = Publishers(name='USwomen')
publisher2 = Publishers(name='The Text')
publisher3 = Publishers(name='The ABC')
book1 = Books(title='Cujo', id_publisher=1)
book2 = Books(title='Misery', id_publisher=2)
book3 = Books(title='Rose Madder', id_publisher=3)
book4 = Books(title='From a Buick 8', id_publisher=1)
shop1 = Shops(name='Wordeater')
shop2 = Shops(name='Singer')
shop3 = Shops(name='Maze')
stock1 = Stocks(id_book=3, id_shop=1, count=3)
stock2 = Stocks(id_book=2, id_shop=2, count=13)
stock3 = Stocks(id_book=1, id_shop=3, count=12)
stock4 = Stocks(id_book=4, id_shop=1, count=6)
stock5 = Stocks(id_book=3, id_shop=2, count=10)
sale1 = Sales(price=770, date_sale='2018-6-1', id_stock=2, count=4)
sale2 = Sales(price=360, date_sale='2017-11-3', id_stock=4, count=4)
sale3 = Sales(price=90, date_sale='2017-8-14', id_stock=1, count=7)
sale4 = Sales(price=920, date_sale='2021-6-5', id_stock=3, count=4)
sale5 = Sales(price=720, date_sale='2019-6-6', id_stock=5, count=7)
sale6 = Sales(price=480, date_sale='2021-7-2', id_stock=2, count=9)

session.add_all([publisher1, publisher2, publisher3,
                 book1, book2, book3, book4,
                 shop1, shop2, shop3,
                 stock1, stock2, stock3, stock4, stock5,
                 sale1, sale2, sale3, sale4, sale5, sale6])
session.commit()

def subquery1(some_input):
    try:
        subq1 = (session.query(Books).join(Publishers.books)
                 .filter(Publishers.id == int(some_input)).subquery())
    except ValueError:
        subq1 = (session.query(Books).join(Publishers.books)
                 .filter(Publishers.name == some_input).subquery())
    return subq1

def title_list(some_input):
    list_of_title = []
    try:
        query = (session.query(Books).join(Publishers.books)
                 .filter(Publishers.id == int(some_input)))
    except ValueError:
        query = (session.query(Books).join(Publishers.books)
                 .filter(Publishers.name == some_input))
    for a in query.all():
        list_of_title.append(a.title)
    return list_of_title

def subquery2(subq):
    subq2 = (session.query(Stocks).join(subq,Stocks.id_book == subq.c.id)
             .subquery())
    return subq2

def shop_name_list(subq2):
    list_of_shop_name = []
    subq3 = session.query(Shops).join(subq2, Shops.id == subq2.c.id_shop)
    for j in subq3.all():
        list_of_shop_name.append(j.name)
    return list_of_shop_name

def price_list(subq2):
    list_of_price = []
    subq4 = session.query(Sales).join(subq2, Sales.id_stock == subq2.c.id)
    for i in subq4.all():
        list_of_price.append(str(i.price))
    return list_of_price

def date_sale_list(subq2):
    list_of_date_sale = []
    subq4 = session.query(Sales).join(subq2, Sales.id_stock == subq2.c.id)
    for i in subq4.all():
        list_of_date_sale.append(str(i.date_sale))
    return list_of_date_sale

def merge_lists(a,b,c, d):
    merged_list = [' | '.join(x) for x in zip(a, b, c, d)]
    for i in merged_list:
        print(i)

publisher_name_or_id = input("Input publisher's name or id:")
subq = subquery2(subquery1(publisher_name_or_id))
merge_lists(title_list(publisher_name_or_id),
            shop_name_list(subq),
            price_list(subq),
            date_sale_list(subq))

session.close()