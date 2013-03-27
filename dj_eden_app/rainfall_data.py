from sqlalchemy import Table
from sqlalchemy.sql import select, cast, label
from sqlalchemy.types import DateTime
from stage_data import meta

rainfall = Table('rainfall', meta, autoload=True)

def rainfall_column_name(gage_name):
    return 'rainfall_' + gage_name

def has_rainfall(gage_name):
    return rainfall.columns.has_key(rainfall_column_name(gage_name))

def rainfall_seq(gage_name, **kwargs):
    q = rainfall_query(gage_name, **kwargs)
    return q.execute()

def rainfall_query(gage_name, beginDate=None, endDate=None):
    "Rainfall data for the given gage. Timestamps are cast to DATETIME for ease of comparison"
    sel = select([cast(rainfall.c.date, DateTime).label("datetime")]).order_by(rainfall.c.date)
    sel = sel.column(rainfall.c[rainfall_column_name(gage_name)])

    if beginDate is not None:
        sel = sel.where(rainfall.c.date >= beginDate)
    if endDate is not None:
        sel = sel.where(rainfall.c.date <= endDate)

    return sel
