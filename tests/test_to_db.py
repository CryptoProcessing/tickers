import unittest
import datetime
from ticker.models import db
from ticker.models import Ticker, Pair, Market
from controllers.tasks import to_db
from tests.base import BaseTestCase
from tests.response_mock import therock_expected_response


class TestToDb(BaseTestCase):

    def setUp(self):
        super(TestToDb, self).setUp()
        to_db('therock.com', therock_expected_response)

    def test_save_to_db(self):

        pairs = Pair.query.all()

        market = Market.query.all()

        self.assertEqual(len(pairs), 2)
        self.assertEqual(len(market), 1)


if __name__ == '__main__':
    unittest.main()