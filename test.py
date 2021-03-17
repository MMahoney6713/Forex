
from unittest import TestCase
from app import app
from flask import session
from functions import *


class ForexTests(TestCase):
    def setUp(self):
        """Setup the test client for all tests"""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Information in HTML is displayed"""

        with self.client:
            response = self.client.get('/')
            self.assertIn(
                b'<form action="/convert" method="POST">', response.data)

    def test_forex_form_submit(self):
        """Form is submitted and returns response status code of 302 for redirect to homepage"""

        data = {'convertFrom': 'USD', 'convertTo': 'EUR', 'amount': '50'}

        with self.client:
            response = self.client.post('/convert', data=data)
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.location, 'http://localhost/result')

    def test_forex_form_submit_redirects(self):
        """Form redirect results in status code 200"""

        data = {'convertFrom': 'USD', 'convertTo': 'USD', 'amount': '50'}

        with self.client:
            response = self.client.post(
                '/convert', data=data, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'The result is US$50.0', response.data)

    def test_flashed_messages(self):
        """Flashed messages appear"""

        data = {'convertFrom': 'Lame', 'convertTo': 'Cool', 'amount': '$$'}

        with self.client:
            response = self.client.post(
                '/convert', data=data, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Not a valid code: Lame', response.data)
            self.assertIn(b'Not a valid code: Cool', response.data)
            self.assertIn(b'Not a valid amount: $$', response.data)


class FunctionTests(TestCase):
    def test_is_currency_code_format(self):
        """User currency code input is in the form of 3 english characters"""

        self.assertTrue(is_currency_code_format("USD"))
        self.assertFalse(is_currency_code_format("US!"))
        self.assertFalse(is_currency_code_format("USSR"))
        self.assertFalse(is_currency_code_format("  D"))

    def test_is_number_format(self):
        """User amount input is in the form of a positive number"""

        self.assertTrue(is_number_format('0'))
        self.assertTrue(is_number_format('1000000000000000000000'))
        self.assertFalse(is_number_format('-20'))
        self.assertFalse(is_number_format('USD'))

    def test_is_real_currency_code(self):
        """Error is raised and handled with invalid currency code inputs"""

        self.assertTrue(is_real_currency_code('USD'))
        self.assertFalse(is_real_currency_code('ZZZ'))

    def test_convert_currency(self):
        """Currency is accurately converted"""

        self.assertEqual(convert_currency('USD', 'USD', '50'), 'US$50.0')
