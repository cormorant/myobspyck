# -*- coding: utf-8 -*-
import os
import sys
import math
import platform
import shutil
import subprocess
import copy
import tempfile
import glob
import fnmatch

import PyQt4
import numpy as np
import matplotlib as mpl
from matplotlib.colors import ColorConverter
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as QFigureCanvas
from matplotlib.widgets import MultiCursor as MplMultiCursor

from obspy.core import UTCDateTime, Trace, Stream
from obspy.core import read
from obspy.xseed import Parser
try:
    from obspy.core.util import gps2DistAzimuth
except:
    from obspy.signal import gps2DistAzimuth

from baikal import BaikalFile, get_time


mpl.rc('figure.subplot', left=0.05, right=0.98, bottom=0.10, top=0.92,
       hspace=0.28)
mpl.rcParams['font.size'] = 10


COMMANDLINE_OPTIONS = (
    # XXX wasn't working as expected
    #(("--debug"), {'dest': "debug", 'action': "store_true",
    #        'default': True,
    #        'help': "Switch on Ipython debugging in case of exception"}),
    (("-t", "--time"), {'dest': "time",
            'help': "Starttime of seismogram to retrieve. It takes a "
            "string which UTCDateTime can convert. E.g. "
            "'2010-01-10T05:00:00'"}),
    (("-d", "--duration"), {'type': "float", 'dest': "duration",
            'help': "Duration of seismogram in seconds"}),
    (("-f", "--files"), {'type': "string", 'dest': "files",
            'help': "Local files containing waveform data. List of "
            "absolute paths separated by commas"}),
    (("--dataless",), {'type': "string", 'dest': "dataless",
            'help': "Local Dataless SEED files to look up metadata for "
            "local waveform files. List of absolute paths separated by "
            "commas"}),
    (("-i", "--seishub-ids"), {'dest': "seishub_ids", 'default': "",
            'help': "Ids to retrieve from SeisHub. Star for channel and "
            "wildcards for stations are allowed, e.g. "
            "'BW.RJOB..EH*,BW.RM?*..EH*'"}),
    (("--seishub-servername",), {'dest': "seishub_servername",
            'default': 'teide',
            'help': "Servername of the SeisHub server"}),
    (("--seishub-port",), {'type': "int", 'dest': "seishub_port",
            'default': 8080, 'help': "Port of the SeisHub server"}),
    (("--seishub-user",), {'dest': "seishub_user", 'default': 'obspyck',
            'help': "Username for SeisHub server"}),
    (("--seishub-password",), {'dest': "seishub_password",
            'default': 'obspyck', 'help': "Password for SeisHub server"}),
    (("--seishub-timeout",), {'dest': "seishub_timeout", 'type': "int",
            'default': 10, 'help': "Timeout for SeisHub server"}),
    (("-k", "--keys"), {'action': "store_true", 'dest': "keybindings",
            'default': False, 'help': "Show keybindings and quit"}),
    (("--lowpass",), {'type': "float", 'dest': "lowpass", 'default': 10.0,
            'help': "Frequency for Lowpass-Slider"}),
    (("--highpass",), {'type': "float", 'dest': "highpass", 'default': 1.0,
            'help': "Frequency for Highpass-Slider"}),
    (("--sta",), {'type': "float", 'dest': "sta", 'default': 3,
            'help': "Window length for STA-Slider"}),
    (("--lta",), {'type': "float", 'dest': "lta", 'default': 10.0,
            'help': "Window length for LTA-Slider"}),
    (("--ar-f1",), {'type': "float", 'dest': "ar_f1",
            'default': 1.0, 'help': "Low corner frequency of AR picker"}),
    (("--ar-f2",), {'type': "float", 'dest': "ar_f2",
            'default': 20.0, 'help': "High corner frequency of AR picker"}),
    (("--ar-sta_p",), {'type': "float", 'dest': "ar_sta_p",
            'default': 0.1, 'help': "P STA window length of AR picker"}),
    (("--ar-lta_p",), {'type': "float", 'dest': "ar_lta_p",
            'default': 1.0, 'help': "P LTA window length of AR picker"}),
    (("--ar-sta_s",), {'type': "float", 'dest': "ar_sta_s",
            'default': 1.0, 'help': "S STA window length of AR picker"}),
    (("--ar-lta_s",), {'type': "float", 'dest': "ar_lta_s",
            'default': 4.0, 'help': "S LTA window length of AR picker"}),
    (("--ar-m_p",), {'type': "int", 'dest': "ar_m_p",
            'default': 2, 'help': "number of coefficients for P of AR picker"}),
    (("--ar-m_s",), {'type': "int", 'dest': "ar_m_s",
            'default': 8, 'help': "number of coefficients for S of AR picker"}),
    (("--ar-l_p",), {'type': "float", 'dest': "ar_l_p",
            'default': 0.1, 'help': "variance window length for P of AR picker"}),
    (("--ar-l_s",), {'type': "float", 'dest': "ar_l_s",
            'default': 0.2, 'help': "variance window length for S of AR picker"}),
    (("--nozeromean",), {'action': "store_true", 'dest': "nozeromean",
            'default': False,
            'help': "Deactivate offset removal of traces"}),
    (("--nonormalization",), {'action': "store_true",
            'dest': "nonormalization", 'default': False,
            'help': "Deactivate normalization to nm/s for plotting " + \
            "using overall sensitivity (tr.stats.paz.sensitivity)"}),
    (("--nometadata",), {'action': "store_true",
            'dest': "nometadata", 'default': False,
            'help': "Deactivate fetching/parsing metadata for waveforms"}),
    (("--pluginpath",), {'dest': "pluginpath",
            'default': "/baysoft/obspyck/",
            'help': "Path to local directory containing the folders with "
            "the files for the external programs. Large files/folders "
            "should only be linked in this directory as the contents are "
            "copied to a temporary directory (links are preserved)."}),
    (("-o", "--starttime-offset"), {'type': "float", 'dest': "starttime_offset",
            'default': 0.0, 'help': "Offset to add to specified starttime "
            "in seconds. Thus a time from an automatic picker can be used "
            "with a specified offset for the starttime. E.g. to request a "
            "waveform starting 30 seconds earlier than the specified time "
            "use -30."}),
    (("-m", "--merge"), {'type': "choice", 'dest': "merge", 'default': "",
            'choices': ("", "safe", "overwrite"),
            'help': "After fetching the streams run a merge "
            "operation on every stream. If not done, streams with gaps "
            "and therefore more traces per channel get discarded.\nTwo "
            "methods are supported (see http://docs.obspy.org/packages/"
            "auto/obspy.core.trace.Trace.__add__.html  for details)\n  "
            "\"safe\": overlaps are discarded "
            "completely\n  \"overwrite\": the second trace is used for "
            "overlapping parts of the trace"}),
    (("--arclink-ids",), {'dest': "arclink_ids", 'default': '',
            'help': "Ids to retrieve via arclink, star for channel "
            "is allowed, e.g. 'BW.RJOB..EH*,BW.ROTZ..EH*'"}),
    (("--arclink-servername",), {'dest': "arclink_servername",
            'default': 'webdc.eu',
            'help': "Servername of the arclink server"}),
    (("--arclink-port",), {'type': "int", 'dest': "arclink_port",
            'default': 18001, 'help': "Port of the arclink server"}),
    (("--arclink-user",), {'dest': "arclink_user", 'default': 'Anonymous',
            'help': "Username for arclink server"}),
    (("--arclink-password",), {'dest': "arclink_password", 'default': '',
            'help': "Password for arclink server"}),
    (("--arclink-institution",), {'dest': "arclink_institution",
            'default': 'Anonymous',
            'help': "Password for arclink server"}),
    (("--arclink-timeout",), {'dest': "arclink_timeout", 'type': "int",
            'default': 20, 'help': "Timeout for arclink server"}),
    (("--fissures-ids",), {'dest': "fissures_ids", 'default': '',
            'help': "Ids to retrieve via Fissures, star for component "
            "is allowed, e.g. 'GE.APE..BH*,GR.GRA1..BH*'"}),
    (("--fissures-network_dc",), {'dest': "fissures_network_dc",
            'default': ("/edu/iris/dmc", "IRIS_NetworkDC"),
            'help': "Tuple containing Fissures dns and NetworkDC name."}),
    (("--fissures-seismogram_dc",), {'dest': "fissures_seismogram_dc",
            'default': ("/edu/iris/dmc", "IRIS_DataCenter"),
            'help': "Tuple containing Fissures dns and DataCenter name."}),
    (("--fissures-name_service",), {'dest': "fissures_name_service",
            'default': "dmc.iris.washington.edu:6371/NameService",
            'help': "String containing the Fissures name service."}),
    (("--ignore-chksum",), {'action': "store_false", 'dest': "verify_chksum",
            'default': True,
            'help': "Deactivate chksum check for local GSE2 files"}),
    (("--filter",), {'action': "store_true", 'dest': "filter",
            'default': False,
            'help': "Switch filter button on at startup."}))

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
WIDGET_NAMES = ("qToolButton_clearAll",
    #"qToolButton_clearOrigMag",
    #"qToolButton_clearFocMec",
    #"qToolButton_doHyp2000",
    #"qToolButton_do3dloc", "qToolButton_doNlloc", "qComboBox_nllocModel",
    #"qToolButton_calcMag", "qToolButton_doFocMec",
    #"qToolButton_showMap",
    #"qToolButton_showFocMec", "qToolButton_nextFocMec",
    #"qToolButton_showWadati", "qToolButton_getNextEvent",
    #"qToolButton_updateEventList", "qToolButton_sendNewEvent",
    #"qToolButton_replaceEvent", "qCheckBox_publishEvent",
    #"qToolButton_deleteEvent", "qCheckBox_sysop",
    #"qLineEdit_sysopPassword", "qComboBox_eventType",
    #"qToolButton_previousStream", "qLabel_streamNumber",
    #"qComboBox_streamName", "qToolButton_nextStream",
    "qToolButton_overview",
    "qComboBox_phaseType",
    #"qToolButton_rotateLQT", "qToolButton_rotateZRT", "qToolButton_filter", "qToolButton_trigger",
    #"qToolButton_arpicker", "qComboBox_filterType", "qCheckBox_zerophase",
    #"qLabel_highpass", "qDoubleSpinBox_highpass", "qLabel_lowpass",
    #"qDoubleSpinBox_lowpass", "qLabel_sta", "qDoubleSpinBox_sta",
    #"qLabel_lta", "qDoubleSpinBox_lta", "qToolButton_spectrogram",
    #"qCheckBox_spectrogramLog", "qLabel_wlen", "qDoubleSpinBox_wlen",
    #"qLabel_perlap", "qDoubleSpinBox_perlap",
    "qPlainTextEdit_stdout", "qPlainTextEdit_stderr"
)
#Estimating the maximum/minimum in a sample-window around click
MAG_PICKWINDOW = 10
MAG_MARKER = {'marker': "x", 'edgewidth': 1.8, 'size': 20}
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

ROTATE_LQT_COMP_MAP = {"Z": "L", "N": "Q", "E": "T"}
ROTATE_ZRT_COMP_MAP = {"Z": "Z", "N": "R", "E": "T"}
S_POL_MAP_ZRT = {'R': {'up': "forward", 'down': "backward",
                       'poorup': "forward", 'poordown': "backward"},
                 'T': {'up': "right", 'down': "left",
                       'poorup': "right", 'poordown': "left"}}
S_POL_PHASE_TYPE = {'R': "SV", 'T': "SH"}
POLARITY_2_FOCMEC = {'up': "U", 'poorup': "+", 'down': "D", 'poordown': "-",
                     'left': "L", 'right': "R", 'forward': "F", 'backward': "B"}

# the following dicts' keys should be all lower case, we use "".lower() later
POLARITY_CHARS = POLARITY_2_FOCMEC
ONSET_CHARS = {'impulsive': "I", 'emergent': "E",
               'implusive': "I"} # XXX some old events have a typo there... =)

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
    """
    Sets up obspy clients and fetches waveforms and metadata according to command
    line options.
    Now also fetches data via arclink (fissures) if --arclink-ids
    (--fissures-ids) is used.
    XXX Notes: XXX
     - there is a problem in the arclink client with duplicate traces in
       fetched streams. therefore at the moment it might be necessary to use
       "-m overwrite" option.

    :returns: (dictionary with clients,
               list(:class:`obspy.core.stream.Stream`s))
    """
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
        #for file in options.dataless.split(","):
        #    print file
        #    parsers.append(Parser(file))
        for file in options.files.split(","):
            print file
            st = read(file, starttime=t1, endtime=t2, verify_chksum=options.verify_chksum)
            streams.append(st)
    #
    print "=" * 80
    return (clients, streams)

def merge_check_and_cleanup_streams(streams, options):
    """
    Cleanup given list of streams so that they conform with what ObsPyck
    expects.

    Conditions:
    - either one Z or three ZNE traces
    - no two streams for any station (of same network)
    - no streams with traces of different stations

    :returns: (warn_msg, merge_msg, list(:class:`obspy.core.stream.Stream`s))
    """
    # Merge on every stream if this option is passed on command line:
    for st in streams:
        st.merge(method=-1)
    if options.merge:
        if options.merge.lower() == "safe":
            for st in streams:
                st.merge(method=0)
        elif options.merge.lower() == "overwrite":
            for st in streams:
                st.merge(method=1)
        else:
            err = "Unrecognized option for merging traces. Try " + \
                  "\"safe\" or \"overwrite\"."
            raise Exception(err)

    # Sort streams again, if there was a merge this could be necessary 
    for st in streams:
        st.sort()
        st.reverse()
    sta_list = set()
    # we need to go through streams/dicts backwards in order not to get
    # problems because of the pop() statement
    warn_msg = ""
    merge_msg = ""
    # XXX we need the list() because otherwise the iterator gets garbled if
    # XXX removing streams inside the for loop!!
    for st in list(streams):
        # check for streams with mixed stations/networks and remove them
        if len(st) != len(st.select(network=st[0].stats.network,
                                    station=st[0].stats.station)):
            msg = "Warning: Stream with a mix of stations/networks. " + \
                  "Discarding stream."
            print msg
            warn_msg += msg + "\n"
            streams.remove(st)
            continue
        net_sta = "%s.%s" % (st[0].stats.network.strip(),
                             st[0].stats.station.strip())
        # Here we make sure that a station/network combination is not
        # present with two streams.
        if net_sta in sta_list:
            msg = "Warning: Station/Network combination \"%s\" " + \
                  "already in stream list. Discarding stream." % net_sta
            print msg
            warn_msg += msg + "\n"
            streams.remove(st)
            continue
        if len(st) not in [1, 3]:
            msg = 'Warning: All streams must have either one Z trace ' + \
                  'or a set of three ZNE traces.'
            print msg
            warn_msg += msg + "\n"
            # remove all unknown channels ending with something other than
            # Z/N/E and try again...
            removed_channels = ""
            for tr in st:
                if tr.stats.channel[-1] not in ["Z", "N", "E"]:
                    removed_channels += " " + tr.stats.channel
                    st.remove(tr)
            if len(st.traces) in [1, 3]:
                msg = 'Warning: deleted some unknown channels in ' + \
                      'stream %s.%s' % (net_sta, removed_channels)
                print msg
                warn_msg += msg + "\n"
                continue
            else:
                msg = 'Stream %s discarded.\n' % net_sta + \
                      'Reason: Number of traces != (1 or 3)'
                print msg
                warn_msg += msg + "\n"
                #for j, tr in enumerate(st.traces):
                #    msg = 'Trace no. %i in Stream: %s\n%s' % \
                #            (j + 1, tr.stats.channel, tr.stats)
                msg = str(st)
                print msg
                warn_msg += msg + "\n"
                streams.remove(st)
                merge_msg = '\nIMPORTANT:\nYou can try the command line ' + \
                        'option merge (-m safe or -m overwrite) to ' + \
                        'avoid losing streams due gaps/overlaps.'
                continue
        if len(st) == 1 and st[0].stats.channel[-1] != 'Z':
            msg = 'Warning: All streams must have either one Z trace ' + \
                  'or a set of three ZNE traces.'
            msg += 'Stream %s discarded. Reason: ' % net_sta + \
                   'Exactly one trace present but this is no Z trace'
            print msg
            warn_msg += msg + "\n"
            #for j, tr in enumerate(st.traces):
            #    msg = 'Trace no. %i in Stream: %s\n%s' % \
            #            (j + 1, tr.stats.channel, tr.stats)
            msg = str(st)
            print msg
            warn_msg += msg + "\n"
            streams.remove(st)
            continue
        if len(st) == 3 and (st[0].stats.channel[-1] != 'Z' or
                             st[1].stats.channel[-1] != 'N' or
                             st[2].stats.channel[-1] != 'E'):
            msg = 'Warning: All streams must have either one Z trace ' + \
                  'or a set of three ZNE traces.'
            msg += 'Stream %s discarded. Reason: ' % net_sta + \
                   'Exactly three traces present but they are not ZNE'
            print msg
            warn_msg += msg + "\n"
            #for j, tr in enumerate(st.traces):
            #    msg = 'Trace no. %i in Stream: %s\n%s' % \
            #            (j + 1, tr.stats.channel, tr.stats)
            msg = str(st)
            print msg
            warn_msg += msg + "\n"
            streams.remove(st)
            continue
        sta_list.add(net_sta)
    # demean traces if not explicitly deactivated on command line
    if not options.nozeromean:
        for st in streams:
            st.detrend('simple')
            st.detrend('constant')
    return (warn_msg, merge_msg, streams)

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
        #if net == '':
        #    net = 'BW'
        #    print "Warning: Got no network information, setting to " + \
        #          "default: BW"
        #'''
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
        #'''
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
    
   
def gk2lonlat(x, y, m_to_km=True):
    """
    This function converts X/Y Gauss-Krueger coordinates (zone 4, central
    meridian 12 deg) to Longitude/Latitude in WGS84 reference ellipsoid.
    We do this using pyproj (python bindings for proj4) which can be installed
    using 'easy_install pyproj' from pypi.python.org.
    Input can be single coordinates or coordinate lists/arrays.
    
    Useful Links:
    http://pyproj.googlecode.com/svn/trunk/README.html
    http://trac.osgeo.org/proj/
    http://www.epsg-registry.org/
    """
    import pyproj

    proj_wgs84 = pyproj.Proj(init="epsg:4326")
    proj_gk4 = pyproj.Proj(init="epsg:31468")
    # convert to meters first
    if m_to_km:
        x = x * 1000.
        y = y * 1000.
    lon, lat = pyproj.transform(proj_gk4, proj_wgs84, x, y)
    return (lon, lat)


def errorEllipsoid2CartesianErrors(azimuth1, dip1, len1, azimuth2, dip2, len2,
                                   len3):
    """
    This method converts the location error of NLLoc given as the 3D error
    ellipsoid (two azimuths, two dips and three axis lengths) to a cartesian
    representation.
    We calculate the cartesian representation of each of the ellipsoids three
    eigenvectors and use the maximum of these vectors components on every axis.
    """
    z = len1 * np.sin(np.radians(dip1))
    xy = len1 * np.cos(np.radians(dip1))
    x = xy * np.sin(np.radians(azimuth1))
    y = xy * np.cos(np.radians(azimuth1))
    v1 = np.array([x, y, z])

    z = len2 * np.sin(np.radians(dip2))
    xy = len2 * np.cos(np.radians(dip2))
    x = xy * np.sin(np.radians(azimuth2))
    y = xy * np.cos(np.radians(azimuth2))
    v2 = np.array([x, y, z])

    v3 = np.cross(v1, v2)
    v3 /= np.sqrt(np.dot(v3, v3))
    v3 *= len3

    v1 = np.abs(v1)
    v2 = np.abs(v2)
    v3 = np.abs(v3)

    error_x = max([v1[0], v2[0], v3[0]])
    error_y = max([v1[1], v2[1], v3[1]])
    error_z = max([v1[2], v2[2], v3[2]])
    
    return (error_x, error_y, error_z)

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

def coords2azbazinc(stream, origin):
    """
    Returns azimuth, backazimuth and incidence angle from station coordinates
    given in first trace of stream and from event location specified in origin
    dictionary.
    """
    sta_coords = stream[0].stats.coordinates
    dist, bazim, azim = gps2DistAzimuth(sta_coords.latitude,
            sta_coords.longitude, origin['Latitude'], origin['Longitude'])
    elev_diff = sta_coords.elevation - origin['Depth'] * 1000
    inci = math.atan2(dist, elev_diff) * 180.0 / math.pi
    return azim, bazim, inci

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
    """ ищем записи """
    try:
        cursor.execute(QUERY, tuple(params,))
    except psycopg2.Error, msg:
        print("An error ocured while executing query:", msg)
        #return []
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
        # digits after point
        precision=3
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
