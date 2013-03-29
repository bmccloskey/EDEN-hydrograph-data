
class DataParams(object):

    stage = "stage"
    salinity = "salinity"
    rainfall = "rainfall"
    temperature = "temperature"

    def __iter__(self):
        return [self.rainfall, self.salinity, self.stage, self.temperature].__iter__()
