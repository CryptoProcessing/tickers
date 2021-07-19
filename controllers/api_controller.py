import datetime

from flask import Response, jsonify, make_response, request
from flask.views import MethodView
from sqlalchemy import Float, String
from sqlalchemy.sql import func

from controllers.utils import get_version
from ticker.models import Market, Pair, Ticker


class PriceApi(MethodView):
    """Операции с аккаунтом"""

    def get(self, **kwargs):
        """
        get info

        :param kwargs:
        :return:
        """

        query_string = request.args

        ts = query_string.get("ts")
        pair = query_string.get("pair")
        market = query_string.get("market")
        format = query_string.get("format")

        result = self._query(ts=ts, pair=pair, market=market, format=format)

        return make_response(jsonify(dict(result))), 200

    def _query(self, ts=None, pair=None, market=None, format=None):
        """
        Main query to get ticker data.
        :return:
        """
        if ts:
            date = datetime.datetime.fromtimestamp(float(ts))
        else:
            date = datetime.datetime.utcnow()

        # ограничение снизу
        min_date = date - datetime.timedelta(hours=8)

        pair_ids = self._get_pair_ids(pair)

        if market:
            # list of filter options
            filter_option = [
                Ticker.created_at < date,
                Ticker.created_at > min_date,
            ]
            try:
                int(market)
                # if market is object market id
                filter_option.append(Market.id == market)
            except ValueError:
                # if market is alias
                filter_option.append(Market.alias == market)

            # from one market
            max_ids = (
                Ticker.query.join(Market)
                .with_entities(func.max(Ticker.id).label("max"))
                .filter(*filter_option)
                .filter(Ticker.pair.has(Pair.id.in_(pair_ids)))
                .group_by(Ticker.pair_id)
            )
        else:
            max_ids = (
                Ticker.query.with_entities(func.max(Ticker.id).label("max"))
                .filter(Ticker.created_at < date, Ticker.created_at > min_date)
                .filter(Ticker.pair.has(Pair.id.in_(pair_ids)))
                .group_by(Ticker.market_id, Ticker.pair_id)
            )

        from sqlalchemy.sql.expression import cast

        result = (
            Ticker.query.filter(Ticker.id.in_(max_ids))
            .from_self()
            .join(Pair)
            .with_entities(
                Pair.name,
                cast(func.avg(Ticker.bid).label("avg"), String if format == "string" else Float),
            )
            .group_by(Ticker.pair_id)
            .all()
        )

        return result

    @staticmethod
    def _get_pair_ids(pair):
        if pair:
            pair_data = Pair.query.filter_by(name=pair).all()
        else:
            pair_data = Pair.query.filter_by(is_active=True).all()
        pair_ids = [p.id for p in pair_data]
        return pair_ids


class MarketApi(MethodView):
    def get(self, **kwargs):
        """
        get market list
        :param kwargs:
        :return:
        """

        result = [{"name": m.name, "id": m.id, "alias": m.alias} for m in (Market.query.all())]
        return make_response(jsonify(result)), 200


class VersionApi(MethodView):
    def get(self, **kwargs):
        result = get_version().split("\n")

        return make_response(jsonify(result)), 200


class CheckerApi(MethodView):
    def get(self, **kwargs):
        """
        Проверка наличия в базе запесей за последние 'time_shift' минут

        Использование:

        GET /api/check
        """

        result = Ticker.query.count()

        help_string = (
            "# HELP saved_tickers_count The number of stored records"
            " in the DB.\n"
            "# TYPE saved_tickers_count counter\n"
        )
        metric = "{} saved_tickers_count {}\n".format(help_string, result)
        return Response(metric, mimetype="text/plain; version=0.0.4")
