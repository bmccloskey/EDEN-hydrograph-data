# Create your views here.

import csv
import MySQLdb as mdb

from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render


from models import *
from forms import TimeSeriesFilterForm
from secure import DB_HOST, DB_PASSWORD, DB_SCHEMA, DB_USER

def _csv_dump(qs, outfile_path):
    
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
        
def _write_dictionary_to_csv(dic_list, outfile_path):
    
    key_list = dic_list[0].keys()
    csv_file = open(outfile_path, 'wb')
    dict_writer = csv.DictWriter(csv_file, key_list)
    dict_writer.writer.writerow(key_list)
    dict_writer.writerows
    
        
def _query_mysql(host, user, schema, password, query):
    
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
                #qs = EdenStageView.objects.filter(datetime__gte = time_start).filter(datetime__lte = time_end).filter(stage = eden_station).only('datetime', 'station')
                '''
                station_query = """
                SELECT stn.station_name
                FROM station stn
                """
                station_where_statement = "WHERE stn.station_id = '%s'" % (eden_station)
                complete_station_query = '%s\n%s' % (station_query, station_where_statement)
                station_query_result = _query_mysql(host=DB_HOST, 
                                            user=DB_USER, 
                                            schema=DB_SCHEMA, 
                                            password=DB_PASSWORD, 
                                            query=complete_station_query)
                '''
                list_of_stations = []
                for station in eden_station:
                    station_name = station
                    cleaned_station_name = station_name.replace("+", "")
                    column_name = 'stg.stage_%s' % (cleaned_station_name)
                    list_of_stations.append(column_name)
                    
                stage_stations = ', '.join(list_of_stations)
                stage_select = "SELECT %s" % (stage_stations)
                stage_from = "FROM stage stg"
                stage_where = "WHERE stg.datetime >= '%s' AND stg.datetime < '%s'" % (time_start, time_end)
                complete_statement = "%s\n%s\%s" % (stage_select, stage_from, stage_where)
                
                
                stage_query_results = _query_mysql(host=DB_HOST, 
                                             password=DB_PASSWORD, 
                                             user=DB_USER, 
                                             schema=DB_SCHEMA, 
                                             query=complete_statement)
                
                
                _csv_dump(stage_query_results, 'static/data.csv')
                
                
                
                         
                if query_form.has_changed():
                    changed = True
                   
                else:
                    pass
                
                #dygraph_array = dygraph_array_creation(qs)
                
                return render (request, template_name, {'query_form': query_form,
                                                        'changed':changed,
                                                                  })
            
    else:
        query_form = TimeSeriesFilterForm()
    return render (request, template_name, {'query_form': query_form,})  
                