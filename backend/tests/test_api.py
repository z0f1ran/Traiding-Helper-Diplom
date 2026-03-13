import unittest

from app import create_app
from app.extensions import db


class ApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(
            {
                'TESTING': True,
                'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
                'SQLALCHEMY_TRACK_MODIFICATIONS': False,
            }
        )
        self.client = self.app.test_client()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_health(self):
        response = self.client.get('/api/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'success')

    def test_create_order(self):
        response = self.client.post('/api/orders', json={'symbol': 'BTCUSDT', 'side': 'buy', 'quantity': 0.01})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['status'], 'success')


if __name__ == '__main__':
    unittest.main()