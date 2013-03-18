import matplotlib.cm  as cm
from matplotlib.colors import rgb2hex as rgb2hex

class ColorRange:
    _color_map_name = None
    cmap = None
    color_list = []

    def __init__(self, color_map=None, count=None):
        self.cmap = cm.get_cmap(color_map, count)
        self.color_list = [ rgb2hex(self.cmap(c)) for c in range(count)]

    def __len__(self):
        return len(self.color_list)

    def __getitem__(self, n):
        return self.color_list[n]

    def __iter__(self):
        return self.color_list.__iter__()

    def name(self):
        return self.cmap.name
