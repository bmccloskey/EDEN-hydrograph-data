'''
Created on Mar 4, 2013

@author: rhayes
'''
import matplotlib
matplotlib.use('Cairo')

from matplotlib.pyplot import savefig, figure, plot_date, legend, xticks, axes, axhline, xlim, xlabel, ylabel
import dj_eden_app.data_queries as data_queries

import textwrap

_label_width = 12
_marker_size = 2.5

def _clean_label(s):
    label = s.replace("stage_", "", 1)
    if len(label) > _label_width:
        label = label.replace("_", " ")
        label = textwrap.fill(label, width=_label_width)
    return label

def plot_multi(data, beginDate, endDate):
    # data is an iterator over tuples.
    # each tuple has a timestamp as first column,
    # then 3 columns for each well: Observed, Estimated, Dry

    figure()
    axes([0.1, 0.3, 0.5, 0.5])
    xlabel('Date')
    ylabel('Water Level (NAVD88 ft)')
    if beginDate != None and endDate != None:
        xlim(xmin=beginDate, xmax=endDate)
    # axhline(y = 0.5) could be used for depicting ground elevation
    # labels = [ _clean_label(s) for s in keys[1:] ]
    # legend(labels, loc='upper left', bbox_to_anchor=(1, 1))
    xticks(rotation=60)

    labels = data.keys()
    # columns is a list of lists, one for each column.
    columns = [ list() for _l in labels]
    for r in data:
        for i, v in enumerate(r):
            columns[i].append(v)

    for i in range(1, len(labels)):
        marker = _line_styles[(i - 1) % 3]
        color = _line_colors[((i - 1) / 3) % len(_line_colors)]
        label = "_nolegend_"
        if (i % 3) == 1:
            label = labels[i]
        markerprops = {'markerfacecolor':color, 'markersize':_marker_size, 'markeredgecolor':color}
        plot_date(columns[0], columns[i], fmt=marker, color=color, label=label, **markerprops)

    legend(loc='upper left', bbox_to_anchor=(1, 1))

    return len(columns[0])


def plot_single(data, beginDate=None, endDate=None, dry_elevation=None, ground_elevation=None):
    figure()
    # axes([0.1, 0.3, 0.5, 0.5])
    xlabel('Date')
    ylabel('Water Level (NAVD88 ft)')
    if beginDate != None and endDate != None:
        xlim(xmin=beginDate, xmax=endDate)
    # labels = [ _clean_label(s) for s in keys[1:] ]
    # legend(labels, loc='upper left', bbox_to_anchor=(1, 1))
    xticks(rotation=60)

    labels = data.keys()
    ylabel(labels[1] + "\nWater Level (NAVD88 ft)")

    # data has exactly 4 columns: date, O, E, D
    columns = [[], [], [], []]
    for r in data:
        for i, v in enumerate(r):
            columns[i].append(v)

    if dry_elevation is not None:
        axhline(y=dry_elevation, linewidth=4, color="gray", zorder= -100)
    if ground_elevation is not None:
        axhline(y=ground_elevation, linewidth=4, color="brown", zorder= -100)
    c = _line_colors[0]
    markerprops = {'markerfacecolor':c, 'markersize':_marker_size, 'markeredgecolor':c}
    plot_date(columns[0], columns[1], _line_styles[0], color=c, label="Obs", **markerprops)
    plot_date(columns[0], columns[2], _line_styles[1], color=c, label="Est", **markerprops)
    plot_date(columns[0], columns[3], _line_styles[2], color=c, label="Dry", **markerprops)

    legend()

    return len(columns[0])

    pass

def plot_many(data, destination, begin_date, end_date):
    """
    Produce a PNG plot of the data series.
    destination can be any file-like object, or a string (file name)
    stations and kwargs are passed to stage_data.data
    """
    keys = data.keys()
    beginDate = begin_date
    endDate = end_date

    # Prefer to build xList and yList by iteration rather than comprehension, to ease memory burden
    xList = []
    yList = []

    for row in data:
        xList.append(row[0])
        yList.append(row[1:])

    # could collapse some of the data ranges, perhaps

    figure()
    axes([0.1, 0.3, 0.5, 0.5])
    plot_date(xList, yList, '-d', markersize=2.5)
    xlabel('Date')
    ylabel('Water Level (NAVD88 ft)')
    if beginDate != None and endDate != None:
        xlim(xmin=beginDate, xmax=endDate)
    # axhline(y = 0.5) could be used for depicting ground elevation
    labels = [ _clean_label(s) for s in keys[1:] ]
    legend(labels, loc='upper left', bbox_to_anchor=(1, 1))
    xticks(rotation=60)

    return len(xList)

_line_style_dict = {
                'D': ":^",  # dotted with triangles
                'O': "-d",  # solid with diamonds
                'E': ":+",  # dotted with crosses
                'M': " ",  # blank
                }
_line_styles = ["-d", ":+", ":^"]
_line_colors = [
"#000000",
"#670075",
"#830094",
"#3800a3",
"#0000c1",
"#0025dd",
"#007ddd",
"#009adb",
"#00aaab",
"#00aa8d",
"#009e28",
"#00ac00",
"#00ca00",
"#00e700",
"#1dff00",
"#bcff00",
"#ecef00",
"#fcd200",
"#ffa900",
"#ff4500",
"#f10000",
"#d80000",
"#cc1c1c",
"#cccccc",
]

def line_style(flag):
    return _line_style_dict.get(flag) or "-"

def png(data, destination, beginDate, endDate):

    ct = plot_many(data, destination, beginDate, endDate)
    savefig(destination, format="png")

    return ct

def png_multi(data, outfile, beginDate, endDate):
    "Plot multiline onto outfile. Data has columns WHEN then O E D for each well."
    ct = plot_multi(data, beginDate, endDate)
    savefig(outfile, format="png")

    return ct

def png_single(data, outfile, beginDate=None, endDate=None, dry_elevation=None, ground_elevation=None):
    "Plot single-well data series. Data has columns WHEN, O, E, D."

    ct = plot_single(data, beginDate=beginDate, endDate=endDate, dry_elevation=dry_elevation, ground_elevation=ground_elevation)
    savefig(outfile, format="png")

    return ct

if __name__ == "__main__":
    import stage_data
    import dateutil.parser

    station_dict = data_queries.station_dict(['2A300', 'G-3567', 'L31NN', "RG3", "ANGEL", "BARW4", "TSH"])
    q, dt = data_queries.daily_query_split(*station_dict.values())
    q = q.where(dt >= "2006-10-15")
    q = q.where(dt <= "2006-11-12")
    data = q.execute()
    ct = png_multi(data, "/tmp/hg5.png", None, None)
    print "hg5.png", ct

    station_dict = data_queries.station_dict(['CV5NR'])
    station = station_dict.values()[0]
    q, dt = data_queries.daily_query_split(*station_dict.values())
    q = q.where(dt >= "2006-10-15")
    q = q.where(dt <= "2006-11-12")
    data = q.execute()
    ct = png_single(data, "/tmp/hg6.png", beginDate=dateutil.parser.parse("2006-10-15"),
                    endDate=dateutil.parser.parse("2006-11-12"),
                    dry_elevation=station.dry_elevation, ground_elevation=station.duration_elevation)
    print "hg6.png", ct

    data = stage_data.data_for_plot(['2A300', 'G-3567'], beginDate="2004-01-01", endDate="2010-01-01", maxCount=600)
    ct = png(data, "/tmp/hg1.png", dateutil.parser.parse("2004-01-01"), dateutil.parser.parse("2010-01-01"))
    print "hg1.png", ct

    data = stage_data.data_for_plot(['2A300', 'G-3567'], maxCount=600)
    ct = png(data, "/tmp/hg2.png", None, None)
    print "hg2.png", ct

    data = stage_data.data_for_plot(['2A300', 'G-3567'], beginDate="2004-01-01", endDate="2004-03-01", maxCount=600)
    ct = png(data, "/tmp/hg3.png", dateutil.parser.parse("2004-01-01"), dateutil.parser.parse("2004-03-01"))
    print "hg3.png", ct

    data = stage_data.data_for_plot(['L31NN', 'Chatham_River_near_the_Watson_Place'], beginDate="2011-09-01", endDate="2011-12-31",
             maxCount=600)
    ct = png(data, "/tmp/hg4.png", dateutil.parser.parse("2011-09-01"), dateutil.parser.parse("2011-12-31"))
    print "hg4.png", ct


