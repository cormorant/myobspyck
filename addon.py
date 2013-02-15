# -*- coding: utf-8 -*-
import os
import sys
import datetime

import PyQt4
import numpy as np
import matplotlib as mpl
from matplotlib.colors import ColorConverter
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as QFigureCanvas
from matplotlib.widgets import MultiCursor as MplMultiCursor

mpl.rc('figure.subplot', left=0.05, right=0.98, bottom=0.10, top=0.92,
       hspace=0.28)
mpl.rcParams['font.size'] = 10


try:
    import psycopg2
except ImportError:
    print("No psycopg2 package. Database postgresql unavailable.")

from obspy.core import UTCDateTime, Trace, Stream
#from obspy.core import read

from baikal import BaikalFile, get_time


COMMANDLINE_OPTIONS = (
    #(('-V', '--version'), {
    #    'action': 'version', 
    #    'version'='%(prog)s.' + __version__,
    #}),
    # основная масса переданных аргументов
    (("arguments",), {
        "nargs": "*",
        'help': "Specify arguments to process",
    }),
    # загрузка папки (?)
    (("-d", "--dir"), {
        "action": "store_true", 'default': False,
        'dest': "directory",
        'help': "Directory in seisobr where to find seismogramms"
    }),
    # загрузка (поиск) файла
    (("-f", "--fromfile"), {
        "action": "store_true", 'default': False,
        'dest': "fromfile",
        'help': "Load information about data to load from file:"
    }),
    # поиск по коду idDir
    (("-I", "--iddir"), {
        "action": "store_true", 'default': False,
        'help': "Search files by query in database by idDir"
    }),
    # поиск по времени
    (("-t", "--datetime"), {
        "action": "store_true", 'default': False,
        "dest": "datetime",
        "help": "Datetime to search (format like 2013-02-14T01:52:17)."
    }),
    # вспомогательные опции
    (("-k", "--keys"), {
        'action': "store_true", 'dest': "keybindings",
        'default': False, 'help': "Show keybindings and quit"
    }),
    #
    (("-o", "--offset"), {
        'type': float, 'default': 0.0,
        'dest': "starttime_offset",
        'help': "Offset to add to specified starttime in seconds."
    }),
)


SEISMIC_PHASES = ('P', 'S')

PHASE_COLORS = {
    'P': "red", 'S': "blue",
    'Psynth': "black", 'Ssynth': "black",
    'Mag': "green",
    'PErr1': "red", 'PErr2': "red",
    'SErr1': "blue", 'SErr2': "blue",
    "E": 'black',
}

PHASE_LINESTYLES = {
    'P': "-", 'S': "-", "E": "-",
    'Psynth': "--", 'Ssynth': "--",
    'PErr1': "-", 'PErr2': "-",
    'SErr1': "-", 'SErr2': "-",
}
PHASE_LINEHEIGHT_PERC = {
    'P': 1, 'S': 1, 'Psynth': 1, 'Ssynth': 1,
    "E": 1,
    'PErr1': 0.75, 'PErr2': 0.75, 'SErr1': 0.75, 'SErr2': 0.75
}
KEY_FULLNAMES = {
    'P': "P pick", 'Psynth': "synthetic P pick",
    "E": "E pick",
    'PWeight': "P pick weight", 'PPol': "P pick polarity",
    'POnset': "P pick onset", 'PErr1': "left P error pick",
    'PErr2': "right P error pick", 'S': "S pick",
    'Ssynth': "synthetic S pick", 'SWeight': "S pick weight",
    'SPol': "S pick polarity", 'SOnset': "S pick onset",
    'SErr1': "left S error pick", 'SErr2': "right S error pick",
    'MagMin1': "Magnitude minimum estimation pick",
    'MagMax1': "Magnitude maximum estimation pick",
    'MagMin2': "Magnitude minimum estimation pick",
    'MagMax2': "Magnitude maximum estimation pick"
}

WIDGET_NAMES = (
    "qToolButton_clearAll",
    "qToolButton_overview",
    "qComboBox_phaseType",
    "qPlainTextEdit_stdout", "qPlainTextEdit_stderr"
)


AXVLINEWIDTH = 1.2
# dictionary for key-bindings.
KEYS = {
    'setPick': "a",
    'setPickError': "s",
    'delPick': "q",
    'setMagMin': "a", 'setMagMax': "s", 'delMagMinMax': "q",
    'switchPhase': "control",
    'prevStream': "y", 'nextStream': "x", 'switchWheelZoomAxis': "shift",
    'setWeight': {'0': 0, '1': 1, '2': 2, '3': 3},
    'setPol': {'u': "up", 'd': "down", '+': "poorup", '-': "poordown"},
    'setOnset': {'i': "impulsive", 'e': "emergent"},
}


S_POL_MAP_ZRT = {'R': {'up': "forward", 'down': "backward",
                       'poorup': "forward", 'poordown': "backward"},
                 'T': {'up': "right", 'down': "left",
                       'poorup': "right", 'poordown': "left"}}
S_POL_PHASE_TYPE = {'R': "SV", 'T': "SH"}
POLARITY_2_FOCMEC = {'up': "U", 'poorup': "+", 'down': "D", 'poordown': "-",
    'left': "L", 'right': "R", 'forward': "F", 'backward': "B"}

# the following dicts' keys should be all lower case, we use "".lower() later
POLARITY_CHARS = POLARITY_2_FOCMEC
ONSET_CHARS = {'impulsive': "I", 'emergent': "E", 'implusive': "I"}


class QMplCanvas(QFigureCanvas):
    """
    Class to represent the FigureCanvas widget.
    """
    def __init__(self, parent=None):
        # Standard Matplotlib code to generate the plot
        self.fig = Figure()
        # initialize the canvas where the Figure renders into
        QFigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

def matplotlib_color_to_rgb(color):
    """
    Converts matplotlib colors to rgb.
    """
    rgb = ColorConverter().to_rgb(color)
    return [int(_i*255) for _i in rgb]

class MultiCursor(MplMultiCursor):
    def __init__(self, canvas, axes, useblit=True, **lineprops):
        self.canvas = canvas
        self.axes = axes
        xmin, xmax = axes[-1].get_xlim()
        xmid = 0.5*(xmin+xmax)
        self.lines = [ax.axvline(xmid, visible=False, **lineprops) for ax in axes]
        self.visible = True
        self.useblit = useblit
        self.background = None
        self.needclear = False
        self.id1=self.canvas.mpl_connect('motion_notify_event', self.onmove)
        self.id2=self.canvas.mpl_connect('draw_event', self.clear)
    

def formatXTicklabels(x, *pos):
    """
    Make a nice formatting for y axis ticklabels: minutes:seconds.microsec
    """
    # x is of type numpy.float64, the string representation of that float
    # strips of all tailing zeros
    # pos returns the position of x on the axis while zooming, None otherwise
    min = int(x / 60.)
    if min > 0:
        sec = x % 60
        return "%i:%06.3f" % (min, sec)
    else:
        return "%.3f" % x

class SplitWriter():
    """
    Implements a write method that writes a given message on all children
    """
    def __init__(self, *objects):
        """
        Remember provided objects as children.
        """
        self.children = objects

    def write(self, msg):
        """
        Sends msg to all childrens write method.
        """
        for obj in self.children:
            if isinstance(obj, PyQt4.QtGui.QPlainTextEdit):
                if msg == '\n':
                    return
                obj.appendPlainText(msg)
            else:
                obj.write(msg)


def setup_dicts(streams, options):
    """
    Function to set up the list of dictionaries that is used on the streams list.
    Also removes streams that do not provide the necessary metadata.
    """
    dicts = []
    # we need to go through streams/dicts backwards in order not to get
    # problems because of the pop() statement
    for st in streams:
    #for i in range(len(streams))[::-1]:
        dic = {}
        trZ = st.select(component="Z")[0]
        dic['MagUse'] = True
        sta = trZ.stats.station.strip()
        dic['Station'] = sta
        dicts.append(dic)
    return dicts

#=== my own

DATA_DIR = "seisobr"


DB_OPTIONS = {
    'host': '172.16.200.1',
    'database': 'seisobr',
    'user': 'pguser',
    'password': 'my_password',
}

CONN_STRING = "host='%(host)s' dbname='%(database)s' user='%(user)s' password='%(password)s'" % DB_OPTIONS


# запросы

SELECT_CODES = """\
SELECT "prnbase01_prns"."idPrn", "prnbase01_prnsdir"."Path", "prnbase01_prns"."seisFile"
FROM "prnbase01_prns"
INNER JOIN "prnbase01_prnsdir"
ON "prnbase01_prnsdir"."idDir" = "prnbase01_prns"."idDir"
WHERE "prnbase01_prns"."idDir" = %s
ORDER BY 1;\
"""

SELECT_WAVES = """\
SELECT "prnbase01_prnswaves"."NameWave", "prnbase01_prnswaves"."TimeWave",
    "prnbase01_prnswaves"."idWave"
FROM "prnbase01_prnswaves"
INNER JOIN "prnbase01_prns"
ON "prnbase01_prns"."idPrn" = "prnbase01_prnswaves"."idPrn"
WHERE "prnbase01_prnswaves"."idPrn" = %s
AND "prnbase01_prnswaves"."NameWave" NOT LIKE '__m'
;\
"""
#--AND "seisobr_prnswaves"."NameWave" NOT LIKE '%m'
#--where letter "m" is not in NameWave

UPDATE_WAVES = 'UPDATE "prnbase01_prnswaves" SET "TimeWave"=%s WHERE "idWave"=%s;'


def execute_query(cursor, query, params):
    """ ищем записи """
    try:
        cursor.execute(query, tuple(params,))
    except psycopg2.Error, msg:
        print("An error ocured while executing query:", msg)
        #return []
    else:
        return cursor.fetchall()


def setup_db_connection():
    conn_string = "host='%(host)s' dbname='%(database)s' user='%(user)s' password='%(password)s'" % DB_OPTIONS
    try:
        conn = psycopg2.connect(conn_string)
    except psycopg2.OperationalError, msg:
        print("Error connecting to database with problem:", msg)
        #sys.exit(1)
    cursor = conn.cursor()
    return (conn, cursor)



#=== BAIKAL data handling

def get_traces_from_baikal_file(filename):
    # загружать данные из файла формата Байкал
    bf = BaikalFile(filename)
    if not bf.valid:
        print("\nSkipping file %s" % filename)
        return
    # time
    _hour, _minute, _seconds = get_time(bf.main_header.to, unpack=True)
    # and UTCDateTime
    utcdatetime = UTCDateTime(
        bf.main_header.year,
        bf.main_header.month,
        bf.main_header.day,
        int(_hour), int(_minute), _seconds,
        precision=3,# digits after point
    )
    # все каналы (трассы) из файла
    traces = []
    for i, channel in enumerate(bf.channels):
        # repair name of channel
        ch_name = channel.name_chan[0].upper()
        # создадим заголовок
        header = {
            'network': 'BR',
            'station': bf.main_header.station.upper(),
            'location': '',
            'channel': ch_name,
            'npts': len(bf.data[i]),
            'sampling_rate': 1. / bf.main_header.dt,
            'starttime': utcdatetime,
        }
        traces += [Trace(header=header, data=bf.data[i])]
    return traces


def calc_seconds_from_T0(str_wave, T0):
    """
    T0 - type=UTCDateTime
    """
    # вступления волн рассчитать относительно глобального начала (Т0), в секундах
    t_wave = datetime.datetime.strptime(str_wave, "%H:%M:%S.%f")
    dt = datetime.datetime.combine(T0.date, t_wave.time())
    assert dt > T0.datetime, "time ow wave smaller then start of file! %s<%s" % (dt,T0)
    delta = dt - T0.datetime
    return delta.total_seconds()


