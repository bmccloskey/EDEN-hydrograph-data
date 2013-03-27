import dj_eden_app.rainfall_data as rainfall_data

import unittest
import datetime

class TestRainfallData(unittest.TestCase):

    def test_exists(self):
        self.assertTrue(rainfall_data.has_rainfall("3B-SE"))
        self.assertFalse(rainfall_data.has_rainfall("NONESUCH"))

    def test_query(self):
        q = rainfall_data.rainfall_query("EDEN_8")
        q_s = str(q)
        print "q =", q_s
        self.assertIn("SELECT", q_s)
        self.assertIn("EDEN_8", q_s)
        self.assertIn("DATETIME", q_s)

    def test_get(self):
        d1 = datetime.datetime(2011, 3, 12, 0, 0)
        d2 = datetime.datetime(2011, 4, 18, 0, 0)

        seq = rainfall_data.rainfall_seq("Broad_River_near_the_Cutoff", beginDate=d1, endDate=d2)

        for t in seq:
            print t
            d_obs = t[0]
            self.assertLessEqual(d1, d_obs, "not less than beginDate")
            self.assertLessEqual(d_obs, d2, "not greater than endDate")

    def test_funky_gage_name(self):
        gage_name = "MET-1"  # yes it exists
        q = rainfall_data.rainfall_query(gage_name)
        self.assertIn(gage_name, str(q))

        seq = rainfall_data.rainfall_seq(gage_name)

        for t in seq:
            self.assertIsNotNone(t[0])

