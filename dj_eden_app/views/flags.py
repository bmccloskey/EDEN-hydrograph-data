from sqlalchemy.sql import *


"Flag computation per Bryan McCloskey, USGS"

"""
The logic for flags displayed to the public for hourly data should be:
  if (flag=="M") "M"; elseif (stage < dry_elevation) "D"; elseif (flag==NULL) "O"; else "E"
(We should explicitly flag measured values "O" [observed] rather than just leave them NULL.)

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

def daily_flag(flag_col, stage_col, dry_elev):
    flag_expr = expression.case([
                                 (flag_col == None, 'O')
                                 ],
                                else_=flag_col)
    expr = expression.case([
                            (func.avg(stage_col) == None, 'M'),
                            (func.avg(stage_col) < dry_elev, 'D'),
                            ],
                           else_=func.max(flag_expr)
                           )
    return expr

# The M flag is redundant with null data

def hourly_flag(data_flag, stage, dry_elev):
    expr = expression.case([
                     (data_flag == 'M', 'M'),
                     (stage < dry_elev, 'D'),
                     (data_flag == None, 'O')],
                    else_='E')
    return expr


if __name__ == '__main__':
    from dj_eden_app.stage_data import stage
    dd = func.min(stage.c['datetime'])
    q = select([dd]).group_by(func.date(stage.c['datetime']))
    f = stage.c['flag_2A300']
    s = stage.c['stage_2A300']
    avg = func.avg(s)
    q = q.column(avg.label('2A300'))
    flag = daily_flag(f, s, 4.2)
    q = q.column(flag.label('2A300 flag'))

    print str(q)
