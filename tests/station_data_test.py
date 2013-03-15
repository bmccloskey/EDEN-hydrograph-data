import dj_eden_app.data_queries as station_data
import dj_eden_app.views.data_views as data_views
from dj_eden_app.models import station_list

from decimal import Decimal
import unittest


gages = ['G-3567', '2A300']
stations = station_list(gages)
dt = station_data.date_col()

class TestStationData(unittest.TestCase):

    def check(self, q, data_cols, flag_cols):
        "Exercise a query and check the results"
        valid_flags = ['M', 'D', 'E', 'O']
        rs = q.execute()
        for r in rs:
            self.assertGreater(len(r), len(data_cols), len(flag_cols))
            for d in data_cols:
                if r[d] is not None:
                    self.assertIsInstance(r[d], Decimal)
            for f in flag_cols:
                self.assertIn(r[f], valid_flags)

    def test_hourly(self):

        q = station_data.hourly_query(*stations)
        q = q.where(dt >= '2003-07-20')
        self.check(q, ['G-3567', '2A300'], ['G-3567 flag', '2A300 flag'])

    def test_daily(self):

        q = station_data.daily_query(*stations)
        q = q.where(dt >= '2003-06-28')
        self.check(q, ['G-3567 avg', '2A300 avg'], ['G-3567 flag', '2A300 flag'])

    def test_hourly_split(self):

        q = station_data.hourly_query_split(*stations)
        q = q.where(dt >= '2003-07-20')
        rs = q.execute()
        rsk = rs.keys()
        for s in stations:
            web_name = s.station_name_web
            for suffix in ["", " est", " dry"]:
                self.assertIn(web_name + suffix, rsk, "expected rs to have key " + web_name + suffix)
        for r in rs:
            self.assertTrue(r, "valid result row")

    def test_daily_split(self):

        q = station_data.daily_query_split(*stations)
        q = q.where(dt >= '2008-09-20')
        rs = q.execute()
        rsk = rs.keys()
        for s in stations:
            web_name = s.station_name_web
            for suffix in [" avg", " est", " dry"]:
                self.assertIn(web_name + suffix, rsk, "expected rs to have key " + web_name + suffix)
        for r in rs:
            self.assertTrue(r, "valid result row")

    def test_hourly_navd_88(self):
        s = stations[0]
        gage = s.station_name_web
        s.id = None
        s.stationdatum.convert_to_navd88_feet = 200

        q = station_data.hourly_query(s)
        rs = q.execute()
        for r in rs:
            v = r[gage]
            if v is not None:
                self.assertGreater(v, 100, "navd 88 correction, got " + str(v))

    def test_daily_navd_88(self):
        s = stations[0]
        gage = s.station_name_web
        s.id = None
        s.stationdatum.convert_to_navd88_feet = 200

        q = station_data.daily_query(s)
        rs = q.execute()
        for r in rs:
            v = r[gage + ' avg']
            if v is not None:
                self.assertGreater(v, 100, "navd 88 correction, got " + str(v))

    def test_ambiguous_station_name(self):
        "Test for the one station name that produces two separate station records"
        names = ["S150_T"]
        ss = data_views.station_list(names)

        self.assertEqual(len(names), len(ss))
        self.assertEquals(names, [s.station_name_web for s in ss])

    def test_peculiar_station_names(self):
        "Test for peculiar station names"
        names = ['C111_wetland_east_of_FIU_LTER_TSPH5', 'S343A_H']
        ss = data_views.station_list(names)

        self.assertEqual(len(names), len(ss))
        self.assertEquals(names, [s.station_name_web for s in ss])

    def test_duplicate_station_names(self):
        "Test that duplicate station names are collapsed, but otherwise order is preserved"
        names = ["G-3567", "CH1", "RG3", "ANGEL", "BARW4", "TSH", "W2", "W15", "W2", "Upstream_Taylor_River", "TSH", "CH1"]
        ss = data_views.station_list(names)

        names_dedup = ["G-3567", "CH1", "RG3", "ANGEL", "BARW4", "TSH", "W2", "W15", "Upstream_Taylor_River"]
        # self.assertEqual(len(names) - 3, len(ss))
        self.assertEquals(names_dedup, [s.station_name_web for s in ss])

    def test_station_dict(self):
        "Test for station dict"
        names = ["G-3567", "RG3", "ANGEL", "BARW4", "TSH", "W15", "W2", "Upstream_Taylor_River", "CH1"]
        sd = data_views.station_dict(names)

        # self.assertEqual(len(names), len(sd))
        self.assertEquals(names, [s.station_name_web for s in sd.values()])
        self.assertEquals(names, sd.keys())

if __name__ == '__main__':
    unittest.main()


