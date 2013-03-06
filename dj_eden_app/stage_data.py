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

def _query_for_plot(stations, beginDate=None, endDate=None, maxCount=None, navd88Offset={}):
    sel = select([stage.c.datetime])

    for gage in stations:
        stage_name = "stage_" + gage
        flag_name = "flag_" + gage
        offset = navd88Offset.get(gage) or 0
        sel = sel.column(func.if_(stage.c[flag_name] == None,
                                  func.if_(stage.c[stage_name] == None, None, offset + stage.c[stage_name]),
                                  None).label(gage))
        sel = sel.column(func.if_(stage.c[flag_name] != None,
                                  func.if_(stage.c[stage_name] == None, None, offset + stage.c[stage_name]),
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

def _query_for_download(stations, beginDate=None, endDate=None, navd88Offset={}):
    sel = select([stage.c.datetime])

    for gage in stations:
        stage_name = "stage_" + gage
        flag_name = "flag_" + gage
        offset = navd88Offset.get(gage) or 0
        sel = sel.column(func.if_(stage.c[stage_name] == None, None, offset + stage.c[stage_name]).label(stage_name))
        sel = sel.column(stage.c[flag_name])

    if beginDate is not None:
        sel = sel.where(stage.c.datetime >= beginDate)
    if endDate is not None:
        sel = sel.where(stage.c.datetime <= endDate)

    return sel

def write_csv(header, results, outfile_path):
    '''
    Writes a csv file to the specified outfile_path.
    This file is not ammenable for user download.
    '''

    csv_file = open(outfile_path, 'wb')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(header)
    csv_writer.writerows(results)
    csv_file.close()

def downloadable_csv(header, results, output):
    '''
    Creates a csv file in an HTTP response
    for use download.
    '''

    csv_writer = csv.writer(output)
    csv_writer.writerow(header)
    csv_writer.writerows(results)


def create_query_and_colnames(columnNames, start_date, end_date, outpath, csv_download=False):
    """
    Takes a list of column names, start/end date,
    output path, and returns the MySQL query results.
    A downloadable csv will be generated if
    csv_download is set as True (default is False).
    """
    selectColumns = [stage.c[cn] for cn in columnNames]

    s = select(selectColumns, \
               stage.c.datetime.between(start_date, end_date))

    # generators can only be used once... there are separate generators for the headers and results
    header_gen = engine.execute(s)
    result_gen = engine.execute(s)

    header_key = header_gen._metadata.keys
    all_results = result_gen.fetchall()

    if csv_download == True:
        downloadable_csv(header=header_key,
                         results=all_results,
                         output=outpath)

    else:
        write_csv(header=header_key,
                  results=all_results,
                  outfile_path=outpath)

    return "Hooray, the data has been written to a csv!"

def example_data_set():
    columnNames = ['datetime', 'stage_G-3567', 'stage_2A300']
    selectColumns = [stage.c[cn] for cn in columnNames]
    s = select(selectColumns, \
               stage.c.datetime.between('2008-03-01', '2008-03-02'))
    return s

if __name__ == "__main__":

    columnNames = ['datetime', 'stage_G-3567', 'stage_2A300']
    selectColumns = [stage.c[cn] for cn in columnNames]

    print "**alchemical query"
    s = select(selectColumns, \
               stage.c.datetime.between('2008-03-01', '2008-03-02'))
    print s

    print "*results"
    rs = engine.execute(s)
    try:
        for r in prepend(columnNames, rs):
            print ",".join(map(str, r))
    finally:
        rs.close()

    print

