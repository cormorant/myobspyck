# -*- coding: utf-8 -*-
import os
import sys
import copy



from obspy.core import UTCDateTime, Trace, Stream
from obspy.core import read



COMMANDLINE_OPTIONS = (
    (("-d", "--dir"), {
        'dest': "directory",
        'help': "Directory in seisobr where to find seismogramms"
    }),
    (("-f", "--files"), {
        'type': "string", 'dest': "files",
        'help': "Local files containing waveform data. List of "
        "absolute paths separated by commas (,)"
    }),
    #(("-i", "--iddir"), {"type": "int", "dest": "iddir",
    #    'help': "Search files by query in database by idDir"}),
    #
    (("-t", "--datetime"), {
        "type": "string",
        "dest": "dt",
        "help": "Datetime to search (format like 2013-02-14T01:52:17)."
    }),
    (("-k", "--keys"), {
        'action': "store_true", 'dest': "keybindings",
        'default': False, 'help': "Show keybindings and quit"
    }),
    #
    (("--nometadata",), {
        'action': "store_true",
        'dest': "nometadata", 'default': True,
        'help': "Deactivate fetching/parsing metadata for waveforms"
    }),
    #
    (("-o", "--starttime-offset"), {
        'type': "float", 'dest': "starttime_offset",
        'default': 0.0,
        'help': "Offset to add to specified starttime in seconds."
    }),
)

SEISMIC_PHASES = ('P', 'S')

PHASE_COLORS = {'P': "red", 'S': "blue", 'Psynth': "black", 'Ssynth': "black",
        'Mag': "green", 'PErr1': "red", 'PErr2': "red", 'SErr1': "blue",
        'SErr2': "blue"}

PHASE_LINESTYLES = {'P': "-", 'S': "-", 'Psynth': "--", 'Ssynth': "--",
        'PErr1': "-", 'PErr2': "-", 'SErr1': "-", 'SErr2': "-"}
PHASE_LINEHEIGHT_PERC = {'P': 1, 'S': 1, 'Psynth': 1, 'Ssynth': 1,
        'PErr1': 0.75, 'PErr2': 0.75, 'SErr1': 0.75, 'SErr2': 0.75}
KEY_FULLNAMES = {'P': "P pick", 'Psynth': "synthetic P pick",
        'PWeight': "P pick weight", 'PPol': "P pick polarity",
        'POnset': "P pick onset", 'PErr1': "left P error pick",
        'PErr2': "right P error pick", 'S': "S pick",
        'Ssynth': "synthetic S pick", 'SWeight': "S pick weight",
        'SPol': "S pick polarity", 'SOnset': "S pick onset",
        'SErr1': "left S error pick", 'SErr2': "right S error pick",
        'MagMin1': "Magnitude minimum estimation pick",
        'MagMax1': "Magnitude maximum estimation pick",
        'MagMin2': "Magnitude minimum estimation pick",
        'MagMax2': "Magnitude maximum estimation pick"}
WIDGET_NAMES = (
    "qToolButton_clearAll",
    "qToolButton_overview",
    "qComboBox_phaseType",
    "qPlainTextEdit_stdout", "qPlainTextEdit_stderr"
)
#Estimating the maximum/minimum in a sample-window around click
#MAG_PICKWINDOW = 10
#MAG_MARKER = {'marker': "x", 'edgewidth': 1.8, 'size': 20}
AXVLINEWIDTH = 1.2
# dictionary for key-bindings.
KEYS = {'setPick': "a", 'setPickError': "s", 'delPick': "q",
        'setMagMin': "a", 'setMagMax': "s", 'delMagMinMax': "q",
        'switchPhase': "control",
        'prevStream': "y", 'nextStream': "x", 'switchWheelZoomAxis': "shift",
        'setWeight': {'0': 0, '1': 1, '2': 2, '3': 3},
        'setPol': {'u': "up", 'd': "down", '+': "poorup", '-': "poordown"},
        'setOnset': {'i': "impulsive", 'e': "emergent"}}
# XXX Qt:
#KEYS = {'setPick': "Key_A", 'setPickError': "Key_S", 'delPick': "Key_Q",
#        'setMagMin': "Key_A", 'setMagMax': "Key_S", 'delMagMinMax': "Key_Q",
#        'switchPhase': "Key_Control",
#        'prevStream': "Key_Y", 'nextStream': "Key_X", 'switchWheelZoomAxis': "Key_Shift",
#        'setWeight': {'Key_0': 0, 'Key_1': 1, 'Key_2': 2, 'Key_3': 3},
#        'setPol': {'Key_U': "up", 'Key_D': "down", 'Key_Plus': "poorup", 'Key_Minus': "poordown"},
#        'setOnset': {'Key_I': "impulsive", 'Key_E': "emergent"}}

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

def check_keybinding_conflicts(keys):
    """
    check for conflicting keybindings. 
    we have to check twice, because keys for setting picks and magnitudes
    are allowed to interfere...
    """
    for ignored_key_list in [['setMagMin', 'setMagMax', 'delMagMinMax'],
                             ['setPick', 'setPickError', 'delPick']]:
        tmp_keys = copy.deepcopy(keys)
        tmp_keys2 = {}
        for ignored_key in ignored_key_list:
            tmp_keys.pop(ignored_key)
        while tmp_keys:
            key, item = tmp_keys.popitem()
            if isinstance(item, dict):
                while item:
                    k, v = item.popitem()
                    tmp_keys2["_".join([key, str(v)])] = k
            else:
                tmp_keys2[key] = item
        if len(set(tmp_keys2.keys())) != len(set(tmp_keys2.values())):
            err = "Interfering keybindings. Please check variable KEYS"
            raise Exception(err)

def fetch_waveforms_with_metadata(options):
    getPAZ = not options.nometadata
    getCoordinates = not options.nometadata
    t1 = UTCDateTime(options.time) + options.starttime_offset
    t2 = t1 + options.duration
    streams = []
    clients = {}
    sta_fetched = set()
    # Local files:
    if options.files:
        print "=" * 80
        print "Reading local files:"
        print "-" * 80
        parsers = []
        for file in options.files.split(","):
            print file
            st = read(file, starttime=t1, endtime=t2, verify_chksum=options.verify_chksum)
            streams.append(st)
    #
    print "=" * 80
    return (clients, streams)

def setup_dicts(streams, options):
    """
    Function to set up the list of dictionaries that is used alongside the
    streams list.
    Also removes streams that do not provide the necessary metadata.
    :returns: (list(:class:`obspy.core.stream.Stream`s),
               list(dict))
    """
    #set up a list of dictionaries to store all picking data
    # set all station magnitude use-flags False
    dicts = []
    for i in xrange(len(streams)):
        dicts.append({})
    # we need to go through streams/dicts backwards in order not to get
    # problems because of the pop() statement
    for i in range(len(streams))[::-1]:
        dict = dicts[i]
        st = streams[i]
        trZ = st.select(component="Z")[0]
        if len(st) == 3:
            trN = st.select(component="N")[0]
            trE = st.select(component="E")[0]
        dict['MagUse'] = False#True
        sta = trZ.stats.station.strip()
        dict['Station'] = sta
        #XXX not used: dictsMap[sta] = dict
        # XXX should not be necessary
        '''
        if net == '':
            net = 'BR'
            print "Warning: Got no network information, setting to " + \
                  "default: BR"
        '''
        if not options.nometadata:
            try:
                dict['StaLon'] = trZ.stats.coordinates.longitude
                dict['StaLat'] = trZ.stats.coordinates.latitude
                dict['StaEle'] = trZ.stats.coordinates.elevation / 1000. # all depths in km!
                dict['pazZ'] = trZ.stats.paz
                if len(st) == 3:
                    dict['pazN'] = trN.stats.paz
                    dict['pazE'] = trE.stats.paz
            except:
                net = trZ.stats.network.strip()
                print 'Error: Missing metadata for %s. Discarding stream.' \
                        % (":".join([net, sta]))
                streams.pop(i)
                dicts.pop(i)
                continue
    return streams, dicts


#Monkey patch (need to remember the ids of the mpl_connect-statements to remove them later)
#See source: http://matplotlib.sourcearchive.com/documentation/0.98.1/widgets_8py-source.html
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

#====================

DB_OPTIONS = {
    'host': '172.16.200.1',
    'database': 'seisobr',
    'user': 'pguser',
    'password': 'my_password',
}

SETTINGS = {
    "width": 800, #1360,
    "height": 400,#700
}

DATA_DIR = "seisobr" # папка где хранятся сейсмограммы


#'SELECT "idPrn", "seisFile" FROM "seisobr_prns" WHERE "idDir" = %s'
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

CANALS = ("NS", "EW", "Z", "NSg", "EWg", "Zg")



def execute_query(QUERY, params):
    """ выполняем запрос и возвращаем его результат """
    try:
        cursor.execute(QUERY, tuple(params,))
    except psycopg2.Error, msg:
        print("An error ocured while executing query:", msg)
    else:
        return cursor.fetchall()


def secfromtime(time):
    """ вернуть число в секундах (и милисек) из времени """
    #tim.hour * 3600 + tim.minute * 60 + tim.second
    # если параметр - строка
    if isinstance(time, str):
        t = time.split(':')
        return int(t[0]) * 3600 + int(t[1]) * 60 + float(t[2])
    else:
        raise NotImplementedError


def read_baikal(filename):
    """ читаем заголовок и область данных в файле формата Байкал """
    #try:
    if not os.path.exists(filename):
        print("File not found: %s" % filename)
        return
    # work on file
    with open(filename, "rb") as _f:
        nkan = struct.unpack("h", _f.read(2))[0]
        # проверка на количество каналов
        if not (nkan in range(1,7)): return
        # разрядность
        _f.seek(18)
        razr = struct.unpack("h", _f.read(2))[0]
        # дискретизация
        _f.seek(48)
        sampl_rate = struct.unpack("d", _f.read(8))[0]
        # считать значение первой секунды
        t0 = struct.unpack("d", _f.read(8))[0]
        # где начинаются данные
        offset = 120 + nkan * 72
        _f.seek(offset)
        # считываются массивы с данными
        a = np.fromstring(_f.read(), dtype=np.int16 if razr==16 else np.int32)
        # обрезать массив с конца пока он не делится на 3
        while len(a) % 3 != 0: a = a[:-1]
        # демультиплексируем
        data = a.reshape((len(a)/nkan, nkan)).T
        #a.fromstring(data)
        # вернуть + массив с demultuplex данными и количество каналов
    return sampl_rate, t0, data, nkan


