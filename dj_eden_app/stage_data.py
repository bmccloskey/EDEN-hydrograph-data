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

    rs = engine.execute(s)

    for r in rs:
        print r
    print

    print "**raw query"
    rs = engine.execute("select datetime, stage_2A300 from stage where datetime between '2002-01-01' and '2002-01-02'")
    for i in prepend(["datetime", "2A300"], rs):
        print ",".join(map(str, i))
    print

    print "**raw query formatted by comprehension"
    rs = engine.execute("select datetime, stage_2A300 from stage where datetime between '2002-01-02' and '2002-01-03'")
    for i in prepend(["datetime", "2A300"], rs):
        print ",".join(['"%s"' % x for x in i])

