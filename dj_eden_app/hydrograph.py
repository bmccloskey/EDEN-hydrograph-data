'''
Created on Mar 4, 2013

@author: rhayes
'''
import matplotlib
matplotlib.use('Cairo')

from matplotlib.pyplot import savefig, figure, plot_date, legend, xticks, axes, axhline, xlim, xlabel, ylabel, tight_layout, subplot, ylim
import dj_eden_app.data_queries as data_queries
from dj_eden_app.models import Station
from dj_eden_app.colors import ColorRange

import textwrap
import logging
_logger = logging.getLogger(__name__)

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

    fig = figure()
    # axx = axes([0.1, 0.3, 0.5, 0.5])
    # left, bottom, width, height
    ax1 = subplot(2, 1, 1)
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

    line_colors = ColorRange(count=(len(labels) - 1) / 3)

    _logger.debug("In plot_multi generation, colors = %s", list(line_colors))

    lines = []
    for i in range(1, len(labels)):
        marker = _line_styles[(i - 1) % 3]
        color = line_colors[(i - 1) / 3]
        label = "_nolegend_"
        if (i % 3) == 1:
            label = labels[i]
        markerprops = {'markerfacecolor':color, 'markersize':_marker_size, 'markeredgecolor':color}
        l = plot_date(columns[0], columns[i], fmt=marker, color=color, label=label, **markerprops)
        lines.append(l[0])

    h, l = ax1.get_legend_handles_labels()

    # position legend in lower sub-plot, not to graphed subplot
    # ax2 = subplot(2, 1, 2)
    fig.legend(h, l, loc='lower right', ncol=1 + (len(l) / 6))

    # make another legend for the dot'n'dashes, from the first 3 lines
    _legend_for_line_styles(fig, lines[0:3])

    return len(columns[0])

def _legend_for_line_styles(fig, lines):
    # make another legend for the dot'n'dashes, from the first 3 lines
    # TODO change the color to black by creating new, unattached instances of Line2D
    fig.legend(lines[0:3],
        ('Observed', 'Estimated', 'Dry'),
        'lower left')

brown_ish = matplotlib.colors.colorConverter.to_rgba("brown", alpha=0.3)
gray_ish = matplotlib.colors.colorConverter.to_rgba("gray", alpha=0.3)

def plot_single(data, beginDate=None, endDate=None, dry_elevation=None, ground_elevation=None, ngvd29_correction=None):
    f = figure()
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

    # data has exactly 5 columns: date, O, E, D, NGVD29 correction
    columns = [[], [], [], [], []]
    for r in data:
        for i, v in enumerate(r):
            columns[i].append(v)

    if dry_elevation is not None:
        axhline(y=dry_elevation, linewidth=4, color=gray_ish, zorder= -100)
    if ground_elevation is not None:
        axhline(y=ground_elevation, linewidth=4, color=brown_ish, zorder= -100)

    line_colors = ColorRange(count=1)
    c = line_colors[0]
    _logger.debug("In plot_single, color = %s", c)

    markerprops = {'markerfacecolor':c, 'markersize':_marker_size, 'markeredgecolor':c}
    (l1,) = plot_date(columns[0], columns[1], _line_styles[0], color=c, label="Obs", **markerprops)
    (l2,) = plot_date(columns[0], columns[2], _line_styles[1], color=c, label="Est", **markerprops)
    (l3,) = plot_date(columns[0], columns[3], _line_styles[2], color=c, label="Dry", **markerprops)

    legend()

    # _legend_for_line_styles(f, [l1, l2, l3])

    if ngvd29_correction is not None:
        axL = f.add_subplot(111)
        axL.yaxis.set_ticks_position("left")
        if beginDate != None and endDate != None:
            xlim(xmin=beginDate, xmax=endDate)
        axL_maj_ticks = axL.yaxis.get_majorticklocs()
        ylim(ymin=min(axL_maj_ticks), ymax=max(axL_maj_ticks))
        axR = f.add_subplot(111, sharex=axL, frameon=False)
        axR.axes.get_xaxis().set_visible(False)
        axR.yaxis.tick_right()
        axL_maj_ticks = axL.yaxis.get_majorticklocs()
        ylim(ymin=min(axL_maj_ticks) - ngvd29_correction, ymax=max(axL_maj_ticks) - ngvd29_correction)
        ylabel(labels[1] + "\nWater Level (NGVD29 ft)")
        axR.yaxis.set_label_position("right")
        tight_layout()

    return len(columns[0])

    pass

def plot_grd_level(site_list):
    """
    Plots the ground level as a brown dashed-line if 
    the 'duration_elevation' column is not null for
    a station in STATION table.
    """
    gage_elevation_qs = Station.objects.get(station_name_web__in=site_list)
    grd_elevation = gage_elevation_qs.duration_elevation

    if grd_elevation:
        # color was #964B00
        grd_level = axhline(y=grd_elevation, linestyle='--', color=brown_ish)
    else:
        grd_level = None

    return grd_level

def plot_many(data, destination, begin_date, end_date, gage_list):
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

    _logger.debug("using default colors in plot_many")
    figure()
    axes([0.1, 0.3, 0.5, 0.5])
    plot_date(xList, yList, '-d', markersize=2.5)
    xlabel('Date')
    ylabel('Water Level (NAVD88 ft)')
    if beginDate != None and endDate != None:
        xlim(xmin=beginDate, xmax=endDate)
    if len(gage_list) == 1:
        plot_grd_level(gage_list)
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

def line_style(flag):
    return _line_style_dict.get(flag) or "-"

def png(data, destination, beginDate, endDate, gage_list):

    ct = plot_many(data, destination, beginDate, endDate, gage_list)
    savefig(destination, format="png")

    return ct

def png_multi(data, outfile, beginDate, endDate):
    "Plot multiline onto outfile. Data has columns TIMESTAMP then O E D for each well."
    ct = plot_multi(data, beginDate, endDate)
    savefig(outfile, format="png")

    return ct

def png_single(data, outfile, beginDate=None, endDate=None, dry_elevation=None, ground_elevation=None, ngvd29_correction=None):
    "Plot single-well data series. Data has columns WHEN, O, E, D."

    ct = plot_single(data, beginDate=beginDate, endDate=endDate,
                     dry_elevation=dry_elevation,
                     ground_elevation=ground_elevation,
                     ngvd29_correction=ngvd29_correction)
    savefig(outfile, format="png")

    return ct

if __name__ == "__main__":
    import stage_data
    import dateutil.parser

    data, ss = data_queries.data_for_plot_daily(['2A300', 'G-3567', 'L31NN', "RG3", "ANGEL", "BARW4", "TSH"],
                                          beginDate="2006-10-15",
                                          endDate="2006-11-12")
    ct = png_multi(data, "/tmp/hg5.png", None, None)
    print "hg5.png", ct

    data, ss = data_queries.data_for_plot_hourly(['CV5NR'], beginDate="2006-10-15", endDate="2006-11-12")
    station = ss[0]
    ct = png_single(data, "/tmp/hg6.png",
                    beginDate=dateutil.parser.parse("2006-10-15"),
                    endDate=dateutil.parser.parse("2006-11-12"),
                    dry_elevation=station.dry_elevation, ground_elevation=station.duration_elevation)
    print "hg6.png", ct

    data, ss = data_queries.data_for_plot_daily(['2A300', 'G-3567'], beginDate="2004-01-01", endDate="2010-01-01")
    ct = png_multi(data, "/tmp/hg1.png", dateutil.parser.parse("2004-01-01"), dateutil.parser.parse("2010-01-01"))
    print "hg1.png", ct

    data, ss = data_queries.data_for_plot_daily(['2A300', 'G-3567'])
    ct = png_multi(data, "/tmp/hg2.png", None, None)
    print "hg2.png", ct

    data, ss = data_queries.data_for_plot_hourly(['2A300', 'G-3567'], beginDate="2004-01-01", endDate="2004-03-01")
    ct = png_multi(data, "/tmp/hg3.png", dateutil.parser.parse("2004-01-01"), dateutil.parser.parse("2004-03-01"))
    print "hg3.png", ct

    data, ss = data_queries.data_for_plot_daily(['L31NN', 'Chatham_River_near_the_Watson_Place'], beginDate="2011-09-01", endDate="2011-12-31")
    ct = png_multi(data, "/tmp/hg4.png", dateutil.parser.parse("2011-09-01"), dateutil.parser.parse("2011-12-31"))
    print "hg4.png", ct
