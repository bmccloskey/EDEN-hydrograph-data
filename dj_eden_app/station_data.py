from flagged_data import daily_base_query, daily_columns, hourly_base_query, hourly_columns, date_col
# uses models.Station
import views.data_views as data_views

def daily_query(*stations):
    q = daily_base_query()

    for s in stations:
        gage_name = s.station_name_web
        navd88correction = s.stationdatum.convert_to_navd88_feet
        dry_value = s.dry_elevation

        flag, val, raw = daily_columns(gage_name, dry_value, navd88correction=navd88correction)

        q = q.column(val.label(gage_name + " avg"))
        q = q.column(flag.label(gage_name + " flag"))

    return q

def hourly_query(*stations):
    q = hourly_base_query()

    for s in stations:
        gage_name = s.station_name_web
        navd88correction = s.stationdatum.convert_to_navd88_feet
        dry_value = s.dry_elevation

        # use navd88 correction
        flag, val = hourly_columns(gage_name, dry_value, navd88correction=navd88correction)

        q = q.column(val.label(gage_name))
        q = q.column(flag.label(gage_name + " flag"))

    return q

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
    stations = data_views.station_list(gages)
    dt = date_col()

    print "hourly query"
    q = hourly_query(*stations)
    q = q.where(dt >= '2003-07-20')
    _show(q)

    print "daily query"
    q = daily_query(*stations)
    q = q.where(dt > '2003-06-28')
    _show(q)



