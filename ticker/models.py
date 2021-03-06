import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError

db = SQLAlchemy()


def get_one_or_create(session,
                      model,
                      create_method='',
                      create_method_kwargs=None,
                      **kwargs):
    try:
        return session.query(model).filter_by(**kwargs).one(), True
    except NoResultFound:
        kwargs.update(create_method_kwargs or {})
        try:
            with session.begin_nested():
                created = getattr(model, create_method, model)(**kwargs)
                session.add(created)
            return created, False
        except IntegrityError:
            return session.query(model).filter_by(**kwargs).one(), True


class Pair(db.Model):
    __tablename__ = "pairs"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    ticker = db.relationship('Ticker', backref='pair', lazy=True)
    is_active = db.Column(TINYINT, default=1)

    def __repr__(self):
        return self.name


class Market(db.Model):
    __tablename__ = "markets"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    market = db.relationship('Ticker', backref='market', lazy=True)
    alias = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return self.name


class Ticker(db.Model):
    """ Tickets Model for storing ticket related details """
    __tablename__ = "tickers"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.DateTime, nullable=False)
    pair_id = db.Column(db.Integer, db.ForeignKey('pairs.id'), nullable=False)
    bid = db.Column(db.Float(precision=32))
    ask = db.Column(db.Float(precision=32))
    market_id = db.Column(db.Integer, db.ForeignKey('markets.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return '{} price - {}, market - {}, date - {}'.format(self.pair, self.bid, self.market, self.date)