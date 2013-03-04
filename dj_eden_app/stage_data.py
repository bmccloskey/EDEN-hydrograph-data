from sqlalchemy import *
from secure import DB_HOST, DB_PASSWORD, DB_SCHEMA, DB_USER
from sqlalchemy.sql import *

engine = create_engine("mysql://", \
                  connect_args={'host': DB_HOST, 'db': DB_SCHEMA, 'user':DB_USER, 'passwd':DB_PASSWORD})

def prepend(item, seq):
    yield item
    for i in seq:
        yield i

meta = MetaData(bind=engine)

stage = Table('stage', meta, autoload=True)

def data(stations, beginDate=None, endDate=None, maxCount=4000):
    columnNames = ['datetime']
    columnNames.extend(stations)

    selectColumns = [stage.c[cn] for cn in columnNames]

    clause = None
    if beginDate:
        clause = stage.c.datetime >= beginDate
    if endDate:
        clause = stage.c.datetime <= endDate
    if beginDate and endDate:
        clause = stage.c.datetime.between(beginDate, endDate)

    # TODO thin data set if count > maxCount

    s = select(selectColumns, clause)

    return engine.execute(s)

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
