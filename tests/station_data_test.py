import dj_eden_app.data_queries as station_data
import dj_eden_app.views.data_views as data_views

from decimal import Decimal
import unittest


gages = ['G-3567', '2A300']
stations = data_views.station_list(gages)
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

if __name__ == '__main__':
    unittest.main()


