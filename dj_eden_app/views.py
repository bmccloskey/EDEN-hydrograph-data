# Create your views here.

import csv
import MySQLdb as mdb

from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.http import HttpResponse

from models import Station
from forms import TimeSeriesFilterForm
from stage_data import create_query_and_colnames

def _csv_dump(qs, outfile_path):
    '''
    Writes the results of a django queryset to csv.
    '''
    
    qs_model = qs.model
    csv_writer = csv.writer(open(outfile_path, 'wb'))
    
    headers = []
    for field in qs_model._meta.fields:
        if field.name != 'id' and field.name != 'flag' and field.name != 'station':
            headers.append(field.name)
    csv_writer.writerow(headers)
    
    for qs_object in qs:
        row = []
        for field in headers:
            value = getattr(qs_object, field)
            if callable(value):
                value = value()
            if type(value) == unicode:
                value = value.encode('utf-8')
            row.append(value)
        csv_writer.writerow(row)
        
def _write_dictionary_to_csv(dic_list, outfile_path, first_column):
    
    '''
    Writes a list of dictionaries to a csv file.
    The dictionary keys appear as headers in the file,
    with "datetime" being the first column.
    '''
    
    key_list = dic_list[0].keys()
    sorted_key_list = []
    for key in key_list:
        if key == first_column:
            sorted_key_list.insert(0, key)
        else:
            sorted_key_list.append(key)
    csv_file = open(outfile_path, 'wb')
    dict_writer = csv.DictWriter(csv_file, sorted_key_list)
    dict_writer.writer.writerow(sorted_key_list)
    dict_writer.writerows(dic_list)
    
def _write_csv_for_download(dj_response, dic_list, first_column):
    
    key_list = dic_list[0].keys()
    sorted_key_list = []
    for key in key_list:
        if key == first_column:
            sorted_key_list.insert(0, key)
        else:
            sorted_key_list.append(key)
    dict_writer = csv.DictWriter(dj_response, sorted_key_list)
    dict_writer.writer.writerow(sorted_key_list)
    dict_writer.writerows(dic_list)
    
    return dj_response
  
        
def _query_mysql(host, user, schema, password, query):
    '''
    Executes a query on a MySQL database and returns
    the results as a list of dictionaries.
    '''
    try:
        con = None
        con = mdb.connect(host, user, password, schema)
        cur = con.cursor()
        cur.execute(query)
        data = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        result = [dict(zip(columns, record)) for record in data]
        
    except mdb.Error, e:
        result = "Error %d: %s" % (e.args[0], e.args[1])
        
    if con:
        con.close()
        
        return result
    
def _generate_error_file(filename, write_list):
    '''
    Writes the contents of a list of a text file.
    Used for troubleshooting purposes (e.g.
    makes sure queries are returned as expected, 
    formatting is correct).
    '''
    target = open(filename, 'wb')
    for item in write_list:
        target.write(str(item))
        target.write('\n')
    target.close()
    
    return 'File writing complete.'

def _generate_safe_station_names(selected_stations, first_column = 'datetime', flags = False):
    """
    Creates a SQL safe list of sites selected by a user.
    This function will also include first_column
    as the first item in the list. The first_column is 'datetime',
    by default. In addition, station flags can also be included if
    flags is set to True; the default is False.
    
    """
    
    list_of_stations = []
    for unicode_station in selected_stations:
        station = unicode_station.encode('utf-8')
        station_name = str(station)
        try:
            string_length = len(station_name)
            plus_position = station_name.rfind('+')
            if plus_position >= 0: # removes plus signs in the event that appear in the station name (doesn't look like it should)
                extranous_text = station_name[plus_position:string_length]
                cleaned_station_name = station_name.replace(extranous_text, "")
            else:
                cleaned_station_name = station_name
            column_name = 'stage_%s' % (cleaned_station_name)
            list_of_stations.append(column_name)
            
            if flags == True:
                flag_name = 'flag_%s' % (cleaned_station_name)
                list_of_stations.append(flag_name)
            else:
                pass
            
        except (ValueError):
            continue
            
    list_of_stations.insert(0, first_column)

    return list_of_stations
    
        
        
"""       
def dygraph_array_creation(qs):
    
    dygraph_data_array = []
    dygraph_label_list = qs[0].keys()
    
    for dictionary in qs:
        dictionary_values = dictionary.values()
        data_json = simplejson.dumps(dictionary_values, use_decimal=True)
        dygraph_data_array.append(data_json)
        
    dygraph_dictionary = {}
    dygraph_dictionary['data'] = dygraph_data_array
    dygraph_dictionary['labels'] = dygraph_label_list
    
    return dygraph_data_array
"""

def eden_page(request):
    """
    Allows a user to select a site,
    date in order to view a dygraph
    plot of results.
    """
    
    template_name = 'hydrograph_query.html'
    
    if request.method == 'GET':
        query_form = TimeSeriesFilterForm(request.GET)

        if not query_form.has_changed():
            return render(request, template_name, {'query_form': query_form,})

        if query_form.is_bound:
            if query_form.is_valid():
                time_start = query_form.cleaned_data['timeseries_start']
                time_end = query_form.cleaned_data['timeseries_end']
                eden_station = query_form.cleaned_data['site_list']

                form_list = [time_start, time_end, eden_station]
                
                _generate_error_file('error.txt', form_list)
                
                get_request = [request.GET]
                
                _generate_error_file('request.txt', get_request)
    
                str_time_start = str(time_start)
                str_time_end = str(time_end)

                         
                if query_form.has_changed():
                    changed = True
                   
                else:
                    pass
                
                station_id_list = []
                for station_id in eden_station:
                    id_number = int(station_id)
                    station_id_list.append(id_number)
                    
                station_queryset = Station.objects.filter(station_id__in = station_id_list)
                
                station_name_list = []
                for station_object in station_queryset:
                    station_web_name = station_object.station_name_web.encode('utf-8')
                    station_name_list.append(station_web_name)
                
                #dygraph_array = dygraph_array_creation(qs)
                
                if u'hydrograph_query' in request.GET:
                    query_columns = _generate_safe_station_names(selected_stations = station_name_list, 
                                                                 first_column = 'datetime', 
                                                                 flags = False)
                    
                    create_query_and_colnames(columnNames = query_columns, 
                                              start_date = str_time_start, 
                                              end_date = str_time_end,
                                              outpath = 'static/data.csv')
                    
                    return render (request, template_name, {'query_form': query_form,
                                                            'changed':changed,
                                                            'time_start': str(time_start),
                                                            'time_end': str(time_end)
                                                                      })
                                                        
                 
                if u'download_query' in request.GET:
                    query_columns = _generate_safe_station_names(selected_stations = station_name_list, 
                                                                 first_column = 'datetime', 
                                                                 flags = True)
                    response = HttpResponse(content_type = 'text/csv')
                    response['Content-Disposition'] = 'attachment; filename="eden_data_download.csv'
                    
                    create_query_and_colnames(columnNames = query_columns, 
                                                          start_date = str_time_start, 
                                                          end_date = str_time_end,
                                                          outpath = response,
                                                          csv_download = True)

                    return response
                
    else:
        query_form = TimeSeriesFilterForm()
    return render (request, template_name, {'query_form': query_form,})
