from sqlalchemy import *
from secure import DB_HOST, DB_PASSWORD, DB_SCHEMA, DB_USER
from sqlalchemy.sql import *
from sqlalchemy.sql.functions import GenericFunction
from seq import prepend
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
        offset = station.stationdatum.convert_to_navd88_feet
        # use corrected data unless data is null
        data_corrected = func.if_(data_col == None, None, data_col + offset).label("stage_" + gage)
    else:
        data_corrected = data_col

    return (data_col, flag_col, data_corrected)

def _query_for_plot(stations, beginDate=None, endDate=None, maxCount=None, station_dict={}):
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

def write_csv(results, outfile):
    '''
    Writes a csv file to the specified outfile file-like object.
    '''

    csv_writer = csv.writer(outfile)
    csv_writer.writerow(results.keys())
    # Iterate, because csv.writerows pulls up all rows to a list
    for r in results:
        csv_writer.writerow(r)


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

