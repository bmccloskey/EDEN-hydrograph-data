'''
Created on Mar 4, 2013

@author: rhayes
'''


from matplotlib.figure import Figure
from matplotlib.pyplot import savefig, figure, plot_date, legend

import stage_data

def png(stations, destination, **kwargs):
    data = stage_data.data(stations, **kwargs)
    dataList = list(data)

    xList = [r[0] for r in dataList]
    yList = [r[1:] for r in dataList]

    # print len(dataList), len(xList), len(yList)

    # get the data set
    fig = figure()
    # ax = fig.add_subplot(111)
    plot_date(xList, yList, '-')
    legend(stations)
    # fig.autofmt_xdate()

    savefig(destination, format="png")

