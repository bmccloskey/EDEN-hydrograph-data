from sqlalchemy import *
from secure import DB_HOST, DB_PASSWORD, DB_SCHEMA, DB_USER
from sqlalchemy.sql import *
from sqlalchemy.sql.functions import GenericFunction, min, max
from seq import prepend
from dj_eden_app.gap_fill import gap_fill_by_3

import csv

engine = create_engine("mysql://", \
                  connect_args={'host': DB_HOST, 'db': DB_SCHEMA, 'user':DB_USER, 'passwd':DB_PASSWORD})

meta = MetaData(bind=engine)

stage = Table('stage', meta, autoload=True)
# station = Table('station', meta, autoload = True)
# station_datum = Table('station_datum', meta, autoload = True)
# stat_datum_vw = Table('stat_datum_vw', meta, autoload = True)

class IfFunc(GenericFunction):
    name = "if"
    identifier = "if_"

def data_for_plot(stations, **kwargs):
    """
    Produces an iterable intended for Dygraphs.
    First column will be observation times, as datetime.datetime instances.
    Every gage in the stations list will produce two columns: one for the verified observations, named with the gage name,
    the second, for estimated observations, labelled as "$GAGE_NAME est". It may be expected that there will be many None
    observations in each data series -- in fact, the estimated column may be entirely None (but it will never be absent).
    """
    q = _query_for_plot(stations, **kwargs)
    return q.execute()

def data_for_download(stations, **kwargs):
    """
    Produces an iterable intended for download.
    First column will be observation times, as datetime.datetime instances.
    Every gage in the stations list will produce two columns: one for the verified observations, named like stage_GAGENAME,
    another for the flag, flag_GAGENAME.
    """
    q = _query_for_download(stations, **kwargs)
    return q.execute()

def _columns(gage, station):
    data_col = stage.c["stage_" + gage]
    flag_col = stage.c["flag_" + gage]

    if station:
        offset = station.convert_to_navd88_feet
        # use corrected data unless data is null
        data_corrected = func.if_(data_col == None, None, data_col + offset).label("stage_" + gage)
    else:
        data_corrected = data_col

    return (data_col, flag_col, data_corrected)

def _query_for_plot(stations, beginDate=None, endDate=None, maxCount=None, station_dict={}):
    # TODO Use queries from data_queries, separating daily and hourly
    sel = select([stage.c.datetime]).order_by(stage.c.datetime)

    # make the world safe for simple calls like _query_for_plot("2A300")
    if isinstance(stations, basestring):
        stations = [stations]

    for gage in stations:
        station = station_dict.get(gage)

        (data_col, flag_col, data_corrected) = _columns(gage, station)

        sel = sel.column(func.if_(flag_col == None,
                                  data_corrected,
                                  None).label(gage))
        sel = sel.column(func.if_(flag_col != None,
                                  data_corrected,
                                  None).label(gage + " est"))

    if beginDate is not None:
        sel = sel.where(stage.c.datetime >= beginDate)
    if endDate is not None:
        sel = sel.where(stage.c.datetime <= endDate)

    # thin the data if there are too many points
    countQuery = sel.alias("forCount").count()
    count = countQuery.execute().scalar()
    if maxCount and count > maxCount:
        sel = sel.where(func.hour(stage.c.datetime) == 0)

    return sel

def _query_for_download(stations, beginDate=None, endDate=None, station_dict={}):
    sel = select([stage.c.datetime]).order_by(stage.c.datetime)

    # make the world safe for simple calls like _query_for_plot("2A300")
    if isinstance(stations, basestring):
        stations = [stations]

    for gage in stations:
        station = station_dict.get(gage)

        (data_col, flag_col, data_corrected) = _columns(gage, station)

        sel = sel.column(data_corrected)
        sel = sel.column(flag_col)

    if beginDate is not None:
        sel = sel.where(stage.c.datetime >= beginDate)
    if endDate is not None:
        sel = sel.where(stage.c.datetime <= endDate)

    return sel

def _infer_rdb_types(resultset):
    '''
    Infer the RDB type codes for a row, from a DB API Cursor
    See http://www.python.org/dev/peps/pep-0249/#cursor-objects
    '''
    desc = resultset.cursor.description
    dialect = resultset.dialect.dbapi
    value = []
    # RDB type row like 5s,10n,12s...
    # s for string
    # n for number
    # d for date
    for d in desc:
        (name, type_code, display_size, internal_size, precision, scale, null_ok) = d
        if type_code == dialect.DATETIME or type_code == dialect.DATE:
            value.append("%dd" % (display_size))
        elif type_code == dialect.NUMBER or 246 == type_code:  # HACK for MySQL
            value.append("%dn" % (display_size))
        else:
            value.append("%ds" % (display_size))

    return value

def write_rdb(results, outfile, metadata=[]):
    '''
    Write an NWIS RDB to outfile.
    RDB is like csv with a header, see http://help.waterdata.usgs.gov/faq/automated-retrievals#MR
    or http://waterdata.usgs.gov/nwis?tab_delimited_format_info
    '''
    # write the metadata before the CSV body -- no escaping
    for r in metadata:
        outfile.write("# " + r + "\r\n")
    csv_writer = csv.writer(outfile, dialect='excel-tab', lineterminator='\r\n')
    csv_writer.writerow(results.keys())

    if hasattr(results, 'cursor') and hasattr(results, 'dialect'):
        type_codes = _infer_rdb_types(results)
    else:
        # totally fake
        type_codes = len(results.keys()) * ["12s"]
    csv_writer.writerow(type_codes)

    # TODO write RDB type row like 5s,10n,12s...
    # s for string
    # n for number
    # d for date

    # Iterate, because csv.writerows pulls up all rows to a list
    for r in results:
        csv_writer.writerow(r)

def add_column_to_csv(column_name, csvfile):
    open_csv = open(csvfile)
    csv_reader = csv.reader(open_csv)
    row_count = len(list(csv_reader))
    
    return row_count

def write_csv_for_plot(results, outfile, metadata=None, column_name=None):
    '''
    Writes a csv file to the specified outfile file-like object.
    Tweak the data to fill in gaps
    '''

    csv_writer = csv.writer(outfile)
    if metadata != None:
        csv_writer.writerow(metadata)
    result_keys = results.keys()
    if column_name != None:
        result_keys.append(column_name)
    csv_writer.writerow(results.keys())
    # Iterate, because csv.writerows pulls up all rows to a list
    for r in gap_fill_by_3(results):
        if column_name == None:
            csv_writer.writerow(r)
        else:
            r_list = list(r)
            r_list.append(None)
            csv_writer.writerow(r_list)

"""
def write_csv(results, outfile, metadata=None, station_name=None):
    '''
    Writes a csv file to the specified outfile file-like object.
    '''

    csv_writer = csv.writer(outfile)
    if metadata != None:
        csv_writer.writerow(metadata)
    result_keys = results.keys()
    if station_name != None:
        ngvd29_name = '%s_NGVD29' % station_name
        result_keys.append(ngvd29_name)
    csv_writer.writerow(result_keys)
    # Iterate, because csv.writerows pulls up all rows to a list
    for r in results:
        if station_name != None:
            r2 = list(r) # cannot append to a result proxy
            r2.append(None)
            csv_writer.writerow(r2)
        else:
            csv_writer.writerow(r)
"""

if __name__ == "__main__":

    gages = ['G-3567', '2A300', 'L31NN', 'Chatham_River_near_the_Watson_Place']

    d4p = data_for_plot(gages, beginDate="2010-01-01", endDate="2010-03-01", maxCount=800)
    print d4p.keys()
    assert len(d4p.keys()) == 1 + 2 * len(gages)
    for row in d4p.fetchmany(4):
        print row
        assert row.datetime is not None
    d4p.close()

    subgages = gages[0:2]
    d4d = data_for_download(subgages, beginDate="2010-01-01", endDate="2010-03-01")
    print d4d.keys()
    assert len(d4d.keys()) == 1 + 2 * len(subgages)
    for row in d4d.fetchmany(4):
        print row
        assert "flag_" + gages[0] in row
    d4d.close()

