'''
Created on Mar 4, 2013

@author: rhayes
'''

from matplotlib.pyplot import savefig, figure, plot_date, legend, xticks, axes

import stage_data
import textwrap

_label_width = 12
def _clean_label(s):
    label = s.replace("stage_", "", 1)
    if len(label) > _label_width:
        label = label.replace("_", " ")
        label = textwrap.fill(label, width=_label_width)
    return label

def png(stations, destination, **kwargs):
    """
    Produce a PNG plot of the data series.
    destination can be any file-like object, or a string (file name)
    stations and kwargs are passed to stage_data.data
    """
    data = stage_data.data_for_plot(stations, **kwargs)
    keys = data.keys()

    # TODO Might prefer to build xList and yList by iteration rather than comprehension, to ease memory burden
    dataList = list(data)

    xList = [r[0] for r in dataList]
    yList = [r[1:] for r in dataList]

    figure()
    axes([0.1, 0.3, 0.5, 0.5])
    plot_date(xList, yList, '-')
    labels = [ _clean_label(s) for s in keys[1:] ]
    legend(labels, loc='upper left', bbox_to_anchor=(1, 1))
    xticks(rotation=60)

    savefig(destination, format="png")

    return len(xList)

if __name__ == "__main__":
    ct = png(['2A300', 'G-3567'], "/tmp/hg1.png", beginDate="2004-01-01", endDate="2010-01-01", maxCount=600)
    print "hg1.png", ct

    ct = png(['2A300', 'G-3567'], "/tmp/hg2.png", maxCount=600)
    print "hg2.png", ct

    ct = png(['2A300', 'G-3567'], "/tmp/hg3.png", beginDate="2004-01-01", endDate="2004-03-01", maxCount=600)
    print "hg3.png", ct

    ct = png(['L31NN', 'Chatham_River_near_the_Watson_Place'], "/tmp/hg4.png", beginDate="2011-09-01", endDate="2011-12-31", maxCount=600)
    print "hg4.png", ct


