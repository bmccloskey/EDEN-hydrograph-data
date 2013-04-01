from django.core.urlresolvers import reverse
from dj_eden_app.data_params import DataParams
from dj_eden_app.coastal_data import coastal_seq
from dj_eden_app.rainfall_data import rainfall_seq

import string

class NoData(Exception):
    def __init__(self, gage, param):
        self.gage = gage
        self.param = param
    def __str__(self):
        return ",".join([repr(self.gage), repr(self.param)])

class Plottable(object):
    """
    Plottable.
    """
    def __init__(self, station=None, param=None, beginDate=None, endDate=None):
        self.station = station
        try:
            self.gage_name = station.station_name_web
        except AttributeError:
            self.gage_name = str(station)
        self.param = param
        self.beginDate = beginDate
        self.endDate = endDate
        if param == DataParams.rainfall:
            self.sequence = self._rainfall_sequence
        elif param in [DataParams.salinity, DataParams.stage, DataParams.temperature]:
            self.sequence = self._coastal_sequence
        else:
            raise TypeError

    def data_url(self):
        base = reverse("param_data_download")
        url = base + "?" + "site_list=" + self.gage_name + "&" + "params=" + self.param
        if self.beginDate:
            url += "&timeseries_start=" + str(self.beginDate)
        if self.endDate:
            url += "&timeseries_end=" + str(self.endDate)

        return url

    def rdb_url(self):
        base = reverse("param_rdb_download")
        url = base + "?" + "site_list=" + self.gage_name + "&" + "params=" + self.param
        if self.beginDate:
            url += "&timeseries_start=" + str(self.beginDate)
        if self.endDate:
            url += "&timeseries_end=" + str(self.endDate)

        return url

    def image_url(self, logo=False):
        base = reverse("plot_image_simple")
        url = base + "?" + "site_list=" + self.gage_name + "&" + "params=" + self.param
        if self.beginDate:
            url += "&timeseries_start=" + str(self.beginDate)
        if self.endDate:
            url += "&timeseries_end=" + str(self.endDate)
        if not logo:
            url += "&no_logo"
        return url

    def image_url_hq(self):
        return self.image_url(logo=True)

    def label_x(self):
        return "Date"

    def label_y(self):
        unit_dict = {DataParams.temperature: 'degrees C',
                  DataParams.rainfall: None,
                  DataParams.salinity: None,
                  DataParams.stage: 'ft'}
        label_unit = unit_dict[self.param]
        nm = self.name()

        if label_unit:
            y_axis_label = '%s (%s)' % (nm, label_unit)
        else:
            y_axis_label = nm
        return y_axis_label

    def name(self):
        return str(self.param).capitalize()

    def title(self):
        try:
            name = self.station.short_name
        except AttributeError:
            name = self.gage_name
        name = name.replace("_", " ")
        name = string.capwords(name)

        # TODO Perhaps add date params?
        return name

    def has_data(self):
        # TODO Make this less wasteful
        try:
            self.sequence()
            return True
        except NoData:
            return False

    def id(self):
        "suitable for constructing an HTML id"
        return self.gage_name + "_" + self.param

    def _coastal_sequence(self):
        try:
            return coastal_seq(self.gage_name, self.param, beginDate=self.beginDate, endDate=self.endDate)
        except KeyError:
            raise NoData(self.gage_name, self.param)

    def _rainfall_sequence(self):
        try:
            return rainfall_seq(self.gage_name, beginDate=self.beginDate, endDate=self.endDate)
        except KeyError:
            raise NoData(self.gage_name, self.param)

if __name__ == "__main__":
    pt = Plottable("2A300", "rainfall")
    print pt


