from django.test.client import Client
from django.utils import unittest

class TestPageGeneration(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._client = Client()

    def test_eve_page(self):
        resp = self._client.get("/eden/eve.html")
        self.assertIn("sofia", resp.content)
        self.assertEqual(200, resp.status_code)

    def test_param_page(self):
        resp = self._client.get("/eden/eve_params.html")
        self.assertIn("sofia", resp.content)
        self.assertEqual(200, resp.status_code)

    def test_eve_page_error_missing_site(self):
        resp = self._client.get("/eden/eve.html",
                {
                 'timeseries_start':'2013-03-03',
                 'timeseries_end':'2013-04-03',
                 'hydrograph_query':'Update Graph',
        })

        self.assertIn("sofia", resp.content)
        self.assertIn("Please select", resp.content)
        self.assertNotEqual(200, resp.status_code)

    def test_param_page_error_missing_site(self):
        resp = self._client.get("/eden/eve.html",
                {
                 'timeseries_start':'2013-03-03',
                 'timeseries_end':'2013-04-03',
                 'hydrograph_query':'Update Graph',
        })

        self.assertIn("sofia", resp.content)
        self.assertIn("Please select", resp.content)
        self.assertNotEqual(200, resp.status_code)

    def test_eve_page_error_bad_date(self):
        resp = self._client.get("/eden/eve.html",
                {
                 'timeseries_start':'2013-bad-03',
                 'timeseries_end':'2013-04-03',
                 'hydrograph_query':'Update Graph',
                 'site_list':['3AS', 'A13']
        })

        self.assertIn("sofia", resp.content)
        self.assertIn("Enter a valid date", resp.content)
        self.assertNotEqual(200, resp.status_code)

    def test_param_page_error_bad_date(self):
        resp = self._client.get("/eden/eve.html",
                {
                 'timeseries_start':'2013-01-03',
                 'timeseries_end':'2013-janufeb-03',
                 'hydrograph_query':'Update Graph',
                 'site_list':'3AS'
        })

        self.assertIn("sofia", resp.content)
        self.assertIn("Enter a valid date", resp.content)
        self.assertNotEqual(200, resp.status_code)

    def test_eve_page_ok(self):
        resp = self._client.get("/eden/eve.html",
                {
                 'timeseries_start':'2012-03-03',
                 'timeseries_end':'2012-04-03',
                 'hydrograph_query':'Update Graph',
                 'site_list':['3AS', 'A13']
        })

        self.assertIn("sofia", resp.content)
        self.assertEqual(200, resp.status_code)

    def test_param_page_ok(self):
        resp = self._client.get("/eden/eve.html",
                {
                 'timeseries_start':'2012-03-03',
                 'timeseries_end':'2012-04-03',
                 'hydrograph_query':'Update Graph',
                 'site_list':'3AS'
        })

        self.assertIn("sofia", resp.content)
        self.assertEqual(200, resp.status_code)

