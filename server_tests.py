import json
import unittest
from server import app


class ServerTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_correct_hello_handler(self):
        response = self.app.get('/hello')
        self.assertEqual(response.get_data(as_text=True), "HSE OneLove!")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "text/plain")

    def test_correct_set_and_get_key_value(self):
        response = self.app.post('/set',
                                 data=json.dumps({'key': 'k1'}),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_data(as_text=True), "")
        response = self.app.post('/set',
                                 data=json.dumps({'value': 'v1'}),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_data(as_text=True), "")
        response = self.app.post('/set',
                                 data=json.dumps({'key': 'k1', 'value': 'v1'}),
                                 content_type='')
        self.assertEqual(response.status_code, 415)
        self.assertEqual(response.get_data(as_text=True), "")
        response = self.app.post('/set',
                                 data=json.dumps({'key': 'k1', 'value': 'v1'}))
        self.assertEqual(response.status_code, 415)
        self.assertEqual(response.get_data(as_text=True), "")
        response = self.app.post('/set', data=json.dumps({'key': 'k1', 'value': 'v1'}), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_data(as_text=True), "")
        response = self.app.get('/get/k1')
        self.assertEqual(response.get_data(as_text=True), json.dumps({'key': 'k1', 'value': 'v1'}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")
        response = self.app.get('/get/k2')
        self.assertEqual(response.get_data(as_text=True), "")
        self.assertEqual(response.status_code, 404)

    def test_correctness_division(self):
        response = self.app.post('/devide',
                                 data=json.dumps({'dividend': 9}),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_data(as_text=True), "")
        response = self.app.post('/devide',
                                 data=json.dumps({'divider': 3}),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_data(as_text=True), "")
        response = self.app.post('/devide',
                                 data=json.dumps({'dividend': 9, 'divider': 0}),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_data(as_text=True), "")
        response = self.app.post('/devide',
                                 data=json.dumps({'dividend': 9, 'divider': 3}),
                                 content_type='')
        self.assertEqual(response.status_code, 415)
        self.assertEqual(response.get_data(as_text=True), "")
        response = self.app.post('/devide',
                                 data=json.dumps({'dividend': 9, 'divider': 3}))
        self.assertEqual(response.status_code, 415)
        self.assertEqual(response.get_data(as_text=True), "")
        response = self.app.post('/devide',
                                 data=json.dumps({'dividend': 9, 'divider': 3}), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'text/plain')
        self.assertEqual(response.get_data(as_text=True), str(3.0))

    def test_handle_exception(self):
        response = self.app.post('/hello')
        self.assertEqual(response.get_data(as_text=True), "")
        self.assertEqual(response.status_code, 405)
        response = self.app.post('/')
        self.assertEqual(response.get_data(as_text=True), "")
        self.assertEqual(response.status_code, 405)
        response = self.app.post('/hello/')
        self.assertEqual(response.get_data(as_text=True), "")
        self.assertEqual(response.status_code, 405)
        response = self.app.get('/set')
        self.assertEqual(response.get_data(as_text=True), "")
        self.assertEqual(response.status_code, 405)
        response = self.app.post('/get/k1')
        self.assertEqual(response.get_data(as_text=True), "")
        self.assertEqual(response.status_code, 405)


if __name__ == '__main__':
    unittest.main()
