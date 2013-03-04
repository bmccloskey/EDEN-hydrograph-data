'''
Created on Mar 4, 2013

@author: rhayes
'''

from matplotlib.pyplot import savefig, figure, plot_date, legend

import stage_data

def png(stations, destination, **kwargs):
    """
    Produce a PNG plot of the data series.
    destination can be any file-like object, or a string (file name)
    stations and kwargs are passed to stage_data.data
    """
    data = stage_data.data(stations, **kwargs)

    # TODO Might prefer to build xList and yList by iteration rather than comprehension, to ease memory burden
    dataList = list(data)

    xList = [r[0] for r in dataList]
    yList = [r[1:] for r in dataList]

    figure()
    plot_date(xList, yList, '-')
    legend(stations)

    savefig(destination, format="png")

    return len(xList)

if __name__ == "__main__":
    ct = png(['stage_2A300', 'stage_G-3567'], "/tmp/hg1.png", beginDate="2004-01-01", endDate="2010-01-01")
    print "hg1.png", ct

    ct = png(['stage_2A300', 'stage_G-3567'], "/tmp/hg2.png")
    print "hg2.png", ct

    ct = png(['stage_2A300', 'stage_G-3567'], "/tmp/hg3.png", beginDate="2004-01-01", endDate="2004-03-01")
    print "hg3.png", ct

