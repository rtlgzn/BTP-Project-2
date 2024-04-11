import unittest
import http.client
import json

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.conn = http.client.HTTPConnection("localhost", 8000)

    def tearDown(self):
        self.conn.close()

    #TESTING to get all reservations for a account
    def test_get_reservations(self):
        valid_token = 'token' #replace with token after logging in 

        headers = {'Authorization': f'Bearer {valid_token}'}
        self.conn.request("GET", "/reservations", headers=headers)

        response = self.conn.getresponse()
        self.assertEqual(response.status, 200)

        data = json.loads(response.read())
        self.assertIsInstance(data, list)
        print(data)


if __name__ == '__main__':
    unittest.main()