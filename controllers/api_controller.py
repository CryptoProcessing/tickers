from flask import request, make_response, jsonify, abort
from flask.views import MethodView
from flask import current_app
from ticker.models import Ticker, Pair, Market
from sqlalchemy.sql import func


class PriceApi(MethodView):
    """ Операции с аккаунтом """
    def query(self):
        """
        SELECT pairs.name AS pairs_name, avg(anon_1.tickers_bid) AS avg
        FROM
            (SELECT tickers.id AS tickers_id,
                tickers.date AS tickers_date,
                tickers.pair_id AS tickers_pair_id,
                tickers.bid AS tickers_bid,
                tickers.ask AS tickers_ask,
                tickers.market_id AS tickers_market_id
            FROM tickers
            WHERE tickers.id IN
                (SELECT max(tickers.id) AS max
                FROM tickers GROUP BY tickers.market_id, tickers.pair_id)
                ) AS anon_1
        INNER JOIN pairs ON pairs.id = anon_1.tickers_pair_id
        GROUP BY anon_1.tickers_pair_id

        :return:
        """

        max_ids = Ticker \
            .query \
            .with_entities(func.max(Ticker.id).label('max')) \
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

        result = self.query()

        return make_response(jsonify(dict(result))), 200