import sqlalchemy
import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from model import create_tables, Publisher, Book, Shop, Stock, Sale, queer_shops
import ast

DSN = 'postgresql://postgres:Lisyona@localhost:5432/books'
engine = sqlalchemy.create_engine(DSN)
Session = sessionmaker(bind = engine)
session = Session()
Base = declarative_base()

Base.metadata.create_all(engine)

with open('python ORM data for db.txt', 'r', encoding='utf-8') as file:
    data = file.read()
    book_data = ast.literal_eval(data)
    
    for record in book_data:
        model = {
            'publisher': Publisher,
            'shop': Shop,
            'book': Book,
            'stock': Stock,
            'sale': Sale,
        }[record.get('model')]
        session.add(model(pk=record.get('pk'), **record.get('fields')))
    session.commit()

publisher_input = input('Введите название издательства или его индекс ').title()
print(queer_shops(publisher_input))

session.close()