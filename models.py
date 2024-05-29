import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Publishers(Base):
    __tablename__ = 'publishers'

    id =sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=80), unique=True, nullable=False)

    books = relationship('Books', back_populates='publisher')

    def __str__(self):
        return f'{self.id} : {self.name}'

class Books(Base):
    __tablename__ = 'books'

    id =sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=150), nullable=False)
    id_publisher = sq.Column(sq.Integer,
                             sq.ForeignKey('publishers.id', ondelete='CASCADE'),
                             nullable=False)

    publisher = relationship('Publishers', back_populates='books')
    #stock = relationship('Stocks', back_populates='books_name')

    def __str__(self):
        return f'{self.id} : {self.title} : {self.id_publisher}'

class Shops(Base):
    __tablename__ = 'shops'

    id =sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=80), unique=True,
                     nullable=False)

    def __str__(self):
        return f'{self.id} : {self.name}'


class Stocks(Base):
    __tablename__ = 'stocks'

    id =sq.Column(sq.Integer, primary_key=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey('books.id', ondelete='CASCADE'),
                        nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey('shops.id', ondelete='CASCADE'),
                        nullable=False)
    count = sq.Column(sq.Integer, nullable=False)

    books = relationship(Books, backref='stocks')
    #books_name = relationship('Books', back_populates='stock')
    shops = relationship(Shops, backref='stocks')

    sale = relationship('Sales', back_populates='stocks')


    def __str__(self):
        return (f'{self.id} : {self.id_book} : {self.id_shop} : '
                f'{self.count}')


class Sales(Base):
    __tablename__ = 'sales'

    id =sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Integer, nullable=False)
    date_sale = sq.Column(sq.Date, nullable=False)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey('stocks.id', ondelete='CASCADE'),
                         nullable=False)
    count = sq.Column(sq.Integer, nullable=False)

    #stocks = relationship(Stocks, backref='sales')
    stocks = relationship('Stocks', back_populates='sale')

    def __str__(self):
        return (f'{self.id} : {self.price} : {self.date_sale} : '
                f'{self.id_stock} : {self.count}')

def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)