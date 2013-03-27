from sqlalchemy import Table
from sqlalchemy.sql import select
from stage_data import meta

coastal = Table('coastal', meta, autoload=True)

def coastal_column_name(gage_name, param):
    return gage_name + "_" + param

def has_coastal_data(gage_name, param):
    return coastal.columns.has_key(coastal_column_name(gage_name, param))

def coastal_seq(gage_name, param, **kwargs):
    q = coastal_query(gage_name, param, **kwargs)
    return q.execute()

def coastal_query(gage_name, param, beginDate=None, endDate=None):
    "Coastal data for the given gage and parameter."
    sel = select([coastal.c.datetime]).order_by(coastal.c.datetime)
    sel = sel.column(coastal.c[coastal_column_name(gage_name, param)])

    if beginDate is not None:
        sel = sel.where(coastal.c.datetime >= beginDate)
    if endDate is not None:
        sel = sel.where(coastal.c.datetime <= endDate)

    return sel
