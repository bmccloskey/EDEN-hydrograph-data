from django.forms import Form, DateField, MultipleChoiceField, SelectMultiple, DateInput, IntegerField, ChoiceField, Select, CheckboxSelectMultiple, ValidationError
from models import Station
import datetime
from dj_eden_app.data_params import DataParams
from dateutil.relativedelta import relativedelta
import string

def convert_qs_to_list_of_tuples(qs):
    """
    creates a list of tuples which is used for the multi-select list
    on the application. The first element is the key, the second is the
    displayed name.
    """
    choice_list = [ (mod_obj.station_name_web,
                     mod_obj.short_name.replace('_', ' '))
                   for mod_obj in qs]
    return choice_list

class TimeSeriesFilterForm(Form):

    stations = Station.objects.filter(edenmaster_start__isnull=False).order_by('station_name_web')  # returns stations where data collection has started
    today = datetime.date.today()
    timeseries_start = DateField(required=False,
                                 initial=today-relativedelta(months=1),
                                 widget=DateInput(attrs={"size":"10"}))
    timeseries_end = DateField(required=False,
                               initial=today,
                               widget=DateInput(attrs={"size":"10"}))
    site_list = MultipleChoiceField(choices=convert_qs_to_list_of_tuples(stations),
                                    required=True,
                                    widget=SelectMultiple(attrs={'size':'20'}))
    max_count = IntegerField(required=False)

    def clean(self):
        cleaned_data = self.cleaned_data
        t_start = cleaned_data['timeseries_start']
        t_end = cleaned_data['timeseries_end']
        try:
            selected_sites = cleaned_data['site_list']
        except KeyError:
            selected_sites = None

        if selected_sites == None: 
            raise ValidationError('Please select a site.')

        if t_start != None and t_end != None:
            if t_start > t_end:
                raise ValidationError('Please enter a start date that precedes the end date.')
        else:
            pass
                  
        return cleaned_data

class DataParamForm(Form):
    stations = Station.objects.filter(edenmaster_start__isnull=False).order_by('station_name_web')  # returns stations where data collection has started
    param_choices = [ (v, string.capwords(v)) for v in DataParams()]
    today = datetime.date.today()
    timeseries_start = DateField(required=False,
                                 initial=today-relativedelta(months=1),
                                 widget=DateInput(attrs={"size":"10"}))
    timeseries_end = DateField(required=False,
                               initial=today,
                               widget=DateInput(attrs={"size":"10"}))
    site_list = ChoiceField(choices=convert_qs_to_list_of_tuples(stations),
                                    required=True,
                                    widget=Select(attrs={'size':'20'}))
    params = MultipleChoiceField(choices=param_choices,
                                 required=True,
                                 widget=CheckboxSelectMultiple)
    
    def clean(self):
        cleaned_data = self.cleaned_data
        t_start = cleaned_data['timeseries_start']
        t_end = cleaned_data['timeseries_end']
        try:
            selected_sites = cleaned_data['site_list']
        except KeyError:
            selected_sites = None
            
        if selected_sites == None: 
            raise ValidationError('Please select a site.')
        
        if t_start != None and t_end != None:
            if t_start > t_end:
                raise ValidationError('Please enter a start date that precedes the end date.')
        else:
            pass
            
        return cleaned_data
