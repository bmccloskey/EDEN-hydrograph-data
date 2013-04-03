import unittest
from dj_eden_app.plottable import Plottable, NoData

class TestPlottable(unittest.TestCase):
    def test_rainfall(self):
        pt = Plottable("GAGE", "rainfall")
        self.assertEquals(pt.gage_name, "GAGE")
        self.assertEquals(pt.param, "rainfall")

    def test_oops_1(self):
        with self.assertRaises(TypeError):
            pt = Plottable("GAGE", "bogus")
            print pt.data_url()

    def test_no_data_neg(self):
        with self.assertRaises(NoData):
            pt = Plottable("2A300", "temperature")
            for t in pt.sequence():
                print t

    def test_plot_data_url(self):
        pt = Plottable("EDEN_7", "salinity", "2012-03-01", "2012-04-01")
        url = pt.data_url()
        print url
        self.assertEquals(url, "/eden/param_data_download?site_list=EDEN_7&params=salinity&timeseries_start=2012-03-01&timeseries_end=2012-04-01")

    def test_id(self):
        pt = Plottable("EDEN_7", "temperature", "2012-03-01", "2012-04-01")
        self.assertEquals("EDEN_7_temperature", pt.id())

    def test_labels(self):
        pt = Plottable("EDEN_3", "salinity", "2012-03-01", "2012-04-01")
        self.assertEquals("Date", pt.label_x())
        self.assertEquals("Salinity", pt.label_y())

    def test_station_title(self):
        class MockStation(object):
            station_name_web = "EDEN_3"
            short_name = "a_test_name"

        pt = Plottable(MockStation(), "temperature", "2004-02-01", "2004-04-01")
        self.assertEquals("A Test Name", pt.title())
        self.assertEquals("EDEN_3", pt.gage_name)
        self.assertIn("Temperature", pt.label_y())

    def test_no_data_pos(self):
        pt = Plottable("EDEN_3", "salinity", "2012-03-01", "2012-04-01")
        for t in pt.sequence():
            self.assertEquals(2, len(t))

