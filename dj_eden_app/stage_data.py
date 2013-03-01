from sqlalchemy import *
from secure import DB_HOST, DB_PASSWORD, DB_SCHEMA, DB_USER
from sqlalchemy.sql import select

engine = create_engine("mysql://", \
                  connect_args={'host': DB_HOST, 'db': DB_SCHEMA, 'user':DB_USER, 'passwd':DB_PASSWORD})

def prepend(item, seq):
    yield item
    for i in seq:
        yield i

meta = MetaData(bind=engine)

stage = Table('stage', meta, autoload=True)

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

