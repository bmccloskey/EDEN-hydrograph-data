import dj_eden_app.forms as forms
from dj_eden_app.models import Station

import unittest

class TestChoiceLists(unittest.TestCase):

    def test_convert_qs_to_list_of_tuples(self):
        stationlist = Station.objects.filter(edenmaster_start__isnull=False).order_by('station_name_web')  # returns stations where data collection has started
        tuplist = forms.convert_qs_to_list_of_tuples(stationlist)
        self.assertEquals(len(stationlist), len(tuplist), "equal length")

        self.assertEquals([s.station_name_web for s in stationlist],
                          [t[0] for t in tuplist],
                          "keys match")
        # next test is data-dependant, but if it fails, there's no point in having the underlying code
        self.assertNotEqual([s.station_name_web for s in stationlist],
                          [t[1] for t in tuplist],
                          "something differs")
