#!/usr/bin/python3
# -*- coding: utf-8 -*-


import sys
import parse
import re
import os
import datetime
import telnetlib
import internetworker
import time

# import pyautogui

# import xdo  # $ pip install  python-libxdo
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QAction, QTableWidget, QTableWidgetItem, QTextEdit, \
    QLineEdit, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QComboBox
from PyQt5.QtCore import pyqtSignal, QObject, QEvent
from PyQt5.QtGui import QIcon, QFocusEvent, QPixmap
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QThread
from time import gmtime, strftime, localtime


# from tel import telnet_cluster

'''if os.name == 'posix':
    from subprocess import check_output
elif os.name == 'nt':
    import win32api, win32con, win32process
    from ctypes import windll

    user32 = windll.user32
'''
APP_VERSION = '0.1 Beta pre release'
settingsDict = {}
file = open('settings.cfg', "r")
for configstring in file:
    if configstring != '' and configstring != ' ' and configstring[0] != '#':
        configstring = configstring.strip()
        configstring = configstring.replace("\r", "")
        configstring = configstring.replace("\n", "")
        splitString = configstring.split('=')
        settingsDict.update({splitString[0]: splitString[1]})

file.close()
print(settingsDict)

class Adi_file:

    def __init__(self):

        self.filename = 'log.adi'

    def get_header(self):

        '''
        This function returned string with cariage return
        :return: string header with cariage return
        '''

        self.header_string="ADIF from LinLog Light v."+APP_VERSION+" \n"
        self.header_string +="Copyright 2019-"+strftime("%Y", gmtime())+"  Baston V. Sergey\n"
        self.header_string +="Header generated on "+strftime("%d/%m/%y %H:%M:%S", gmtime())+" by "+settingsDict['my-call']+"\n"
        self.header_string +="File output restricted to QSOs by : All Operators - All Bands - All Modes \n"
        self.header_string +="<PROGRAMID:6>LinLog\n"
        self.header_string += "<PROGRAMVERSION:"+str(len(APP_VERSION))+">"+APP_VERSION+"\n"
        self.header_string += "<EOH>\n\n"
        return self.header_string

    def get_all_qso(self):
        try:
            with  open(self.filename, 'r') as file:
                lines = file.readlines()
                print (lines)
        except Exception:
            print ("Adi_file: Exception. Don't open or read"+self.filename)

    def record_all_qso (self, list_data):
        '''
        This function recieve List (list_data) with Dictionary with QSO-data
        Dictionary including:
        call
        name
        qth
        rst_send
        rst_reciev
        band
        mode
        comment
        :param list_data: List with Dictionary with QSO-data
        :return:
        '''
        print(list_data[0]['call'])
        #header = self.get_header()
        #with open('aditest.adi', 'w') as file:
          #  file.writelines(header)
            #file.writelines(list_data)







class Filter(QObject):

    previous_call=''
    def eventFilter(self, widget, event):
        # FocusOut event
        #print(widget)

        if event.type() == QEvent.FocusOut:
                # do custom stuff
                text = logForm
                textCall = text.inputCall.text()
                foundList = self.searchInBase(textCall)
                logSearch.overlap(foundList)
                if textCall != '' and textCall != Filter.previous_call:
                    if settingsDict['search-internet-window'] == 'true':
                        print("textCall", textCall)
                        Filter.previous_call = textCall
                        self.isearch = internetworker.internetWorker(window=internetSearch, callsign=textCall, settings=settingsDict)
                        self.isearch.start()
                if textCall == '' or textCall == ' ':
                    pixmap = QPixmap('logo-big.png')
                    #pixmap_resized = pixmap.scaled(int(settingsDict['image-width']),
                                                 #  int(settingsDict['image-height']),
                                                 #  QtCore.Qt.KeepAspectRatio)
                    internetSearch.labelImage.setPixmap(pixmap)
                    #print(img)


                # print ('focus out')
                return False

        if event.type() == QEvent.FocusIn:
                # do custom stuff
                logForm.inputRstS.setText('59')
                logForm.inputRstR.setText('59')
                # return False so that the widget will also handle the event
                # otherwise it won't focus out
                return False
        else:
                # we don't care about other events
                return False

    def searchInBase(self, call):
        # print (logWindow.allRecord)
        foundList = []  # create empty list for result list
        lenRecords = len(logWindow.allRecord)  # get count all Records
        for counter in range(lenRecords):  # start cicle where chek all elements at equivivalent at input call
            if logWindow.allRecord[counter]['CALL'].strip() == call.strip():
                foundList.append(logWindow.allRecord[counter])

        return foundList
        # print (foundList)
        #


class logWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.filename = "log.adi"
        self.allCollumn = ['QSO_DATE', 'TIME_ON', 'BAND', 'CALL', 'MODE', 'RST_RCVD', 'RST_SENT', 'NAME', 'QTH']
        self.allRecord = parse.getAllRecord(self.allCollumn, self.filename)
        self.initUI()

    def initUI(self):

        self.setGeometry(int(settingsDict['log-window-left']),
                         int(settingsDict['log-window-top']),
                         int(settingsDict['log-window-width']),
                         int(settingsDict['log-window-height']))
        self.setWindowTitle('LinLog | All QSO')
        self.setWindowIcon(QIcon('logo.png'))
        style = "QWidget{background-color:" + settingsDict['background-color'] + "; color:" + settingsDict[
            'color'] + ";}"
        self.setStyleSheet(style)

        self.allRows = len(self.allRecord)
        allCols = len(self.allCollumn)
        # print ('%10s %5s %10s %16s %8s %8s %8s %15s %15s' % ('QSO_DATE', 'TIME', 'FREQ', 'CALL',
        #			'MODE', 'RST_RCVD', 'RST_SENT',	'NAME', 'QTH')
        #		   )
        self.tableWidget = QTableWidget()
        fnt = self.tableWidget.font()
        fnt.setPointSize(8)
        self.tableWidget.setSortingEnabled(True)
        self.tableWidget.setFont(fnt)
        self.tableWidget.setRowCount(self.allRows)
        self.tableWidget.setColumnCount(9)
        self.tableWidget.setHorizontalHeaderLabels(["   Date   ", " Time ", "Band", "   Call   ", "Mode", "RST r",
                                                    "RST s", "      Name      ", "      QTH      "])
        self.tableWidget.resizeColumnsToContents()

        self.tableWidget.resizeRowsToContents()
        # self.tableWidget.resizeColsToContents()
        for row in range(self.allRows):
            for col in range(allCols):
                pole = self.allCollumn[col]
                if self.allRecord[row][pole] != ' ' or self.allRecord[row][pole] != '':
                    self.tableWidget.setItem(row, col, QTableWidgetItem(self.allRecord[row][pole]))
                #  print(self.allRecord[row][pole])

        self.tableWidget.move(0, 0)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tableWidget)
        self.setLayout(self.layout)

        #
        logForm.test('test')
        self.show()

    def addRecord(self, recordObject):
        # <BAND:3>20M <CALL:6>DL1BCL <FREQ:9>14.000000
        # <MODE:3>SSB <OPERATOR:6>UR4LGA <PFX:3>DL1 <QSLMSG:19>TNX For QSO TU 73!.
        # <QSO_DATE:8:D>20131011 <TIME_ON:6>184700 <RST_RCVD:2>57 <RST_SENT:2>57 <TIME_OFF:6>184700
        # <eQSL_QSL_RCVD:1>Y <APP_LOGGER32_QSO_NUMBER:1>1  <EOR>
        # record to file
        stringToAdiFile = "<BAND:" + str(len(recordObject['BAND'])) + ">" + recordObject['BAND'] + "<CALL:" + str(
            len(recordObject['CALL'])) + ">"

        stringToAdiFile = stringToAdiFile + recordObject['CALL'] + "<FREQ:" + str(len(recordObject['FREQ'])) + ">" + \
                          recordObject['FREQ']
        stringToAdiFile = stringToAdiFile + "<MODE:" + str(len(recordObject['MODE'])) + ">" + recordObject[
            'MODE'] + "<OPERATOR:" + str(len(recordObject['OPERATOR']))
        stringToAdiFile = stringToAdiFile + ">" + recordObject['OPERATOR'] + "<QSO_DATE:" + str(
            len(recordObject['QSO_DATE'])) + ">"
        stringToAdiFile = stringToAdiFile + recordObject['QSO_DATE'] + "<TIME_ON:" + str(
            len(recordObject['TIME_ON'])) + ">"
        stringToAdiFile = stringToAdiFile + recordObject['TIME_ON'] + "<RST_RCVD:" + str(
            len(recordObject['RST_RCVD'])) + ">" + recordObject['RST_RCVD']
        stringToAdiFile = stringToAdiFile + "<RST_SENT:" + str(len(recordObject['RST_SENT'])) + ">" + recordObject[
            'RST_SENT'] + "<NAME:" + str(
            len(recordObject['NAME'])) + ">" + recordObject['NAME'] + "<QTH:" + str(
            len(recordObject['QTH'])) + ">" + recordObject['QTH'] + "<COMMENTS:" + str(
            len(recordObject['COMMENTS'])) + ">" + recordObject[
                              'COMMENTS'] + "<TIME_OFF:6>000000<eQSL_QSL_RCVD:1>Y<EOR>\n\n"
        # print(stringToAdiFile)
        file = open(self.filename, 'a')
        resultWrite = file.write(stringToAdiFile)
        # print(resultWrite)
        if resultWrite > 0:
            file.close()
        else:
            print("QSO not write in logfile")
        #####

        # record to allRecord
        self.allRecord.append(recordObject)

        # record to table
        allCols = len(self.allCollumn)
        row = self.allRows + 1
        # print(recordObject)
        # print (row)
        self.tableWidget.setRowCount(row)
        self.tableWidget.insertRow(0)
        self.tableWidget.resizeRowsToContents()
        #
        for col in range(allCols):
            pole = self.allCollumn[col]
            # print(self.allCollumn[col])
            self.tableWidget.setItem(0, col, QTableWidgetItem(recordObject[self.allCollumn[col]]))
        # print (recordObject)


class logSearch(QWidget):
    def __init__(self):
        super().__init__()
        self.foundList = []
        self.initUI()

    def initUI(self):

        self.setGeometry(int(settingsDict['log-search-window-left']), int(settingsDict['log-search-window-top']),
                         int(settingsDict['log-search-window-width']), int(settingsDict['log-search-window-height']))
        self.setWindowTitle('LinLog | Search')
        self.setWindowIcon(QIcon('logo.png'))
        style = "QWidget{background-color:" + settingsDict['background-color'] + "; color:" + settingsDict[
            'color'] + ";}"
        self.setStyleSheet(style)

        # print ('%10s %5s %10s %16s %8s %8s %8s %15s %15s' % ('QSO_DATE', 'TIME', 'FREQ', 'CALL',
        #			'MODE', 'RST_RCVD', 'RST_SENT',	'NAME', 'QTH')
        #		   )
        self.tableWidget = QTableWidget()
        fnt = self.tableWidget.font()
        fnt.setPointSize(8)
        self.tableWidget.setSortingEnabled(True)
        self.tableWidget.setFont(fnt)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tableWidget)
        self.setLayout(self.layout)
        self.show()

    def overlap(self, foundList):
        allRows = len(foundList)
        # print(foundList)
        self.tableWidget.setRowCount(allRows)
        self.tableWidget.setColumnCount(9)
        self.tableWidget.setHorizontalHeaderLabels(["   Date   ", " Time ", "Band", "   Call   ", "Mode", "RST r",
                                                    "RST s", "      Name      ", "      QTH      "])
        self.tableWidget.resizeColumnsToContents()
        allCols = len(logWindow.allCollumn)
        # print(foundList[0]["CALL"])
        for row in range(allRows):
            for col in range(allCols):
                pole = logWindow.allCollumn[col]
                # print(foundList[row][pole])
                self.tableWidget.setItem(row, col, QTableWidgetItem(foundList[row][pole]))

        self.tableWidget.resizeRowsToContents()
        self.foundList = foundList
        # print(self.foundList)


class Communicate(QObject):
    closeApp = pyqtSignal()


class realTime(QThread):
    def __init__(self, logformwindow, parent=None):
        super().__init__()
        self.logformwindow = logformwindow


    def run(self):

        while 1:
            self.logformwindow.labelTime.setText("Loc: "+strftime("%H:%M:%S", localtime())+
                                                 "  |  GMT: "+strftime("%H:%M:%S", gmtime()))
            time.sleep(0.5)



class logForm(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def menu(self):
        '''
        logSettingsAction = QAction(QIcon('logo.png'), 'Log settings', self)
        logSettingsAction.setStatusTip('Name, Call and other of station')
        logSettingsAction.triggered.connect(self.logSettings)
        #
        catSettingsAction = QAction(QIcon('logo.png'), 'Cat settings', self)
        catSettingsAction.setStatusTip('Name, Call and other of station')
        catSettingsAction.triggered.connect(self.logSettings)
        #
        logWindowAction = QAction(QIcon('logo.png'), 'All log Window', self)
        logWindowAction.setStatusTip('Name, Call and other of station')
        logWindowAction.triggered.connect(self.logSettings)
        #
        searchWindowAction = QAction(QIcon('logo.png'), 'Search window', self)
        searchWindowAction.setStatusTip('Name, Call and other of station')
        searchWindowAction.triggered.connect(self.searchWindow)
        #
        importAdiAction = QAction(QIcon('logo.png'), 'Import ADI', self)
        importAdiAction.setStatusTip('Name, Call and other of station')
        importAdiAction.triggered.connect(self.logSettings)
        #
        exportAdiAction = QAction(QIcon('logo.png'), 'Export ADI', self)
        exportAdiAction.setStatusTip('Name, Call and other of station')
        exportAdiAction.triggered.connect(self.logSettings)
        #

        telnetAction = QAction(QIcon('logo.png'), 'Cluster window', self)
        telnetAction.setStatusTip('Name, Call and other of station')
        telnetAction.triggered.connect(self.logSettings)
        #
        newDiplomEnvAction = QAction(QIcon('logo.png'), 'New Diplom Env', self)
        newDiplomEnvAction.setStatusTip('Name, Call and other of station')
        newDiplomEnvAction.triggered.connect(self.logSettings)
        #
        helpAction = QAction(QIcon('logo.png'), 'New Diplom Env', self)
        helpAction.setStatusTip('Name, Call and other of station')
        helpAction.triggered.connect(self.logSettings)
        #
        aboutAction = QAction(QIcon('logo.png'), 'New Diplom Env', self)
        aboutAction.setStatusTip('Name, Call and other of station')
        aboutAction.triggered.connect(self.logSettings)
        #
        exitAction = QAction(QIcon('logo.png'), '&Exit', self)
        exitAction.triggered.connect(QApplication.quit)

        menuBar = self.menuBar()
        mainMenu = menuBar.addMenu('&Menu')
        mainMenu.addAction(logSettingsAction)
        mainMenu.addAction(catSettingsAction)
        searchWindowMenu = mainMenu.addMenu('Window')
        searchWindowMenu.addAction(telnetAction)
        searchWindowMenu.addAction(logWindowAction)
        searchWindowMenu.addAction(searchWindowAction)
        mainMenu.addAction(importAdiAction)
        mainMenu.addAction(exportAdiAction)
        diplomMenu = mainMenu.addMenu('Diplom Env.')
        diplomMenu.addAction(newDiplomEnvAction)
        mainMenu.addAction(exitAction)
        ###
        helpMenu = menuBar.addMenu('Help')
        helpMenu.addAction(helpAction)
        helpMenu.addAction(aboutAction)
        '''
        pass
    def searchWindow(self):

        logSearch.hide()

    def initUI(self):

        styleform = "background :" + settingsDict['form-background']
        self.setGeometry(int(settingsDict['log-form-window-left']), int(settingsDict['log-form-window-top']),
                         int(settingsDict['log-form-window-width']), int(settingsDict['log-form-window-height']))
        self.setWindowTitle('LinLog | Form')
        self.setWindowIcon(QIcon('logo.png'))
        style = "QWidget{background-color:" + settingsDict['background-color'] + "; color:" + settingsDict[
            'color'] + ";}"
        self.setStyleSheet(style)
        self.menu()

        # self.test()
        labelCall = QLabel("Call")
        labelCall.setFont(QtGui.QFont('SansSerif', 9))

        # labelCall.move(40,40)
        self.inputCall = QLineEdit()
        #self.inputCall.setFocusPolicy(Qt.StrongFocus)
        self.inputCall.setStyleSheet(styleform)
        self.inputCall.setFixedWidth(108)
        self.inputCall.textChanged[str].connect(
            self.onChanged)  # событие изминения текста, привязываем в слот функцию onChanged
        self._filter = Filter()
        # adjust for your QLineEdit
        self.inputCall.installEventFilter(self._filter)
        self.inputCall.returnPressed.connect(
            self.logFormInput)  # событие нажатия Enter, привязываем в слот функцию logSettings
        #self.inputCall.tabPressed.connect(self.internetWorker.get_internet_info)
        # inputCall.move(40,40)
        labelRstR = QLabel('RSTr')
        labelRstR.setFont(QtGui.QFont('SansSerif', 7))

        self.inputRstR = QLineEdit(self)
        self.inputRstR.setFixedWidth(30)
        self.inputRstR.setStyleSheet(styleform)
        # style= "QLineEdit{ border: 1px solid #313142; border-radius: 50px; background: "+settingsDict['form-background']+"; font-weight: bold;}"
        #self.inputRstR.setStyleSheet(style)
        self.inputRstR.installEventFilter(self._filter)

        labelRstS = QLabel('RSTs')
        labelRstS.setFont(QtGui.QFont('SansSerif', 7))
        self.inputRstS = QLineEdit(self)
        self.inputRstS.setFixedWidth(30)
        self.inputRstS.setStyleSheet(styleform)

        labelName = QLabel('Name')
        labelName.setFont(QtGui.QFont('SansSerif', 9))
        self.inputName = QLineEdit(self)
        self.inputName.setFixedWidth(137)
        self.inputName.setStyleSheet(styleform)
        self.inputName.returnPressed.connect(self.logFormInput)

        labelQth = QLabel("QTH  ")
        labelQth.setFont(QtGui.QFont('SansSerif', 9))

        self.inputQth = QLineEdit(self)
        self.inputQth.setFixedWidth(137)
        self.inputQth.setStyleSheet(styleform)
        self.inputQth.returnPressed.connect(self.logFormInput)

        self.comboMode = QComboBox(self)
        self.comboMode.addItems(["SSB", "ESSB", "CW", "AM", "DIGI"])
        indexMode = self.comboMode.findText(settingsDict['mode'])
        self.comboMode.setCurrentIndex(indexMode)
        self.comboMode.activated[str].connect(self.rememberMode)

        self.comboBand = QComboBox(self)
        self.comboBand.addItems(["160", "80", "40", "30", "20", "17", "15", "12", "10", "100", "200"])
        indexBand = self.comboBand.findText(settingsDict['band'])
        self.comboBand.setCurrentIndex(indexBand)
        self.comboBand.activated[str].connect(self.rememberBand)

        self.labelStatusCat = QLabel('CAT On')
        self.labelStatusCat.setFont(QtGui.QFont('SansSerif', 7))

        self.labelStatusTelnet = QLabel('Telnet')
        self.labelStatusTelnet.setFont(QtGui.QFont('SansSerif', 7))

        self.labelTime = QLabel()
        self.labelTime.setFont(QtGui.QFont('SansSerif', 7))


        self.labelFreq = QLabel()
        self.labelFreq.setFont(QtGui.QFont('SansSerif', 7))
        self.labelFreq.setText('      ')

        self.labelMyCall = QLabel(settingsDict['my-call'])
        self.labelMyCall.setFont(QtGui.QFont('SansSerif', 10))
        self.comments = QTextEdit()

        hBoxHeader = QHBoxLayout()
        hBoxHeader.addWidget(self.labelTime)

        hBoxLeft = QHBoxLayout(self)
        hBoxRight = QHBoxLayout(self)
        hBoxRst = QHBoxLayout(self)

        vBoxLeft = QVBoxLayout(self)
        vBoxRight = QVBoxLayout(self)
        vBoxMain = QVBoxLayout(self)
        # Build header line
        hBoxHeader.addWidget(self.labelTime)
        hBoxHeader.addWidget(self.labelFreq)
        hBoxHeader.addWidget(self.labelMyCall)
        # Build Left block
        # vBoxLeft.addLayout(hBoxHeader)

        # set label Call
        # set input CALL
        hCall = QHBoxLayout(self)
        hCall.addWidget(labelCall)
        hCall.addWidget(self.inputCall)
        hCall.addStretch(1)
        vBoxLeft.addLayout(hCall)

        hBoxRst.addWidget(labelRstR)  # set label RSTr
        hBoxRst.addWidget(self.inputRstR)
        hBoxRst.addWidget(labelRstS)  # set input RSTr
        hBoxRst.addWidget(self.inputRstS)
        hBoxRst.addStretch(1)

        vBoxLeft.addLayout(hBoxRst)
        hName = QHBoxLayout(self)
        hName.addWidget(labelName)
        hName.addWidget(self.inputName)
        hName.addStretch(1)
        vBoxLeft.addLayout(hName)

        hQth = QHBoxLayout(self)
        hQth.addWidget(labelQth)
        hQth.addWidget(self.inputQth)
        hQth.addStretch(1)
        vBoxLeft.addLayout(hQth)

        # vBoxLeft.addWidget( labelName) #set label Name
        # vBoxLeft.addWidget( inputName) #set input Name
        # vBoxLeft.addWidget( labelQth)  #set label QTH
        # vBoxLeft.addWidget( inputQth)  #set input RSTr

        vBoxRight.addWidget(self.comboBand)
        vBoxRight.addWidget(self.comboMode)
        vBoxRight.addStretch(1)
        vBoxRight.addWidget(self.labelStatusCat)
        vBoxRight.addWidget(self.labelStatusTelnet)

        leftRight = QHBoxLayout()
        leftRight.addLayout(vBoxLeft)
        leftRight.addLayout(vBoxRight)
        # leftRight.setAlignment(Qt.AlignHCenter)

        vBoxMain.addLayout(hBoxHeader)
        vBoxMain.addLayout(leftRight)
        vBoxMain.addWidget(self.comments)
        style = "QTextEdit{background:" + settingsDict['form-background'] + "; border: 1px solid " + settingsDict[
            'solid-color'] + ";}"
        self.comments.setStyleSheet(style)

        central_widget = QWidget()
        central_widget.setLayout(vBoxMain)
        self.setCentralWidget(central_widget)
        self.show()

        # run time in Thread
        self.run_time = realTime(logformwindow=self) #run time in Thread
        self.run_time.start()

    def rememberBand(self, text):
        with open('settings.cfg', 'r') as file:
            # read a list of lines into data
            data = file.readlines()
        for i in range(len(data)):
            string = data[i]
            string = string.strip()
            string = string.replace("\r", "")
            string = string.replace("\n", "")
            string = string.split('=')
            # print(string)
            if data[i][0] != "#":
                if string[0] == 'band':
                    string[1] = self.comboBand.currentText().strip()
                data[i] = string[0] + '=' + string[1] + '\n'
                with open('settings.cfg', 'w') as file:
                    file.writelines(data)

    def rememberMode(self, text):
        # print(self.comboMode.currentText())
        with open('settings.cfg', 'r') as file:
            # read a list of lines into data
            data = file.readlines()
        for i in range(len(data)):
            string = data[i]
            string = string.strip()
            string = string.replace("\r", "")
            string = string.replace("\n", "")
            string = string.split('=')
            # print(string)
            if data[i][0] != "#":
                if string[0] == 'mode':
                    string[1] = self.comboMode.currentText().strip()
                data[i] = string[0] + '=' + string[1] + '\n'
                with open('settings.cfg', 'w') as file:
                    file.writelines(data)

    def onChanged(self, text):
        '''метод которій отрабатывает как только произошло изменение в поле ввода'''
        self.inputCall.setText(text.upper())

        if re.search('[А-Я]', text):
            self.inputCall.setStyleSheet("color: rgb(255,2,2);")
        elif re.search('[A-Z]', text):
            style = "QLineEdit{ border: 1px solid " + settingsDict[
                'solid-color'] + "; border-radius: 50px; background: " + settingsDict[
                        'form-background'] + "; font-weight: bold;}"
            self.inputCall.setStyleSheet(style)
            # pyautogui.hotkey('ctrl', 'shift')
            # print(text)

        # print (locale)

    def logFormInput(self):

        call = str(self.inputCall.text()).strip()
        # print(call+ "this")
        if call != '':
            recordObject = {}
            freq = str(self.labelFreq.text()).strip()

            mode = str(self.comboMode.currentText()).strip()
            rstR = str(self.inputRstR.text()).strip()
            rstS = str(self.inputRstS.text()).strip()
            name = str(self.inputName.text()).strip()
            qth = str(self.inputQth.text()).strip()
            operator = str(self.labelMyCall.text()).strip()
            band = str(self.comboBand.currentText()).strip() + "M"
            comment = str(self.comments.toPlainText()).strip()
            comment = comment.replace("\r", " ")
            comment = comment.replace("\n", " ")

            # print("'QSO_DATE':'20190703', 'TIME_ON':'124600', 'FREQ':"+freq+" 'CALL':"+cal+"'MODE'"+mode+" 'RST_RCVD':"+rstR+" 'RST_SENT':"+rstS+", 'NAME':"+name+", 'QTH':"+qth+"'OPERATOR':"+operator+"'BAND':"+band+"'COMMENT':"+comment)

            datenow = datetime.datetime.now()
            date = datenow.strftime("%Y%m%d")
            time = datenow.strftime("%H%M%S")
            # print (name)
            recordObject = {'QSO_DATE': date, 'TIME_ON': time, 'FREQ': freq, 'CALL': call, 'MODE': mode,
                            'RST_RCVD': rstR, 'RST_SENT': rstS, 'NAME': name, 'QTH': qth, 'OPERATOR': operator,
                            'BAND': band, 'COMMENTS': comment}

            logWindow.addRecord(recordObject)
            self.inputCall.clear()
            self.inputRstR.clear()
            self.inputRstS.clear()
            self.inputName.clear()
            self.inputQth.clear()
            self.comments.clear()

    def closeEvent(self, event):
        '''
        This function recieve signal close() from logSearch window
        Save coordinate and size all window
        Close app
        '''
        self.parameter={}
        if settingsDict['log-window'] == 'true':
            logWindow.close()
            logWindow_geometry = logWindow.geometry()
            self.parameter.update({'log-window-left': str(logWindow_geometry.left()),
                              'log-window-top': str(logWindow_geometry.top()),
                              'log-window-width': str(logWindow_geometry.width()),
                              'log-window-height': str(logWindow_geometry.height())
                              })

        if settingsDict['search-internet-window'] == 'true':
            internetSearch.close()
            internetSearch_geometry = internetSearch.geometry()
            self.parameter.update({'search-internet-left': str(internetSearch_geometry.left()),
                              'search-internet-top': str(internetSearch_geometry.top()),
                              'search-internet-width': str(internetSearch_geometry.width()),
                              'search-internet-height': str(internetSearch_geometry.height())
                              })
        if settingsDict['log-search-window'] == 'true':
            logSearch.close()
            logSearch_geometry = logSearch.geometry()
            self.parameter.update({'log-search-window-left': str(logSearch_geometry.left()),
                              'log-search-window-top': str(logSearch_geometry.top()),
                              'log-search-window-width': str(logSearch_geometry.width()),
                              'log-search-window-height': str(logSearch_geometry.height())
                              })
        if settingsDict['log-form-window'] == 'true':
            logForm.close()
            logForm_geometry = logForm.geometry()
            self.parameter.update({'log-form-window-left': str(logForm_geometry.left()),
                              'log-form-window-top': str(logForm_geometry.top()),
                              'log-form-window-width': str(logForm_geometry.width()),
                              'log-form-window-height': str(logForm_geometry.height())
                              })
        if settingsDict['telnet-cluster-window'] == 'true':
            telnetCluster.close()
            telnetCluster_geometry = telnetCluster.geometry()
            self.parameter.update({'telnet-cluster-window-left': str(telnetCluster_geometry.left()),
                              'telnet-cluster-window-top': str(telnetCluster_geometry.top()),
                              'telnet-cluster-window-width': str(telnetCluster_geometry.width()),
                              'telnet-cluster-window-height': str(telnetCluster_geometry.height())
                              })
        #print(parameter)
        self.remember_in_cfg(self.parameter)


    def remember_in_cfg (self, parameter):
        '''
        This function reciev Dictionary parametr with key:value
        record key=value into config.cfg

        :param parameter:
        :return:
        '''
        filename='settings.cfg'
        with open(filename,'r') as f:
            old_data = f.readlines()
        for line, string in enumerate(old_data):
            print(line, string)
            for key in parameter:
                if key in string:
                    string = key+"="+parameter[key]+"\n"
                    old_data[line] = string
        with open(filename, 'w') as f:
            f.writelines(old_data)


        '''   
        for key in parameter:
            new_data = old_data.replace(old_data.startswith(key), key+"="+parameter[key])
        with open(filename,'w') as f:
            f.write(new_data)
       '''        '''
        with open('settings.cfg', 'r') as file:
            # read a list of lines into data
            data = file.readlines()
            print(data)
        file.close()
        string_lenght = len(data)
        for i in range(string_lenght):
            #string = data[i]
            if data[i][0] != "#":

                print(data[i].split('=')[0])

                for key in parameter:

                    if data[i].split('=')[0] == key:
                        print(data[i].split('=')[1])
                        #data[i].split('=')[1] = parameter[key]
                        data[i] = key + '=' + parameter[key] + '\n'
                    with open('settings.cfg', 'w') as file:
                        file.writelines(data)
                    file.close()


        '''

    def empty(self):
        print('hi')

    def logSettings(self):
        print('logSettings')
        # logSearch.close()

    def test(data):
        pass



class clusterThread(QThread):
    def __init__(self, mainwindow, parent=None):
        super().__init__()
        self.telnetCluster = mainwindow
        # self.run()

    def run(self):
        HOST = settingsDict['telnet-host']
        PORT = settingsDict['telnet-port']
        call = settingsDict['my-call']
        telnetObj = telnetlib.Telnet(HOST, PORT)
        lastRow = 0

        message = (call + "\n").encode('ascii')
        telnetObj.write(message)
        message2 = (call + "\n").encode('ascii')
        telnetObj.write(message2)
        splitString = []
        cleanList = []
        i = 0
        print('Starting Telnet cluster:', HOST, ':', PORT, '\nCall:', call, '\n\n')
        while 1:
            output_data = telnetObj.read_some()

            if output_data != '':
                if output_data[0:2].decode(settingsDict['encodeStandart']) == "DX":
                    splitString = output_data.decode(settingsDict['encodeStandart']).split(' ')
                    count_chars = len(splitString)
                    for i in range(count_chars):
                        if splitString[i] != '':
                            cleanList.append(splitString[i])
                    # print(self.telnetCluster.tableWidget)

                    #print(cleanList) # Check point - output List with data from cluster telnet-server

                    lastRow = self.telnetCluster.tableWidget.rowCount()
                    self.telnetCluster.tableWidget.insertRow(lastRow)
                    self.telnetCluster.tableWidget.setItem(lastRow, 0,
                                                           QTableWidgetItem(
                                                               strftime("%H:%M:%S", localtime())))
                    self.telnetCluster.tableWidget.setItem(lastRow, 1,
                                                           QTableWidgetItem(
                                                               strftime("%H:%M:%S", gmtime())))
                    if (len(cleanList) > 4):
                        self.telnetCluster.tableWidget.setItem(lastRow, 2,
                                                               QTableWidgetItem(cleanList[4]))

                        self.telnetCluster.tableWidget.setItem(lastRow, 3,
                                                               QTableWidgetItem(cleanList[3]))

                    self.telnetCluster.tableWidget.resizeColumnsToContents()
                    self.telnetCluster.tableWidget.setItem(lastRow, 4,
                                                           QTableWidgetItem(
                                                               output_data.decode(settingsDict['encodeStandart'])))

                    self.telnetCluster.tableWidget.resizeColumnsToContents()
                    self.telnetCluster.tableWidget.resizeRowsToContents()
                    self.telnetCluster.tableWidget.scrollToBottom()

                    #print(output_data) # Check point - output input-string with data from cluster telnet-server
                elif output_data[0:3].decode(settingsDict['encodeStandart']) == "WWV":
                    self.telnetCluster.labelIonosphereStat.setText(
                        "Ionosphere status: " + output_data.decode(settingsDict['encodeStandart']))
                    print("Ionosphere status: ", output_data.decode(settingsDict['encodeStandart']))
                del cleanList[0:len(cleanList)]


class telnetCluster(QWidget):

    def __init__(self):
        super().__init__()
        # self.mainwindow = mainwindow

        self.host = settingsDict['telnet-host']
        self.port = settingsDict['telnet-port']
        self.call = settingsDict['my-call']
        self.tableWidget = QTableWidget()
        self.allRows = 0

        self.initUI()

    def initUI(self):
        '''
         Design of cluster window

        '''

        self.setGeometry(int(settingsDict['telnet-cluster-window-left']), int(settingsDict['telnet-cluster-window-top']),
                         int(settingsDict['telnet-cluster-window-width']), int(settingsDict['telnet-cluster-window-height']))
        self.setWindowTitle('Telnet cluster')
        self.setWindowIcon(QIcon('logo.png'))
        style = "QWidget{background-color:" + settingsDict['background-color'] + "; color:" + settingsDict[
            'color'] + ";}"
        self.setStyleSheet(style)
        self.labelIonosphereStat = QLabel()
        self.labelIonosphereStat.setStyleSheet("font: 12px;")
        style = "QTableWidget{background:" + settingsDict['form-background'] + "; border: 0px solid, #000000 ; width " \
                                                                               ": 100%;  font-size: 9 px; } "
        self.tableWidget.setStyleSheet(style)
        fnt = self.tableWidget.font()
        fnt.setPointSize(9)
        self.tableWidget.setFont(fnt)
        self.tableWidget.setRowCount(0)
        self.tableWidget.horizontalHeader().setStyleSheet("font: 12px; width:100%;")
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setHorizontalHeaderLabels(["Time Loc", "Time GMT", "Call", "Freq", " Spot"])
        self.tableWidget.verticalHeader().hide()
        self.tableWidget.cellClicked.connect(self.getFreq)
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.move(0, 0)
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.labelIonosphereStat)
        self.layout.addWidget(self.tableWidget)
        self.setLayout(self.layout)

        # logForm.test('test')
        self.show()

        self.run_cluster = clusterThread(mainwindow=self)
        self.run_cluster.start()

    def getFreq(self):
        row = self.tableWidget.currentItem().row()
        item = self.tableWidget.item(row, 3).text()
        logForm.labelFreq.setText(item)
        print(item)


class internetSearch(QWidget):

    def __init__(self):
        super().__init__()
        self.labelImage = QLabel(self)
        #self.pixmap=""
        self.initUI()

    def initUI(self):
        hbox = QHBoxLayout(self)
        self.pixmap = QPixmap("logo.png")
        self.labelImage = QLabel(self)
        self.labelImage.setAlignment(Qt.AlignCenter)
        self.labelImage.setPixmap(self.pixmap)
        hbox.addWidget(self.labelImage)
        self.setLayout(hbox)

        #self.move(100, 200)
        self.setGeometry(int(settingsDict['search-internet-left']),
                         int(settingsDict['search-internet-top']),
                         int(settingsDict['search-internet-width']),
                         int(settingsDict['search-internet-height']))
        self.setWindowTitle('Telnet cluster')
        self.setWindowIcon(QIcon('logo.png'))
        self.setWindowTitle('Image from internet')
        self.show()

    def update_photo(self):
        pixmap = QPixmap("logo.png")
        self.labelImage.setPixmap(pixmap)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    if settingsDict['log-window'] == 'true':
        logWindow = logWindow()
    if settingsDict['log-search-window'] == 'true':
        logSearch = logSearch()
    if settingsDict['log-form-window'] == 'true':
        logForm = logForm()
    if settingsDict['telnet-cluster-window'] == 'true':
        telnetCluster = telnetCluster()
    if settingsDict['search-internet-window'] == 'true':
        internetSearch = internetSearch()
    #adi = Adi_file()
    #Adi_file().get_all_qso()
    list = [{'call':'URLGA' , 'name':'Sergey'}, 'blah2\n', 'blah3\n']

    Adi_file().record_all_qso(list)
    sys.exit(app.exec_())
