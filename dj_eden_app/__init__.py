import os
from django.conf import settings

_mpl_work = settings.MATPLOTLIB_WORK_DIR

if not os.path.exists(_mpl_work):
    os.makedirs(_mpl_work)
# make a test file to ensure we can write a file to the dir
filename = os.path.join(_mpl_work, "trial.txt")
f = open(filename, "w")
f.write("hello")
f.close()
os.remove(filename)

os.environ['MPLCONFIGDIR'] = settings.MATPLOTLIB_WORK_DIR

