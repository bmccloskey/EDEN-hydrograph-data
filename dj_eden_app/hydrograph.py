'''
Created on Mar 4, 2013

@author: rhayes
'''
import matplotlib
matplotlib.use('Cairo')

from matplotlib.pyplot import savefig, figure, plot_date, legend, xticks, axes, axhline, xlim

import textwrap

_label_width = 12

def _clean_label(s):
    label = s.replace("stage_", "", 1)
    if len(label) > _label_width:
        label = label.replace("_", " ")
        label = textwrap.fill(label, width=_label_width)
    return label

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
    plot_date(xList, yList, 'o', markersize=2.5)
    if beginDate != None and endDate != None:
        xlim(xmin=beginDate, xmax=endDate)
    # axhline(y = 0.5) could be used for depicting ground elevation
    labels = [ _clean_label(s) for s in keys[1:] ]
    legend(labels, loc='upper left', bbox_to_anchor=(1, 1))
    xticks(rotation=60)

    return len(xList)

_line_style_ = {
                'D': ":^",  # dotted with triangles
                'O': "-d",  # solid with diamonds
                'E': ":+",  # dotted with crosses
                'M': " ",  # blank
                }

def line_style(flag):
    return _line_style_.get(flag) or "-"

def png(data, destination, beginDate, endDate):

    ct = plot_many(data, destination, beginDate, endDate)
    savefig(destination, format="png")

    return ct

if __name__ == "__main__":
    import stage_data
    data = stage_data.data_for_plot(['2A300', 'G-3567'], beginDate="2004-01-01", endDate="2010-01-01", maxCount=600)
    ct = png(data, "/tmp/hg1.png")
    print "hg1.png", ct

    data = stage_data.data_for_plot(['2A300', 'G-3567'], maxCount=600)
    ct = png(data, "/tmp/hg2.png")
    print "hg2.png", ct

    data = stage_data.data_for_plot(['2A300', 'G-3567'], beginDate="2004-01-01", endDate="2004-03-01", maxCount=600)
    ct = png(data, "/tmp/hg3.png")
    print "hg3.png", ct

    data = stage_data.data_for_plot(['L31NN', 'Chatham_River_near_the_Watson_Place'], beginDate="2011-09-01", endDate="2011-12-31",
             maxCount=600)
    ct = png(data, "/tmp/hg4.png")
    print "hg4.png", ct



