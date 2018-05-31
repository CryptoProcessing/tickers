import datetime
from controllers.utils import get_version
from flask import request, make_response, jsonify
from flask.views import MethodView
from ticker.models import Ticker, Pair, Market
from sqlalchemy.sql import func
from sqlalchemy.orm import load_only


class PriceApi(MethodView):
    """ Операции с аккаунтом """
    def query(self, ts=None, pair=None, market=None, market_id=None):
        """
        SELECT pairs.name AS pairs_name, avg(anon_1.tickers_bid) AS avg
        FROM (SELECT tickers.id AS tickers_id,
                tickers.date AS tickers_date,
                tickers.pair_id AS tickers_pair_id,
                tickers.bid AS tickers_bid,
                tickers.ask AS tickers_ask,
                tickers.market_id AS tickers_market_id,
                tickers.created_at AS tickers_created_at
            FROM tickers
            WHERE tickers.id IN (SELECT max(tickers.id) AS max
                FROM tickers
                WHERE tickers.created_at < %(created_at_1)s AND (EXISTS (SELECT 1
                FROM pairs
                WHERE pairs.id = tickers.pair_id
                    AND pairs.id IN (%(id_1)s)))
                GROUP BY tickers.market_id, tickers.pair_id)) AS anon_1
            INNER JOIN pairs ON pairs.id = anon_1.tickers_pair_id
        GROUP BY anon_1.tickers_pair_id

        :return:
        """
        if ts:
            date = datetime.datetime.utcfromtimestamp(float(ts))
        else:
            date = datetime.datetime.now()

        # ограничение снизу
        min_date = date - datetime.timedelta(hours=10)

        if pair:
            pair_data = Pair.query.filter_by(name=pair).all()
        else:
            pair_data = Pair.query.all()

        pairids = [p.id for p in pair_data]

        if market_id:
            # from one market
            max_ids = Ticker \
                .query \
                .join(Market) \
                .with_entities(func.max(Ticker.id).label('max')) \
                .filter(Ticker.created_at < date, Ticker.created_at > min_date, Market.id == market_id) \
                .filter(Ticker.pair.has(Pair.id.in_(pairids))) \
                .group_by(Ticker.pair_id)
        else:
            max_ids = Ticker \
                .query \
                .with_entities(func.max(Ticker.id).label('max')) \
                .filter(Ticker.created_at < date, Ticker.created_at > min_date) \
                .filter(Ticker.pair.has(Pair.id.in_(pairids)))\
                .group_by(Ticker.market_id, Ticker.pair_id)

        result = Ticker \
            .query \
            .filter(Ticker.id.in_(max_ids)) \
            .from_self() \
            .join(Pair) \
            .with_entities(Pair.name, func.avg(Ticker.bid).label('avg')) \
            .group_by(Ticker.pair_id) \
            .all()

        return result

    def get(self, **kwargs):
        """
        get info

        :param kwargs:
        :return:
        """
        query_string = request.args
        ts = query_string.get('ts')
        pair = query_string.get('pair')
        market = query_string.get('market')

        result = self.query(ts=ts, pair=pair, market_id=market)

        return make_response(jsonify(dict(result))), 200


class MarketApi(MethodView):

    def get(self, **kwargs):
        """
        get market list
        :param kwargs:
        :return:
        """

        result = [{'name': m.name, 'id': m.id} for m in (Market.query.all())]
        return make_response(jsonify(result)), 200


class VersionApi(MethodView):

    def get(self, **kwargs):
        result = get_version().split('\n')

        return make_response(jsonify(result)), 200