import json
from ..app import app


import unittest


class AppTestCase(unittest.TestCase):

    def setUp(self):
        self.test_app = app.test_client()

    def test_hello(self):
        response = self.test_app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'{"hello": "world"}')

    def test_repositories_base(self):
        response = self.test_app.get(
            'github/repositories/?username=curiousest'
        )
        self.assertEqual(response.status_code, 200, response.get_data())

    def test_repositories_limit(self):
        response = self.test_app.get(
            '/github/repositories/?username=curiousest&limit=10'
        )
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.data.decode('utf-8'))
        self.assertEqual(len(response_json), 10)

    def test_repositories_order_by(self):
        response = self.test_app.get(
            '/github/repositories/?username=curiousest&limit=10&order_by=-stargazers_count'
        )
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.data.decode('utf-8'))
        self.assertEqual(len(response_json), 10)
        self.assertGreater(
            response_json[0]['stargazers_count'], response_json[-1]['stargazers_count']
        )


if __name__ == '__main__':
    unittest.main()
