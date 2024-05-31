import sqlalchemy
import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy import select

DSN = 'postgresql://postgres:Lisyona@localhost:5432/books'
engine = sqlalchemy.create_engine(DSN)
Session = sessionmaker(bind = engine)
session = Session()
Base = declarative_base()
class Publisher(Base):
    __tablename__ = "publisher"

    pk = sq.Column(sq.Integer, primary_key=True)
    publisher_name = sq.Column(sq.String(length=40), unique=True)
class Book(Base):
    __tablename__ = "book"

    pk = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.Text, nullable=False)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey("publisher.pk"), nullable=False)

    publisher_pointer = relationship("Publisher", backref="edited_book")
    book_pointer = relationship("Stock", backref="delivered_book")

class Stock(Base):
    __tablename__ = "stock"

    pk = sq.Column(sq.Integer, primary_key=True)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey("shop.pk"), nullable=False)
    id_book = sq.Column(sq.Integer, sq.ForeignKey("book.pk"), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)

class Shop(Base):
    __tablename__ = "shop"

    pk = sq.Column(sq.Integer, primary_key=True)
    shop_name = sq.Column(sq.Text, nullable=False)

    shop_pointer = relationship("Stock", backref="shop_to_deliver")

class Sale(Base):
    __tablename__ = "sale"

    pk = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Float, nullable=False)
    sale_date = sq.Column(sq.DATE, nullable=False)
    count = sq.Column(sq.Integer, nullable=False)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey("stock.pk"), nullable=False)

    stock_pointer = relationship("Stock", backref="sales")
def create_tables(engine):
    Base.metadata.create_all(engine)

def queer_shops(publisher_input):
    shops = []
    if publisher_input.isdigit()==True:
        stmt = books.session.query(Shop).join(Stock.id_book).join(Book.id_publisher).join(Publisher.pk).where(Publisher.pk==publisher_input)
    else:
        stmt = books.session.query(Shop).join(Stock.id_book).join(Book.id_publisher).join(Publisher.pk).where(Publisher.publisher_name==publisher_input)
    for shop_point in session.scalars(stmt).all():
        shops.append(shop_point)
    return(shops)