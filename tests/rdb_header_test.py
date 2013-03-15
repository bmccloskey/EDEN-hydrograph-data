import dj_eden_app.download_header as download_header
from dj_eden_app.models import Station
from dj_eden_app.eden_headers import HEADER_MESSAGE, EDEN_CONTACT, END_OF_HEADER

import unittest

class TestRDBHeaders(unittest.TestCase):

    def test_create_metadata_header(self):
        gages = ['2A300', ]
        station_qs = Station.objects.filter(station_name_web__in=gages)
        query_info = {"key1": "value1", "key2":"value2"}

        hh = download_header.create_metadata_header("message", "contact", "header_end", query_info, station_qs)
        self.assertIsInstance(hh, list)
        i = 0
        self.assertEquals("message", hh[i]); i += 1
        self.assertEquals("contact", hh[i]); i += 1
        self.assertTrue("Retrieved" in hh[i]); i += 1
        self.assertTrue("parameters" in hh[i]); i += 1
        self.assertTrue("2A300" in hh[i]); i += 1
        self.assertTrue("parameter codes" in hh[i]); i += 1
        self.assertTrue("Note" in hh[i]); i += 1
        self.assertTrue("key" in hh[i]); i += 1
        self.assertTrue("key" in hh[i]); i += 1
        self.assertEquals("header_end", hh[i]); i += 1

    def test_header_crlf(self):
        station_qs = []
        query_info = {"key1": "value1", "key2":"value2"}

        hh = download_header.create_metadata_header(HEADER_MESSAGE, EDEN_CONTACT, END_OF_HEADER, query_info, station_qs)

        self.assertIsInstance(hh, list)
        # let the writer add the line endings
        for h in hh:
            self.assertFalse("\n" in h, "contains newline:" + h)
            self.assertFalse("\r" in h, "contains carriage return:" + h)


if __name__ == '__main__':
    unittest.main()


