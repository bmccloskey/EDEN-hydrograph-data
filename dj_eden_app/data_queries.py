from flagged_data import daily_base_query, daily_columns, hourly_base_query, hourly_columns, date_col
# uses models.Station
from sqlalchemy.sql import expression
from collections import OrderedDict

from dj_eden_app.models import Station


def station_dict(gages):
    # pull station name list up to Station objects
    stations = Station.objects.filter(station_name_web__in=gages)
    # and make a dictionary mapping names back to stations
    _dict = dict((s.station_name_web, s) for s in stations)
    # and then map back to the original order (duplicates removed)
    # ordering will be the natural ordering for the Station model, not the input order
    station_dict = OrderedDict((name, _dict[name]) for name in gages)

    return station_dict

def station_list(gages):
    sd = station_dict(gages)
    return sd.values()

def get_ngvd29_conversion(station_object):
    
    conversion = station_object.vertical_conversion
    if conversion is None or conversion == '':
        ngvd29_conv = 0
    else:
        ngvd29_conv = conversion
        
    return ngvd29_conv

def daily_query(*stations):
    q, dt = daily_base_query()

    for s in stations:
        gage_name = s.station_name_web
        navd88correction = s.convert_to_navd88_feet
        dry_value = s.dry_elevation
        
        flag, val, _raw = daily_columns(gage_name, dry_value, navd88correction=navd88correction)

        q = q.column(val.label(gage_name + " avg"))
        q = q.column(flag.label(gage_name + " flag"))

    return q, dt

def daily_query_split(*stations):
    q, dt = daily_base_query()

    for s in stations:
        gage_name = s.station_name_web
        navd88correction = s.convert_to_navd88_feet
        dry_value = s.dry_elevation

        flag, val, _raw = daily_columns(gage_name, dry_value, navd88correction=navd88correction)

        # split to 3 columns: Observed, Estimated, Dry. Missing is just missing.
        q = q.column(expression.case(value=flag,
                                     whens={'O': val},
                                     else_=None).label(gage_name + " avg"))
        q = q.column(expression.case(value=flag,
                                     whens={'E': val},
                                     else_=None).label(gage_name + " est"))
        q = q.column(expression.case(value=flag,
                                     whens={'D': val},
                                     else_=None).label(gage_name + " dry"))
        if len(stations) == 1:
            # create a series with NGVD29 data for dygraphs
            ngvd29correction = get_ngvd29_conversion(s)
            q = q.column((val - ngvd29correction).label(gage_name + "_NGVD29"))

    return q, dt

def hourly_query(*stations):
    q, dt = hourly_base_query()

    for s in stations:
        gage_name = s.station_name_web
        navd88correction = s.convert_to_navd88_feet
        dry_value = s.dry_elevation

        # use navd88 correction
        flag, val = hourly_columns(gage_name, dry_value, navd88correction=navd88correction)

        q = q.column(val.label(gage_name))
        q = q.column(flag.label(gage_name + " flag"))
    
    return q, dt

def hourly_query_split(*stations):
    q, dt = hourly_base_query()

    for s in stations:
        gage_name = s.station_name_web
        navd88correction = s.convert_to_navd88_feet
        dry_value = s.dry_elevation

        flag, val = hourly_columns(gage_name, dry_value, navd88correction=navd88correction)

        # split to 3 columns: Observed, Estimated, Dry. Missing is just missing.
        q = q.column(expression.case(value=flag,
                                     whens={'O': val},
                                     else_=None).label(gage_name))
        q = q.column(expression.case(value=flag,
                                     whens={'E': val},
                                     else_=None).label(gage_name + " est"))
        q = q.column(expression.case(value=flag,
                                     whens={'D': val},
                                     else_=None).label(gage_name + " dry"))
        if len(stations) == 1:
            # create a series with NGVD29 data for dygraphs
            ngvd29correction = get_ngvd29_conversion(s)
            q = q.column((val - ngvd29correction).label(gage_name + "_NGVD29"))
    return q, dt

def data_for_plot_daily(stations, beginDate=None, endDate=None):
    sl = station_list(stations)
    q, dt = daily_query_split(*sl)
    if beginDate is not None:
        q = q.where(dt >= beginDate)
    if endDate is not None:
        q = q.where(dt <= endDate)
    data = q.execute()
    return data, sl

def data_for_plot_hourly(stations, beginDate=None, endDate=None):
    sl = station_list(stations)
    q, dt = hourly_query_split(*sl)
    if beginDate is not None:
        q = q.where(dt >= beginDate)
    if endDate is not None:
        q = q.where(dt <= endDate)
    data = q.execute()
    return data, sl


if __name__ == '__main__':
    def _show(q):
        "Exercise a query"
        print "-query"
        print str(q)

        rs = q.execute()
        print "-results"
        print "\t", rs.keys()
        vv = rs.fetchmany(30)
        for v in vv:
            print "\t", v
        print


    gages = ['G-3567', '2A300']
    stations = station_list(gages)
    # dt = date_col()

    print "hourly query"
    q, dt = hourly_query(*stations)
    q = q.where(dt >= '2003-07-20')
    _show(q)

    print "daily query"
    q, dt = daily_query(*stations)
    q = q.where(dt >= '2003-06-28')
    _show(q)

    print "hourly query split"
    q, dt = hourly_query_split(*stations)
    q = q.where(dt >= '2003-07-20')
    _show(q)

    print "daily query_split"
    q, dt = daily_query_split(*stations)
    q = q.where(dt >= '2003-06-28')
    _show(q)


