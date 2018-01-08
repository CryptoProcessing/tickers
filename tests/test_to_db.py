import unittest
from ticker.models import Pair, Market, Ticker
from controllers.tasks import to_db
from tests.base import BaseTestCase
from tests.response_mock.response_mock import therock_expected_response


class TestToDb(BaseTestCase):

    def setUp(self):
        super(TestToDb, self).setUp()
        to_db('therock.com', therock_expected_response)

    def test_save_to_db(self):

        pairs = Pair.query.all()

        market = Market.query.all()

        tickers = Ticker.query.all()

        self.assertEqual(len(pairs), 2)
        self.assertEqual(len(market), 1)
        self.assertEqual(len(tickers), 2)


if __name__ == '__main__':
    unittest.main()