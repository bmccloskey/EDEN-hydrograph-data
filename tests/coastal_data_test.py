import dj_eden_app.coastal_data as coastal_data

import unittest
import datetime

class TestcoastalData(unittest.TestCase):

    def test_exists(self):
        self.assertTrue(coastal_data.has_coastal_data("G-3777", "salinity"))
        self.assertTrue(coastal_data.has_coastal_data("G-3777", "stage"))
        self.assertTrue(coastal_data.has_coastal_data("G-3777", "temperature"))
        self.assertTrue(coastal_data.has_coastal_data("Alligator_Creek", "stage"))
        self.assertFalse(coastal_data.has_coastal_data("Alligator_Creek", "salinity"))
        self.assertTrue(coastal_data.has_coastal_data("EDEN_3", "salinity"))
        self.assertFalse(coastal_data.has_coastal_data("NONESUCH", "salinity"))
        self.assertFalse(coastal_data.has_coastal_data("EDEN_3", "random"))

    def test_query(self):
        q = coastal_data.coastal_query("Joe_Bay_2E", "temperature")
        q_s = str(q)
        print "q =", q_s
        self.assertIn("SELECT", q_s)
        self.assertIn("Joe_Bay_2E", q_s)
        self.assertIn("DATETIME", q_s.upper())
        self.assertIn("temperature".upper(), q_s.upper())

    def test_get(self):
        d1 = datetime.datetime(2011, 3, 12, 4, 31)
        d2 = datetime.datetime(2011, 3, 12, 22, 59)

        seq = coastal_data.coastal_seq("Lostmans_River_below_Second_Bay", "salinity", beginDate=d1, endDate=d2)

        for t in seq:
            print t
            d_obs = t[0]
            self.assertLessEqual(d1, d_obs, "not less than beginDate")
            self.assertLessEqual(d_obs, d2, "not greater than endDate")

    def test_funky_gage_name(self):
        gage_name = "G-3777"  # yes it exists
        q = coastal_data.coastal_query(gage_name, "stage")
        self.assertIn(gage_name, str(q))

        seq = coastal_data.coastal_seq(gage_name, "stage")

        for t in seq:
            self.assertIsNotNone(t[0])

