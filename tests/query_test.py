import dj_eden_app.station_data as station_data
import dj_eden_app.views.data_views as data_views

from decimal import Decimal
import unittest


gages = ['G-3567', '2A300']
stations = data_views.station_list(gages)
dt = station_data.date_col()

class TestStationData(unittest.TestCase):

    def check(self, q, data_cols, flag_cols):
        "Exercise a query and check the results"
        print "-query"
        print str(q)

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

        print "hourly query"
        q = station_data.hourly_query(*stations)
        q = q.where(dt >= '2003-07-20')
        self.check(q, ['G-3567', '2A300'], ['G-3567 flag', '2A300 flag'])

    def test_daily(self):
        print "daily query"
        q = station_data.daily_query(*stations)
        q = q.where(dt > '2003-06-28')
        self.check(q, ['G-3567 avg', '2A300 avg'], ['G-3567 flag', '2A300 flag'])

if __name__ == '__main__':
    unittest.main()


