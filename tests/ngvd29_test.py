from dj_eden_app.views.data_views import _hourly_plot_data, _daily_plot_data, get_ngvd29_conversion
from dj_eden_app.forms import TimeSeriesFilterForm

from types import FloatType
import unittest

single_gage = ['2A300']

class TestNgvd29Conversion(unittest.TestCase):
           
    def test_hourly_get_conversion(self):
        gage_object = single_gage
        post_dict = {'site_list': gage_object, 'timeseries_start': '2012-03-15', 'timeseries_end': '2012-03-16'}
        query_form = TimeSeriesFilterForm(post_dict)
        self.assertTrue(query_form.is_valid())
        data, beginDate, endDate, station = _hourly_plot_data(query_form)
        ngvd29_correction = get_ngvd29_conversion(station)
        self.assertIsNotNone(data)
        self.assertIsNotNone(beginDate)
        self.assertIsNotNone(endDate)
        if type(ngvd29_correction) is float:
            ngvd29_returned = True
        else:
            ngvd29_returned = False
        self.assertTrue(ngvd29_returned)
        
    def test_daily_get_conversion(self):
        gage_object = single_gage
        post_dict = {'site_list': gage_object, 'timeseries_start': '2000-03-15', 'timeseries_end': '2012-03-16'}
        query_form = TimeSeriesFilterForm(post_dict)
        self.assertTrue(query_form.is_valid())
        data, beginDate, endDate, station = _daily_plot_data(query_form)
        ngvd29_correction = get_ngvd29_conversion(station)
        self.assertIsNotNone(data)
        self.assertIsNotNone(beginDate)
        self.assertIsNotNone(endDate)
        if type(ngvd29_correction) is float:
            ngvd29_returned = True
        else:
            ngvd29_returned = False
        self.assertTrue(ngvd29_returned)

        
if __name__ == '__main__':
    unittest.main()