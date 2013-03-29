'''
Created on Mar 4, 2013

@author: rhayes
'''
import matplotlib
import django.conf
import os.path

matplotlib.use('Cairo')

from matplotlib.pyplot import savefig, figure, plot_date, xticks, axes, axhline, xlim, xlabel, ylabel, draw, grid
from matplotlib.lines import Line2D
try:
    import Image
except ImportError:
    from PIL import Image  # to deal with Windows...

import dj_eden_app.stage_queries as stage_queries
from dj_eden_app.colors import ColorRange
from dj_eden_app.gap_fill import gap_fill

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

def plot_multi(data, beginDate, endDate, show_logo=True):
    # data is an iterator over tuples.
    # each tuple has a timestamp as first column,
    # then 3 columns for each well: Observed, Estimated, Dry

    fig = figure()

    if show_logo:
        logo(fig)

    # axx = axes([0.1, 0.3, 0.5, 0.5])
    # left, bottom, width, height
    # ax1 = subplot(2, 1, 1)

    # left, bottom, width, height -- 0..1
    ax1 = axes([0.1, 0.3, 0.8, 0.55])
    fig.suptitle("Water level elevation above NAVD88 datum, in feet", y=0.9)

    xlabel('Date')
    ylabel('Water Level (NAVD88 ft)')
    if beginDate != None and endDate != None:
        xlim(xmin=beginDate, xmax=endDate)
    # axhline(y = 0.5) could be used for depicting ground elevation
    # labels = [ _clean_label(s) for s in keys[1:] ]
    # legend(labels, loc='upper left', bbox_to_anchor=(1, 1))
    xticks(rotation=90)

    labels = data.keys()
    # columns is a list of lists, one for each column.
    columns = [ list() for _l in labels]
    for r in data:
        for i, v in enumerate(r):
            columns[i].append(v)

    for i in range(1, len(columns), 3):
        gap_fill(columns[i], columns[i + 1], columns[i + 2])

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

    grid(color="0.7", linestyle="-")  # float-ish color is interpreted as gray level, 1.0=white


    h, l = ax1.get_legend_handles_labels()

    # position legend in lower sub-plot, not to graphed subplot
    # ax2 = subplot(2, 1, 2)
    fig.legend(h, l, loc='lower right', ncol=1 + (len(l) / 6))

    # make another legend for the dot'n'dashes, from the first 3 lines
    _legend_for_line_styles(fig)

    return len(columns[0]), fig

def logo(fig):
    filename = "usgs-logo.png"
    if not os.path.exists(filename):
        if django.conf.settings.SITE_HOME:
            filename = os.path.join(django.conf.settings.SITE_HOME, "dj_eden_app", filename)

    try:
        img = Image.open(filename)
    except IOError:
        # silly windows...
        logo_path = django.conf.settings.SITE_HOME.replace('\\', '/').replace('eden_project', 'dj_eden_app')
        filename_win = os.path.join(logo_path, "usgs-logo.png").replace('\\', '/')
        img = Image.open(filename_win)


    """
    # this did not help on windows
    try:
        img = Image.open(filename)
    except IOError:
        backslash_string = '\\'
        backslash_replace = '/'
        filename_windows = filename.replace(backslash_string, backslash_replace).replace('C:', '')
        img = Image.open(filename_windows)
    """
    height = img.size[1]

    bbox = fig.bbox
    bbox = bbox.anchored("NW")

    fig.figimage(img, 0, int(bbox.ymax) - height, zorder=None)


def _legend_for_line_styles(fig):
    fig.legend([Line2D([0, 1], [0, 1], color="black", linestyle=_line_styles[0][:-1], marker=_line_styles[0][-1:]),
                Line2D([0, 1], [0, 1], color="black", linestyle=_line_styles[1][:-1], marker=_line_styles[1][-1:]),
                Line2D([0, 1], [0, 1], color="black", linestyle=_line_styles[2][:-1], marker=_line_styles[2][-1:])],  # lines
        ('Observed', 'Estimated', 'Dry'),  # labels
        'lower left'  # anchor for positioning
        )

brown_ish = matplotlib.colors.colorConverter.to_rgba("brown", alpha=0.3)
gray_ish = matplotlib.colors.colorConverter.to_rgba("gray", alpha=0.3)

def plot_simple(data, beginDate=None, endDate=None, show_logo=True, title=None, y_label=None):
    "Plot a simple data series"
    f = figure()

    labels = data.keys()
    if not y_label:
        y_label = labels[1]

    if show_logo:
        logo(f)

    axes([0.1, 0.25, 0.8, 0.55])

    if title:
        f.suptitle(title, y=0.9)

    # left, bottom, width, height
    # ax1 = axes([0.1, 0.25, 0.8, 0.55])

    grid(color="0.7", linestyle="-")  # float-ish color is interpreted as gray level, 1.0=white

    xlabel('Date')
    if beginDate is not None:
        xlim(xmin=beginDate)
    if endDate is not None:
        xlim(xmax=endDate)
    xticks(rotation=90)

    ylabel(y_label)

    # TODO Consider using numpy arrays for better performance
    xx = []
    yy = []
    for t in data:
        xx.append(t[0])
        yy.append(t[1])

    plot_date(xx, yy, linestyle="-", marker=".", markersize=2.5)

    return f

def plot_single(data, beginDate=None, endDate=None, dry_elevation=None, ground_elevation=None, ngvd29_correction=None, show_logo=True):
    f = figure()

    labels = data.keys()

    if show_logo:
        logo(f)

    # left, bottom, width, height
    ax1 = axes([0.1, 0.25, 0.8, 0.55])

    f.suptitle("Water level elevation above NAVD88 datum, in feet\nGage " + labels[1], y=0.9)

    xlabel('Date')
    ylabel('Water Level (NAVD88 ft)')
    if beginDate != None and endDate != None:
        xlim(xmin=beginDate, xmax=endDate)
    # labels = [ _clean_label(s) for s in keys[1:] ]
    # legend(labels, loc='upper left', bbox_to_anchor=(1, 1))
    xticks(rotation=90)

    ylabel(labels[1] + "\nWater Level (NAVD88 ft)")

    # data has exactly 4 columns: date, O, E, D
    columns = [[], [], [], []]
    for r in data:
        for i, v in enumerate(r):
            columns[i].append(v)

    gap_fill(*columns[1:3])

    if dry_elevation is not None:
        axhline(y=dry_elevation, linewidth=4, color=gray_ish, zorder= -100)
    if ground_elevation is not None:
        axhline(y=ground_elevation, linewidth=4, color=brown_ish, zorder= -100)

    line_colors = ColorRange(count=1)
    c = line_colors[0]
    _logger.debug("In plot_single, color = %s", c)

    grid(color="0.7", linestyle="-")  # float-ish color is interpreted as gray level, 1.0=white

    markerprops = {'markerfacecolor':c, 'markersize':_marker_size, 'markeredgecolor':c}
    (l1,) = plot_date(columns[0], columns[1], _line_styles[0], color=c, label="Obs", **markerprops)
    (l2,) = plot_date(columns[0], columns[2], _line_styles[1], color=c, label="Est", **markerprops)
    (l3,) = plot_date(columns[0], columns[3], _line_styles[2], color=c, label="Dry", **markerprops)

    # Set options to make legend horizontal, across bottom
    h, l = ax1.get_legend_handles_labels()
    f.legend(h, l, loc='lower center', bbox_to_anchor=(0.5, 0.0), ncol=3)

    # logo(f)

    # _legend_for_line_styles(f, [l1, l2, l3])


    if ngvd29_correction is not None:
        ax1 = f.axes[0]
        ax2 = ax1.twinx()  # new axis overlay, ticks on right, shared x axis

        lim = ax1.get_ylim()
        ax2.set_ylim([d - ngvd29_correction for d in lim])
        ax2.set_ylabel("NAVD29 ft")

        # twinx does not preserve this, so restore it now
        ax2.xaxis_date()

        # tight_layout()
        draw()

    # tight_layout() # does not look good

    return len(columns[0]), f

def plot_grd_level(station):
    """
    Plots the ground level as a brown dashed-line if 
    the 'duration_elevation' column is not null for
    a station in STATION table.
    """
    grd_elevation = station.duration_elevation

    if grd_elevation:
        # color was #964B00
        grd_level = axhline(y=grd_elevation, linestyle='--', color=brown_ish)
    else:
        grd_level = None

    return grd_level

_line_style_dict = {
                'D': ":^",  # dotted with triangles
                'O': "-d",  # solid with diamonds
                'E': ":+",  # dotted with crosses
                'M': " ",  # blank
                }
_line_styles = ["-d", ":+", ":^"]

def line_style(flag):
    return _line_style_dict.get(flag) or "-"

def png_simple(data, outfile, **kwargs):
    fig = plot_simple(data, **kwargs)
    savefig(outfile, format="png", dpi=fig.dpi)

def png(data, outfile, **kwargs):
    if len(data) == 1:
        return png_single_station(data, outfile, **kwargs)
    else:
        return png_multi(data, outfile, **kwargs)

def png_multi(data, outfile, beginDate, endDate, show_logo=True):
    "Plot multiline onto outfile. Data has columns TIMESTAMP then O E D for each well."
    ct, fig = plot_multi(data, beginDate, endDate, show_logo)
    savefig(outfile, format="png", dpi=fig.dpi)

    return ct

def png_single_station(data, outfile, station=None, beginDate=None, endDate=None, show_logo=True):
    "Plot single-well data series. Data has columns WHEN, O, E, D."

    ct, fig = plot_single(data, beginDate=beginDate, endDate=endDate,
                     dry_elevation=station.dry_elevation,
                     ground_elevation=station.duration_elevation,
                     show_logo=show_logo,
                     ngvd29_correction=station.vertical_conversion)
    savefig(outfile, format="png", dpi=fig.dpi)

    return ct

if __name__ == "__main__":
    import dateutil.parser
    import sys

    default_show_logo = not 'windows' in sys.platform

    data, ss = stage_queries.data_for_plot_daily(['2A300', 'G-3567'], beginDate="2004-01-01", endDate="2010-01-01")
    ct = png_multi(data, "/tmp/hg1.png", dateutil.parser.parse("2004-01-01"), dateutil.parser.parse("2010-01-01"), show_logo=default_show_logo)
    print "hg1.png", ct

    data, ss = stage_queries.data_for_plot_daily(['2A300', 'G-3567'])
    ct = png_multi(data, "/tmp/hg2.png", None, None, show_logo=default_show_logo)
    print "hg2.png", ct

    data, ss = stage_queries.data_for_plot_hourly(['2A300', 'G-3567'], beginDate="2004-01-01", endDate="2004-03-01")
    ct = png_multi(data, "/tmp/hg3.png", dateutil.parser.parse("2004-01-01"), dateutil.parser.parse("2004-03-01"), show_logo=default_show_logo)
    print "hg3.png", ct

    data, ss = stage_queries.data_for_plot_daily(['L31NN', 'Chatham_River_near_the_Watson_Place'], beginDate="2011-09-01", endDate="2011-12-31")
    ct = png_multi(data, "/tmp/hg4.png", dateutil.parser.parse("2011-09-01"), dateutil.parser.parse("2011-12-31"), show_logo=False)
    print "hg4.png", ct

    data, ss = stage_queries.data_for_plot_daily(['2A300', 'G-3567', 'L31NN', "RG3", "ANGEL", "BARW4", "TSH"],
                                          beginDate="2006-10-15",
                                          endDate="2006-11-12")
    ct = png_multi(data, "/tmp/hg5.png", None, None)
    print "hg5.png", ct

    class Mock:
        def __init__(self, **attributes):
            self.__dict__ = attributes

    data, ss = stage_queries.data_for_plot_hourly(['CV5NR'], beginDate="2006-10-15", endDate="2006-11-12")
    station = ss[0]
    mock_station = Mock(dry_elevation=station.dry_elevation,
                        ground_elevation=station.duration_elevation,
                        ngvd29_correction=0.0,
                        duration_elevation=0.3,
                        vertical_conversion=0.0
                        )
    ct = png_single_station(data, "/tmp/hg6.png", mock_station,
                    beginDate=dateutil.parser.parse("2006-10-15"),
                    endDate=dateutil.parser.parse("2006-11-12"),
                    show_logo=default_show_logo)
    print "hg6.png", ct

    data, ss = stage_queries.data_for_plot_hourly(['CV5NR'], beginDate="2006-10-15", endDate="2006-11-12")
    station = ss[0]
    mock_station = Mock(dry_elevation=station.dry_elevation,
                    ground_elevation=station.duration_elevation,
                    ngvd29_correction=None,
                    duration_elevation=0.3,
                    vertical_conversion=None
                    )
    ct = png_single_station(data, "/tmp/hg6a.png", mock_station,
                    beginDate=dateutil.parser.parse("2006-10-15"),
                    endDate=dateutil.parser.parse("2006-11-12"),
                    show_logo=default_show_logo)
    print "hg6a.png", ct

    data, ss = stage_queries.data_for_plot_hourly(['CV5NR'], beginDate="2006-10-15", endDate="2006-11-12")
    station = ss[0]
    ct = png_single_station(data, "/tmp/hg6b.png", station,
                    beginDate=dateutil.parser.parse("2006-10-15"),
                    endDate=dateutil.parser.parse("2006-11-12"),
                    show_logo=False)
    print "hg6b.png", ct

