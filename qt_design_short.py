# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt_design_short.ui'
#
# Created: Thu Jan 24 10:48:04 2013
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_qMainWindow_obsPyck(object):
    def setupUi(self, qMainWindow_obsPyck):
        qMainWindow_obsPyck.setObjectName(_fromUtf8("qMainWindow_obsPyck"))
        qMainWindow_obsPyck.resize(1325, 756)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(qMainWindow_obsPyck.sizePolicy().hasHeightForWidth())
        qMainWindow_obsPyck.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(11)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        qMainWindow_obsPyck.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("obspyck.gif")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        qMainWindow_obsPyck.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(qMainWindow_obsPyck)
        self.centralwidget.setMouseTracking(True)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.qSplitter_vertical = QtGui.QSplitter(self.centralwidget)
        self.qSplitter_vertical.setOrientation(QtCore.Qt.Vertical)
        self.qSplitter_vertical.setHandleWidth(8)
        self.qSplitter_vertical.setObjectName(_fromUtf8("qSplitter_vertical"))
        self.qSplitter_horizontal = QtGui.QSplitter(self.qSplitter_vertical)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.qSplitter_horizontal.sizePolicy().hasHeightForWidth())
        self.qSplitter_horizontal.setSizePolicy(sizePolicy)
        self.qSplitter_horizontal.setFrameShape(QtGui.QFrame.NoFrame)
        self.qSplitter_horizontal.setFrameShadow(QtGui.QFrame.Plain)
        self.qSplitter_horizontal.setOrientation(QtCore.Qt.Horizontal)
        self.qSplitter_horizontal.setHandleWidth(8)
        self.qSplitter_horizontal.setObjectName(_fromUtf8("qSplitter_horizontal"))
        self.qWidget_mpl = QtGui.QWidget(self.qSplitter_horizontal)
        self.qWidget_mpl.setObjectName(_fromUtf8("qWidget_mpl"))
        self.qVBoxLayout_mpl = QtGui.QVBoxLayout(self.qWidget_mpl)
        self.qVBoxLayout_mpl.setMargin(0)
        self.qVBoxLayout_mpl.setObjectName(_fromUtf8("qVBoxLayout_mpl"))
        self.qMplCanvas = QMplCanvas(self.qWidget_mpl)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(99)
        sizePolicy.setVerticalStretch(99)
        sizePolicy.setHeightForWidth(self.qMplCanvas.sizePolicy().hasHeightForWidth())
        self.qMplCanvas.setSizePolicy(sizePolicy)
        self.qMplCanvas.setCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        self.qMplCanvas.setMouseTracking(True)
        self.qMplCanvas.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.qMplCanvas.setObjectName(_fromUtf8("qMplCanvas"))
        self.qVBoxLayout_mpl.addWidget(self.qMplCanvas)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.VerticalLayout = QtGui.QVBoxLayout()
        self.VerticalLayout.setSpacing(6)
        self.VerticalLayout.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.VerticalLayout.setContentsMargins(-1, 0, -1, -1)
        self.VerticalLayout.setObjectName(_fromUtf8("VerticalLayout"))
        self.horizontalLayout_13 = QtGui.QHBoxLayout()
        self.horizontalLayout_13.setObjectName(_fromUtf8("horizontalLayout_13"))
        self.qToolButton_previousStream = QtGui.QToolButton(self.qWidget_mpl)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.qToolButton_previousStream.sizePolicy().hasHeightForWidth())
        self.qToolButton_previousStream.setSizePolicy(sizePolicy)
        self.qToolButton_previousStream.setFocusPolicy(QtCore.Qt.NoFocus)
        self.qToolButton_previousStream.setArrowType(QtCore.Qt.LeftArrow)
        self.qToolButton_previousStream.setObjectName(_fromUtf8("qToolButton_previousStream"))
        self.horizontalLayout_13.addWidget(self.qToolButton_previousStream)
        self.qLabel_streamNumber = QtGui.QLabel(self.qWidget_mpl)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.qLabel_streamNumber.sizePolicy().hasHeightForWidth())
        self.qLabel_streamNumber.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Monospace"))
        self.qLabel_streamNumber.setFont(font)
        self.qLabel_streamNumber.setStyleSheet(_fromUtf8(""))
        self.qLabel_streamNumber.setAlignment(QtCore.Qt.AlignCenter)
        self.qLabel_streamNumber.setObjectName(_fromUtf8("qLabel_streamNumber"))
        self.horizontalLayout_13.addWidget(self.qLabel_streamNumber)
        self.qToolButton_nextStream = QtGui.QToolButton(self.qWidget_mpl)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.qToolButton_nextStream.sizePolicy().hasHeightForWidth())
        self.qToolButton_nextStream.setSizePolicy(sizePolicy)
        self.qToolButton_nextStream.setFocusPolicy(QtCore.Qt.NoFocus)
        self.qToolButton_nextStream.setArrowType(QtCore.Qt.RightArrow)
        self.qToolButton_nextStream.setObjectName(_fromUtf8("qToolButton_nextStream"))
        self.horizontalLayout_13.addWidget(self.qToolButton_nextStream)
        self.VerticalLayout.addLayout(self.horizontalLayout_13)
        self.qComboBox_streamName = QtGui.QComboBox(self.qWidget_mpl)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.qComboBox_streamName.sizePolicy().hasHeightForWidth())
        self.qComboBox_streamName.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Monospace"))
        self.qComboBox_streamName.setFont(font)
        self.qComboBox_streamName.setFocusPolicy(QtCore.Qt.NoFocus)
        self.qComboBox_streamName.setStyleSheet(_fromUtf8(""))
        self.qComboBox_streamName.setObjectName(_fromUtf8("qComboBox_streamName"))
        self.VerticalLayout.addWidget(self.qComboBox_streamName)
        self.horizontalLayout_6.addLayout(self.VerticalLayout)
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.qToolButton_overview = QtGui.QToolButton(self.qWidget_mpl)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.qToolButton_overview.sizePolicy().hasHeightForWidth())
        self.qToolButton_overview.setSizePolicy(sizePolicy)
        self.qToolButton_overview.setFocusPolicy(QtCore.Qt.NoFocus)
        self.qToolButton_overview.setCheckable(True)
        self.qToolButton_overview.setObjectName(_fromUtf8("qToolButton_overview"))
        self.verticalLayout_3.addWidget(self.qToolButton_overview)
        self.qComboBox_phaseType = QtGui.QComboBox(self.qWidget_mpl)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.qComboBox_phaseType.sizePolicy().hasHeightForWidth())
        self.qComboBox_phaseType.setSizePolicy(sizePolicy)
        self.qComboBox_phaseType.setFocusPolicy(QtCore.Qt.NoFocus)
        self.qComboBox_phaseType.setObjectName(_fromUtf8("qComboBox_phaseType"))
        self.verticalLayout_3.addWidget(self.qComboBox_phaseType)
        self.horizontalLayout_6.addLayout(self.verticalLayout_3)
        self.horizontalLayout_2.addLayout(self.horizontalLayout_6)
        self.verticalLayout_7 = QtGui.QVBoxLayout()
        self.verticalLayout_7.setObjectName(_fromUtf8("verticalLayout_7"))
        self.horizontalLayout_18 = QtGui.QHBoxLayout()
        self.horizontalLayout_18.setObjectName(_fromUtf8("horizontalLayout_18"))
        self.qToolButton_clearAll = QtGui.QToolButton(self.qWidget_mpl)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.qToolButton_clearAll.sizePolicy().hasHeightForWidth())
        self.qToolButton_clearAll.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setKerning(True)
        self.qToolButton_clearAll.setFont(font)
        self.qToolButton_clearAll.setFocusPolicy(QtCore.Qt.NoFocus)
        self.qToolButton_clearAll.setStyleSheet(_fromUtf8(""))
        self.qToolButton_clearAll.setCheckable(False)
        self.qToolButton_clearAll.setObjectName(_fromUtf8("qToolButton_clearAll"))
        self.horizontalLayout_18.addWidget(self.qToolButton_clearAll)
        self.verticalLayout_7.addLayout(self.horizontalLayout_18)
        self.horizontalLayout_19 = QtGui.QHBoxLayout()
        self.horizontalLayout_19.setObjectName(_fromUtf8("horizontalLayout_19"))
        self.qToolButton_debug = QtGui.QToolButton(self.qWidget_mpl)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.qToolButton_debug.sizePolicy().hasHeightForWidth())
        self.qToolButton_debug.setSizePolicy(sizePolicy)
        self.qToolButton_debug.setFocusPolicy(QtCore.Qt.NoFocus)
        self.qToolButton_debug.setObjectName(_fromUtf8("qToolButton_debug"))
        self.horizontalLayout_19.addWidget(self.qToolButton_debug)
        self.verticalLayout_7.addLayout(self.horizontalLayout_19)
        self.horizontalLayout_2.addLayout(self.verticalLayout_7)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout_9 = QtGui.QHBoxLayout()
        self.horizontalLayout_9.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.horizontalLayout_9.setObjectName(_fromUtf8("horizontalLayout_9"))
        self.horizontalLayout_8 = QtGui.QHBoxLayout()
        self.horizontalLayout_8.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.horizontalLayout_8.setObjectName(_fromUtf8("horizontalLayout_8"))
        self.qLabel_x_rel = QtGui.QLabel(self.qWidget_mpl)
        self.qLabel_x_rel.setObjectName(_fromUtf8("qLabel_x_rel"))
        self.horizontalLayout_8.addWidget(self.qLabel_x_rel)
        self.qLabel_xdata_rel = QtGui.QLabel(self.qWidget_mpl)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(200)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.qLabel_xdata_rel.sizePolicy().hasHeightForWidth())
        self.qLabel_xdata_rel.setSizePolicy(sizePolicy)
        self.qLabel_xdata_rel.setMinimumSize(QtCore.QSize(50, 0))
        self.qLabel_xdata_rel.setBaseSize(QtCore.QSize(40, 0))
        self.qLabel_xdata_rel.setAutoFillBackground(False)
        self.qLabel_xdata_rel.setText(_fromUtf8(""))
        self.qLabel_xdata_rel.setObjectName(_fromUtf8("qLabel_xdata_rel"))
        self.horizontalLayout_8.addWidget(self.qLabel_xdata_rel)
        self.horizontalLayout_9.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        self.qLabel_y = QtGui.QLabel(self.qWidget_mpl)
        self.qLabel_y.setObjectName(_fromUtf8("qLabel_y"))
        self.horizontalLayout_7.addWidget(self.qLabel_y)
        self.qLabel_ydata = QtGui.QLabel(self.qWidget_mpl)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.qLabel_ydata.sizePolicy().hasHeightForWidth())
        self.qLabel_ydata.setSizePolicy(sizePolicy)
        self.qLabel_ydata.setMinimumSize(QtCore.QSize(25, 0))
        self.qLabel_ydata.setBaseSize(QtCore.QSize(40, 0))
        self.qLabel_ydata.setText(_fromUtf8(""))
        self.qLabel_ydata.setObjectName(_fromUtf8("qLabel_ydata"))
        self.horizontalLayout_7.addWidget(self.qLabel_ydata)
        self.horizontalLayout_9.addLayout(self.horizontalLayout_7)
        self.verticalLayout_2.addLayout(self.horizontalLayout_9)
        self.horizontalLayout_8b = QtGui.QHBoxLayout()
        self.horizontalLayout_8b.setObjectName(_fromUtf8("horizontalLayout_8b"))
        self.qLabel_x_abs = QtGui.QLabel(self.qWidget_mpl)
        self.qLabel_x_abs.setObjectName(_fromUtf8("qLabel_x_abs"))
        self.horizontalLayout_8b.addWidget(self.qLabel_x_abs)
        self.qLabel_xdata_abs = QtGui.QLabel(self.qWidget_mpl)
        self.qLabel_xdata_abs.setMinimumSize(QtCore.QSize(160, 0))
        self.qLabel_xdata_abs.setText(_fromUtf8(""))
        self.qLabel_xdata_abs.setObjectName(_fromUtf8("qLabel_xdata_abs"))
        self.horizontalLayout_8b.addWidget(self.qLabel_xdata_abs)
        self.verticalLayout_2.addLayout(self.horizontalLayout_8b)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.qVBoxLayout_mpl.addLayout(self.horizontalLayout_2)
        self.layoutWidget = QtGui.QWidget(self.qSplitter_vertical)
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.qPlainTextEdit_stdout = QtGui.QPlainTextEdit(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.qPlainTextEdit_stdout.sizePolicy().hasHeightForWidth())
        self.qPlainTextEdit_stdout.setSizePolicy(sizePolicy)
        self.qPlainTextEdit_stdout.setMinimumSize(QtCore.QSize(0, 50))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Monospace"))
        font.setPointSize(10)
        self.qPlainTextEdit_stdout.setFont(font)
        self.qPlainTextEdit_stdout.setFocusPolicy(QtCore.Qt.NoFocus)
        self.qPlainTextEdit_stdout.setAcceptDrops(False)
        self.qPlainTextEdit_stdout.setUndoRedoEnabled(False)
        self.qPlainTextEdit_stdout.setReadOnly(True)
        self.qPlainTextEdit_stdout.setTextInteractionFlags(QtCore.Qt.TextBrowserInteraction)
        self.qPlainTextEdit_stdout.setObjectName(_fromUtf8("qPlainTextEdit_stdout"))
        self.horizontalLayout.addWidget(self.qPlainTextEdit_stdout)
        self.qPlainTextEdit_stderr = QtGui.QPlainTextEdit(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.qPlainTextEdit_stderr.sizePolicy().hasHeightForWidth())
        self.qPlainTextEdit_stderr.setSizePolicy(sizePolicy)
        self.qPlainTextEdit_stderr.setMinimumSize(QtCore.QSize(0, 50))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Monospace"))
        font.setPointSize(10)
        self.qPlainTextEdit_stderr.setFont(font)
        self.qPlainTextEdit_stderr.setFocusPolicy(QtCore.Qt.NoFocus)
        self.qPlainTextEdit_stderr.setAcceptDrops(False)
        self.qPlainTextEdit_stderr.setUndoRedoEnabled(False)
        self.qPlainTextEdit_stderr.setReadOnly(True)
        self.qPlainTextEdit_stderr.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.qPlainTextEdit_stderr.setObjectName(_fromUtf8("qPlainTextEdit_stderr"))
        self.horizontalLayout.addWidget(self.qPlainTextEdit_stderr)
        self.verticalLayout.addWidget(self.qSplitter_vertical)
        self.verticalLayout_4.addLayout(self.verticalLayout)
        qMainWindow_obsPyck.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(qMainWindow_obsPyck)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1325, 23))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menu = QtGui.QMenu(self.menubar)
        self.menu.setObjectName(_fromUtf8("menu"))
        self.menuAbout = QtGui.QMenu(self.menubar)
        self.menuAbout.setObjectName(_fromUtf8("menuAbout"))
        qMainWindow_obsPyck.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(qMainWindow_obsPyck)
        self.statusbar.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statusbar.sizePolicy().hasHeightForWidth())
        self.statusbar.setSizePolicy(sizePolicy)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        qMainWindow_obsPyck.setStatusBar(self.statusbar)
        self.open_action = QtGui.QAction(qMainWindow_obsPyck)
        self.open_action.setObjectName(_fromUtf8("open_action"))
        self.exit_action = QtGui.QAction(qMainWindow_obsPyck)
        self.exit_action.setShortcutContext(QtCore.Qt.WidgetShortcut)
        self.exit_action.setMenuRole(QtGui.QAction.QuitRole)
        self.exit_action.setObjectName(_fromUtf8("exit_action"))
        self.action_5 = QtGui.QAction(qMainWindow_obsPyck)
        self.action_5.setObjectName(_fromUtf8("action_5"))
        self.action_6 = QtGui.QAction(qMainWindow_obsPyck)
        self.action_6.setMenuRole(QtGui.QAction.AboutRole)
        self.action_6.setObjectName(_fromUtf8("action_6"))
        self.menu.addAction(self.open_action)
        self.menu.addSeparator()
        self.menu.addAction(self.exit_action)
        self.menuAbout.addAction(self.action_5)
        self.menuAbout.addAction(self.action_6)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())

        self.retranslateUi(qMainWindow_obsPyck)
        QtCore.QMetaObject.connectSlotsByName(qMainWindow_obsPyck)

    def retranslateUi(self, qMainWindow_obsPyck):
        qMainWindow_obsPyck.setWindowTitle(QtGui.QApplication.translate("qMainWindow_obsPyck", "ObsPyck", None, QtGui.QApplication.UnicodeUTF8))
        self.qToolButton_previousStream.setText(QtGui.QApplication.translate("qMainWindow_obsPyck", "<", None, QtGui.QApplication.UnicodeUTF8))
        self.qLabel_streamNumber.setText(QtGui.QApplication.translate("qMainWindow_obsPyck", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<  html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, l  i { white-space: pre-wrap; }\n"
"<  /style></head><body style=\" font-family:\'Monospace\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<  p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">00/00</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.qToolButton_nextStream.setText(QtGui.QApplication.translate("qMainWindow_obsPyck", ">", None, QtGui.QApplication.UnicodeUTF8))
        self.qToolButton_overview.setText(QtGui.QApplication.translate("qMainWindow_obsPyck", "Просмотр", None, QtGui.QApplication.UnicodeUTF8))
        self.qToolButton_clearAll.setText(QtGui.QApplication.translate("qMainWindow_obsPyck", "очистить", None, QtGui.QApplication.UnicodeUTF8))
        self.qToolButton_debug.setText(QtGui.QApplication.translate("qMainWindow_obsPyck", "debug", None, QtGui.QApplication.UnicodeUTF8))
        self.qLabel_x_rel.setText(QtGui.QApplication.translate("qMainWindow_obsPyck", "x (rel):", None, QtGui.QApplication.UnicodeUTF8))
        self.qLabel_y.setText(QtGui.QApplication.translate("qMainWindow_obsPyck", "y:", None, QtGui.QApplication.UnicodeUTF8))
        self.qLabel_x_abs.setText(QtGui.QApplication.translate("qMainWindow_obsPyck", "x:", None, QtGui.QApplication.UnicodeUTF8))
        self.menu.setTitle(QtGui.QApplication.translate("qMainWindow_obsPyck", "Файл", None, QtGui.QApplication.UnicodeUTF8))
        self.menuAbout.setTitle(QtGui.QApplication.translate("qMainWindow_obsPyck", "About", None, QtGui.QApplication.UnicodeUTF8))
        self.open_action.setText(QtGui.QApplication.translate("qMainWindow_obsPyck", "Открыть", None, QtGui.QApplication.UnicodeUTF8))
        self.exit_action.setText(QtGui.QApplication.translate("qMainWindow_obsPyck", "Выход", None, QtGui.QApplication.UnicodeUTF8))
        self.action_5.setText(QtGui.QApplication.translate("qMainWindow_obsPyck", "Помощь", None, QtGui.QApplication.UnicodeUTF8))
        self.action_6.setText(QtGui.QApplication.translate("qMainWindow_obsPyck", "О программе", None, QtGui.QApplication.UnicodeUTF8))

from util import QMplCanvas
