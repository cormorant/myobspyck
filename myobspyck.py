#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------
__version__="0.0.1"
COMPANY_NAME = 'GIN'
APP_NAME = 'pyck'
#---------------------------------------------------------------------

import os
import sys

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QEvent, Qt
from PyQt4.QtCore import QVariant, QString, QSize

import numpy as np

import matplotlib.pyplot as plt
import matplotlib.cm
import matplotlib.transforms
from matplotlib.patches import Ellipse
from matplotlib.ticker import FuncFormatter, FormatStrFormatter, MaxNLocator
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as QNavigationToolbar
from matplotlib.backend_bases import MouseEvent as MplMouseEvent, KeyEvent as MplKeyEvent

from qt_design_short import Ui_qMainWindow_obsPyck

from baikal import *#MyDictClass


PHASE_COLORS = {
    'P': "red", 'S': "blue",
    #'PErr1': "red", 'PErr2': "red", 'SErr1': "blue", 'SErr2': "blue"
}
SEISMIC_PHASES = ('P', 'S')


class SplitWriter():
    """ Implements a write method that writes a given message on all children """
    def __init__(self, *objects):
        """ Remember provided objects as children """
        self.children = objects
    def write(self, msg):
        """ Sends msg to all childrens write method """
        for obj in self.children:
            if isinstance(obj, PyQt4.QtGui.QPlainTextEdit):
                if msg == '\n':
                    return
                obj.appendPlainText(msg)
            else:
                obj.write(msg)


class ObsPyck(QtGui.QMainWindow):
    """ Main Window with the design loaded from the Qt Designer """
    def __init__(self, *args):
        """ initialization """
        # init the GUI stuff
        QtGui.QMainWindow.__init__(self)
        # All GUI elements will be accessible via self.widgets.name_of_element
        self.widgets = Ui_qMainWindow_obsPyck()
        self.widgets.setupUi(self)
        # Create little color icons in front of the phase type combo box.
        # Needs to be done pretty much at the beginning because some other
        # stuff relies on the phase type being set.
        pixmap = QtGui.QPixmap(70, 50)
        for phase_type in SEISMIC_PHASES:
            rgb = matplotlib_color_to_rgb(PHASE_COLORS[phase_type])
            pixmap.fill(QtGui.QColor(*rgb))
            icon = QtGui.QIcon(pixmap)
            self.widgets.qComboBox_phaseType.addItem(icon, phase_type)
        #
        self.qMain = self.widgets.centralwidget
        # Add write methods to stdout/stderr text edits in GUI displays to
        # enable redirections for stdout and stderr.
        self.stdout_backup = sys.stdout
        self.stderr_backup = sys.stderr
        # We automatically redirect all messages to both console and Gui boxes
        sys.stdout = SplitWriter(sys.stdout, self.widgets.qPlainTextEdit_stdout)
        sys.stderr = SplitWriter(sys.stderr, self.widgets.qPlainTextEdit_stderr)
        #=== Matplotlib figure.
        # we bind the figure to the FigureCanvas, so that it will be
        # drawn using the specific backend graphic functions
        self.canv = self.widgets.qMplCanvas
        # We have to reset all splitters such that the widget with the canvas
        # in it can not be collapsed as this leads to a crash of the program
        _i = self.widgets.qSplitter_vertical.indexOf(self.widgets.qSplitter_horizontal)
        self.widgets.qSplitter_vertical.setCollapsible(_i, False)
        _i = self.widgets.qSplitter_horizontal.indexOf(self.widgets.qWidget_mpl)
        self.widgets.qSplitter_horizontal.setCollapsible(_i, False)
        # XXX this resizing operation (buttons minimum size) should be done in
        # XXX the qt_designer.ui but I didn't find the correct settings there..
        self.widgets.qSplitter_horizontal.setSizes([1, 9999])
        # Bind the canvas to the mouse wheel event. Use Qt events for it
        # because the matplotlib events seem to have a problem with Debian.
        self.widgets.qMplCanvas.wheelEvent = self.__mpl_wheelEvent
        #self.keyPressEvent = self.__mpl_keyPressEvent
        #
        self.fig = self.widgets.qMplCanvas.fig
        facecolor = self.qMain.palette().color(QtGui.QPalette.Window).getRgb()
        self.fig.set_facecolor([value / 255.0 for value in facecolor])
        #
        #Define some flags, dictionaries and plotting options
        #this next flag indicates if we zoom on time or amplitude axis
        self.flagWheelZoomAmplitude = False
        #
        self.dictOrigin = {}
        self.dictEvent = {}
        # set up dictionaries to store phase_type/axes/line informations
        self.lines = {}
        self.texts = {}
        #
        self.dicts = dicts
        # Define a pointer to navigate through the streams
        self.stNum = len(streams)
        self.stPt = 0
        #
        self.drawAxes()
        self.multicursor = MultiCursor(self.canv, self.axs, useblit=True,
            color='k', linewidth=1.5, ls='dotted')
        #=== mpl connect
        # Activate all mouse/key/Cursor-events
        #self.canv.mpl_connect('key_press_event', self.__mpl_keyPressEvent)
        #self.canv.mpl_connect('key_release_event', self.__mpl_keyReleaseEvent)
        self.canv.mpl_connect('button_release_event', self.__mpl_mouseButtonReleaseEvent)
        # The scroll event is handled using Qt.
        #self.canv.mpl_connect('scroll_event', self.__mpl_wheelEvent)
        self.canv.mpl_connect('button_press_event', self.__mpl_mouseButtonPressEvent)
        self.canv.mpl_connect('motion_notify_event', self.__mpl_motionNotifyEvent)
        self.multicursorReinit()
        self.canv.show()
        self.showMaximized()
        # XXX XXX the good old focus issue again!?! no events get to the mpl canvas
        # XXX self.canv.setFocusPolicy(Qt.WheelFocus)
        #print self.canv.hasFocus()
        #
        #
        self.settings = QtCore.QSettings(COMPANY_NAME, APP_NAME)
        #self.setWindowTitle('pyck (v. %s)' % __version__)
        size = self.settings.value("MainWindow/Size", QVariant(QSize(800, 600))).toSize()
        self.resize(size)
        #
        # connect own button and menu clicks
        self.connect(self.widgets.exit_action, QtCore.SIGNAL("triggered()"), self.close)
        self.connect(self.widgets.open_action, QtCore.SIGNAL("triggered()"), self.open_file)

    def multicursorReinit(self):
        """ matplotlib.sourcearchive.com/documentation/0.98.1/widgets_8py-source.html """
        self.canv.mpl_disconnect(self.multicursor.id1)
        self.canv.mpl_disconnect(self.multicursor.id2)
        self.multicursor.__init__(self.canv, self.axs, useblit=True,
            color='black', linewidth=1, ls='dotted')
        self.updateMulticursorColor()

    # Define zooming for the mouse wheel wheel
    def __mpl_wheelEvent(self, ev):
        """ an exelent function for zooming """
        # create mpl event from QEvent to get cursor position in data coords
        x = ev.x()
        y = self.canv.height() - ev.y()
        mpl_ev = MplMouseEvent("scroll_event", self.canv, x, y, "up", guiEvent=ev)
        # Calculate and set new axes boundaries from old ones
        ax = self.axs[0]
        (left, right) = ax.get_xbound()
        (bottom, top) = ax.get_ybound()
        # Get the keyboard modifiers. They are a enum type.
        # Use bitwise or to compare...hope this is correct.
        if ev.modifiers() == QtCore.Qt.NoModifier:
            # Zoom in.
            if ev.delta() < 0:
                left -= (mpl_ev.xdata - left) / 2
                right += (right - mpl_ev.xdata) / 2
                if self.widgets.qToolButton_showMap.isChecked():
                    top -= (mpl_ev.ydata - top) / 2
                    bottom += (bottom - mpl_ev.ydata) / 2
            # Zoom out.
            elif ev.delta() > 0:
                left += (mpl_ev.xdata - left) / 2
                right -= (right - mpl_ev.xdata) / 2
                if self.widgets.qToolButton_showMap.isChecked():
                    top += (mpl_ev.ydata - top) / 2
                    bottom -= (bottom - mpl_ev.ydata) / 2
        # Still able to use the dictionary.
        elif ev.modifiers() == getattr(QtCore.Qt,
            '%sModifier' % self.keys['switchWheelZoomAxis'].capitalize()):
            # Zoom in on wheel-up
            if ev.delta() < 0:
                top *= 2
                bottom *= 2
            # Zoom out on wheel-down
            elif ev.delta() > 0:
                top /= 2
                bottom /= 2
        ax.set_xbound(lower=left, upper=right)
        ax.set_ybound(lower=bottom, upper=top)
        self.redraw()

    def redraw(self):
        for line in self.multicursor.lines:
            line.set_visible(False)
        self.canv.draw()

    def __mpl_mouseButtonPressEvent(self, ev):
        # set widgetlock when pressing mouse buttons and dont show cursor
        # cursor should not be plotted when making a zoom selection etc.
        if ev.button in [1, 3]:
            self.multicursor.visible = False
            self.__mpl_keyPressEvent(ev)
        elif ev.button == 2:
            ax = self.axs[0]
            ax.set_xbound(lower=self.xMin, upper=self.xMax)
            ax.set_ybound(lower=self.yMin, upper=self.yMax)
            # Update all subplots
            self.redraw()
            print "Resetting axes"
    
    def __mpl_mouseButtonReleaseEvent(self, ev):
        # release widgetlock when releasing mouse buttons
        if ev.button in [1, 3]:
            self.multicursor.visible = True

    def __mpl_motionNotifyEvent(self, ev):
        try:
            if ev.inaxes in self.axs:
                self.widgets.qLabel_xdata_rel.setText(formatXTicklabels(ev.xdata))
                label = self.time_rel2abs(ev.xdata).isoformat().replace("T", "  ")[:-3]
                self.widgets.qLabel_xdata_abs.setText(label)
                self.widgets.qLabel_ydata.setText("%.1f" % ev.ydata)
            else:
                self.widgets.qLabel_xdata_rel.setText("")
                self.widgets.qLabel_xdata_abs.setText(str(ev.xdata))
                self.widgets.qLabel_ydata.setText(str(ev.ydata))
        except TypeError:
            pass

    def __mpl_keyPressEvent(self, ev):
        phase_type = str(self.widgets.qComboBox_phaseType.currentText())
        dict = self.dicts[self.stPt]
        st = self.streams[self.stPt]
        tr = st[self.axs.index(ev.inaxes)]
        #######################################################################
        # Start of key events related to picking                              #
        #######################################################################
        # For some key events (picking events) we need information on the x/y
        # position of the cursor:
        if ev.key in [keys['setPick'], keys['setPickError'],
                      keys['setMagMin'], keys['setMagMax']]:
            # some keyPress events only make sense inside our matplotlib axes
            if ev.inaxes not in self.axs:
                return
            # get the correct sample times array for the click
            t = self.t[self.axs.index(ev.inaxes)]
            # We want to round from the picking location to
            # the time value of the nearest sample:
            samp_rate = st[0].stats.sampling_rate
            pickSample = (ev.xdata - t[0]) * samp_rate
            print pickSample
            pickSample = round(pickSample)
            print pickSample
            # we need the position of the cursor location
            # in the seismogram array:
            xpos = pickSample
            # Determine the time of the nearest sample
            pickSample = t[pickSample]
            print pickSample
            print ev.inaxes.lines[0].get_ydata()[xpos]

        if ev.key == keys['setPick']:
            # some keyPress events only make sense inside our matplotlib axes
            if not ev.inaxes in self.axs:
                return
            if phase_type in SEISMIC_PHASES:
                dict[phase_type] = pickSample
                if phase_type == "S":
                    dict['Saxind'] = self.axs.index(ev.inaxes)
                depending_keys = (phase_type + k for k in ['', 'synth'])
                for key in depending_keys:
                    self.updateLine(key)
                    self.updateLabel(key)
                #check if the new P pick lies outside of the Error Picks
                key1 = phase_type + "Err1"
                key2 = phase_type + "Err2"
                if key1 in dict and dict[phase_type] < dict[key1]:
                    self.delLine(key1)
                    self.delKey(key1)
                if key2 in dict and dict[phase_type] > dict[key2]:
                    self.delLine(key2)
                    self.delKey(key2)
                self.redraw()
                abs_time = self.time_rel2abs(dict[phase_type])
                print "%s set at %.3f (%s)" % (KEY_FULLNAMES[phase_type],
                    dict[phase_type], abs_time.isoformat())
                return
