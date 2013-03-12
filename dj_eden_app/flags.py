from sqlalchemy.sql import *
from sqlalchemy import String

"Flag computation per Bryan McCloskey, USGS"

"""
The logic for flags displayed to the public for hourly data should be:
  if (flag=="M") "M"; elseif (stage < dry_elevation) "D"; elseif (flag==NULL) "O"; else "E"
(We should explicitly flag measured values "O" [observed] rather than just leave them NULL.)
"""
# The M flag is redundant with null data
_M = literal_column("'M'", String)
_D = literal_column("'D'", String)
_O = literal_column("'O'", String)
_E = literal_column("'E'", String)

def hourly_data(flag_expr, value_expr, dry_elev):
    flag = expression.case([
                     ((flag_expr == _M) or (value_expr == None), _M),
                      (value_expr < dry_elev, _D),
                      (flag_expr == None, _O)],
                    else_=_E)
    return (flag, value_expr)


"""
The logic for flags displayed for daily means should be:
  if (length(flag=="M")==24) "M"; elseif (mean(stage) < dry_elevation) "D"; elseif (length(flag==NULL)>0) "O"; else "E"
I.e., if _all_ 24 hourly values are missing, flag "M"; if the daily mean is below the "goes dry" value, flag "D"; if _any_ of the daily values are measured, flag "O"; else flag as estimated ("E").
"""

# if any O then (if v < dry then D else O)
# if any E then (if v < dry then D else E)
# else (all M) M

# so (v == None) -> None
# (v < dry) -> D
# else max(flag)

# note that avg(all nulls) -> null

def daily_data(flag_expr, value_expr, dry_elev):
    flag_expr = expression.case([
                                 (flag_expr == None, _O)
                                 ],
                                else_=flag_expr)
    flag = expression.case([
                            (func.avg(value_expr) == None, _M),
                            (func.avg(value_expr) < dry_elev, _D),
                            ],
                           else_=func.max(flag_expr)
                           )
    return (flag, func.avg(value_expr))

def flag_col(g):
    return stage.c['flag_' + g]

def value_col(g):
    return stage.c['stage_' + g]

if __name__ == '__main__':
    from dj_eden_app.stage_data import stage
    gages = ['2A300', 'G-3567']

    dt = stage.c['datetime']

    # base query, raw values
    query_by_hour = select([dt])
    for g in gages:
        f = flag_col(g)
        s = value_col(g)
        (flag, val) = hourly_data(f, s, 4.2)
        query_by_hour = query_by_hour.column(val.label(g))
        query_by_hour = query_by_hour.column(flag.label(g + ' flag'))

    print "hourly"
    print str(query_by_hour)

    dm = func.min(dt)
    # base query, daily means
    query_by_day = select([dm]).group_by(func.date(dt))
    for g in gages:
        f = flag_col(g)
        s = value_col(g)
        (flag, val) = daily_data(f, s, 4.5)
        query_by_day = query_by_day.column(val.label(g + ' avg'))
        query_by_day = query_by_day.column(flag.label(g + ' flag'))
    # just to verify that we are really grouping
    query_by_day = query_by_day.column(func.count(dt).label("ct"))

    print "daily"
    print str(query_by_day)

    # does it really work?
    q = query_by_day.where(dt >= '2001-01-01')
    rs = q.execute()
    print "\t", rs.keys()
    vv = rs.fetchmany(30)
    for v in vv:
        print "\t", v


