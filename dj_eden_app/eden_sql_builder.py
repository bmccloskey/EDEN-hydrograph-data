from sqlalchemy import *
from secure import DB_HOST, DB_PASSWORD, DB_SCHEMA, DB_USER
import csv

engine = create_engine("mysql://", \
                  connect_args={'host': DB_HOST, 'db': DB_SCHEMA, 'user':DB_USER, 'passwd':DB_PASSWORD})

def prepend(item, seq):
    yield item
    for i in seq:
        yield i
        
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
        

meta = MetaData(bind=engine)

stage = Table('stage', meta, autoload=True)

def create_query_and_colnames(columnNames, start_date, end_date, outpath, csv_download = False):
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
        downloadable_csv(header = header_key, 
                         results = all_results, 
                         output = outpath)
        
    else:
        write_csv(header = header_key, 
                  results = all_results, 
                  outfile_path = outpath)
    
    return "Hooray, the data has been written to a csv!"