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
import tci
import std
import settings

# import pyautogui

# import xdo  # $ pip install  python-libxdo
from PyQt5.QtWidgets import QApplication, QAction, QWidget, QMainWindow, QTableView, QTableWidget, QTableWidgetItem, QTextEdit, \
    QLineEdit, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QComboBox
from PyQt5.QtCore import pyqtSignal, QObject, QEvent
from PyQt5.QtGui import QIcon, QFocusEvent, QPixmap, QTextTableCell, QStandardItemModel
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

        with open(self.filename, 'r') as file: #read all strings

            self.strings_in_file = file.readlines()

    def get_last_string(self):
        return len(self.strings_in_file)


    def store_changed_qso(self, object):
        '''
        1. Function recived object in format (ch.1)
        2. Building string for log.adi file
        3. Read all strings
        4. ReWrite string in log.adi file
        chapter 1
        :param object: {'BAND': '40M', 'CALL': 'UR4LGA', 'FREQ': 'Freq: 7028500', 'MODE': 'ESSB',
        'OPERATOR': 'UR4LGA', 'QSO_DATE': '20191109', 'TIME_ON': '224058', 'RST_RCVD': '59',
         'RST_SENT': '59', 'NAME': '', 'QTH': '', 'COMMENTS': '', 'TIME_OFF': '224058',
         'eQSL_QSL_RCVD': 'Y', 'EOR': 'R\n',
         'string_in_file': '186', 'records_number': '89'}

        :return:
        '''

        #print("hello  store_changed_qso method in Adi_file class\n", object)
        stringToAdiFile = "<BAND:" + str(len(object['BAND'])) + ">" + object['BAND'] + "<CALL:" + str(
            len(object['CALL'])) + ">"

        stringToAdiFile = stringToAdiFile + object['CALL'] + "<FREQ:" + str(len(object['FREQ'])) + ">" + \
                          object['FREQ']
        stringToAdiFile = stringToAdiFile + "<MODE:" + str(len(object['MODE'])) + ">" + object[
            'MODE'] + "<OPERATOR:" + str(len(object['OPERATOR']))
        stringToAdiFile = stringToAdiFile + ">" + object['OPERATOR'] + "<QSO_DATE:" + str(
            len(object['QSO_DATE'])) + ">"
        stringToAdiFile = stringToAdiFile + object['QSO_DATE'] + "<TIME_ON:" + str(
            len(object['TIME_ON'])) + ">"
        stringToAdiFile = stringToAdiFile + object['TIME_ON'] + "<RST_RCVD:" + \
                          str(len(object['RST_RCVD'])) + ">" + object['RST_RCVD']
        stringToAdiFile = stringToAdiFile + "<RST_SENT:" + str(len(object['RST_SENT'])) + ">" + \
                          object['RST_SENT'] + "<NAME:" + str(len(object['NAME'])) + ">" + object['NAME'] + \
                          "<QTH:" + str(len(object['QTH'])) + ">" + object['QTH'] + "<COMMENTS:" + \
                          str(len(object['COMMENTS'])) + ">" + object['COMMENTS'] + "<TIME_OFF:" + \
                          str(len(object['TIME_OFF'])) + ">" + object['TIME_OFF'] + "<eQSL_QSL_RCVD:1>Y<EOR>\n"
        print("store_changed_qso: stringToAdiFile", stringToAdiFile)

        self.strings_in_file[int(object['string_in_file'])-1] = stringToAdiFile
        with open(self.filename, 'w') as file:
            file.seek(0)
            file.writelines(self.strings_in_file)


        #print("this:", self.strings_in_file[int(object['string_in_file'])-1])





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
                #print (lines)
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
        #print(list_data[0]['call'])
        #header = self.get_header()
        #with open('aditest.adi', 'w') as file:
          #  file.writelines(header)
            #file.writelines(list_data)

class Filter(QObject):

    previous_call = ''



    def eventFilter(self, widget, event):
        # FocusOut event
        #print(event.type())

        if event.type() == QEvent.FocusOut:
                # do custom stuff
                text = logForm
                textCall = text.inputCall.text()
                foundList = self.searchInBase(textCall)
                logSearch.overlap(foundList)
                freq = logForm.get_freq()
                #print("freq in Filter", freq)
                if textCall != '' and textCall != Filter.previous_call:
                    if settingsDict['search-internet-window'] == 'true':
                        #print("textCall", textCall)
                        Filter.previous_call = textCall
                        self.isearch = internetworker.internetWorker(window=internetSearch, callsign=textCall, settings=settingsDict)
                        self.isearch.start()
                        if settingsDict['tci'] == 'enable':
                            try:
                                tci.Tci_sender(settingsDict['tci-server']+":"+settingsDict['tci-port']).set_spot(textCall, freq)
                            except:
                                print("Filter: Can't connect to TCI-server")

                if textCall == '' or textCall == ' ':
                    pixmap = QPixmap('logo.png')
                    #pixmap_resized = pixmap.scaled(int(settingsDict['image-width']),
                                                  # int(settingsDict['image-height']),
                                                  # QtCore.Qt.KeepAspectRatio)
                    #internetSearch.labelImage.setPixmap(pixmap_resized)
                    #print(img)


                # print ('focus out')
                return False

        if event.type() == QEvent.FocusIn:
                # do custom stuff
                if logForm.inputCall.text() == '':
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

class Log_window (QWidget):
    def __init__(self):
        super().__init__()
        self.filename = "log.adi"
        self.filename = "log.adi"
        self.allCollumn = ['records_number', 'QSO_DATE', 'TIME_ON', 'BAND', 'CALL', 'MODE', 'RST_RCVD', 'RST_SENT'
                           'NAME', 'QTH', 'COMMENTS', 'TIME_OFF', 'eQSL_QSL_RCVD']
        self.allRecord = parse.getAllRecord(self.allCollumn, self.filename)
        self.mass = [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10], [11, 12, 13, 14, 15]]
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
        self.tableWidget = QTableView()
        style_table = "QWidget{background-color:" + settingsDict['form-background'] + "; color:" + \
                      settingsDict['color'] + "; font-size: 12px;}"
        self.tableWidget.setStyleSheet(style_table)
        tableModel = QStandardItemModel()
        all_records_count = len(self.allRecord)
        for row in range(all_records_count):
           #for col in range(len(self.allCollumn)):
                no = QtGui.QStandardItem(self.allRecord[(all_records_count-1)-row]['records_number'])
                date = QtGui.QStandardItem(self.allRecord[(all_records_count-1)-row]['QSO_DATE'])
                time = QtGui.QStandardItem(self.allRecord[(all_records_count-1)-row]['TIME_ON'])
                band = QtGui.QStandardItem(self.allRecord[(all_records_count-1)-row]['BAND'])
                call = QtGui.QStandardItem(self.allRecord[(all_records_count-1)-row]['CALL'])
                mode = QtGui.QStandardItem(self.allRecord[(all_records_count-1)-row]['MODE'])
                rst_r = QtGui.QStandardItem(self.allRecord[(all_records_count-1)-row]['RST_RCVD'])
                rst_s = QtGui.QStandardItem(self.allRecord[(all_records_count-1)-row]['RST_SENT'])
                name = QtGui.QStandardItem(self.allRecord[(all_records_count-1)-row]['NAME'])
                qth = QtGui.QStandardItem(self.allRecord[(all_records_count-1)-row]['QTH'])
                comments = QtGui.QStandardItem(self.allRecord[(all_records_count-1)-row]['COMMENTS'])
                e_qsl_r = QtGui.QStandardItem(self.allRecord[(all_records_count-1)-row]['eQSL_QSL_RCVD'])
                tableModel.appendRow([no, date, time, band, call, mode, rst_r, rst_s, name, qth, comments, time, e_qsl_r])
        tableModel.setHorizontalHeaderLabels(["No", "   Date   ", " Time ", "Band", "   Call   ", "Mode", "RST r",
                                              "RST s", "      Name      ", "      QTH      ", " Comments ",
                                              " Time off ", " eQSL Rcvd "])

        
        self.tableWidget.setModel(tableModel)
        self.tableWidget.resizeRowsToContents()
        self.tableWidget.resizeColumnsToContents()
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tableWidget)
        self.setLayout(self.layout)            
        self.show()

class logWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.filename = "log.adi"
        if os.path.isfile(self.filename):
            pass
        else:
            with open(self.filename, "w") as file:
                file.write(Adi_file().get_header())

        self.allCollumn = ['records_number', 'QSO_DATE', 'TIME_ON', 'BAND', 'CALL', 'MODE', 'RST_RCVD', 'RST_SENT',
                               'NAME', 'QTH', 'COMMENTS', 'TIME_OFF', 'eQSL_QSL_RCVD']
        self.allRecord = parse.getAllRecord(self.allCollumn, self.filename)


        self.initUI()

    def get_all_record(self):
        return self.allRecord

    def initUI(self):


        self.setGeometry(int(settingsDict['log-window-left']),
                         int(settingsDict['log-window-top']),
                         int(settingsDict['log-window-width']),
                         int(settingsDict['log-window-height']))
        self.setWindowTitle('LinLog | All QSO')
        self.setWindowIcon(QIcon('logo.png'))
        self.setWindowOpacity(float(settingsDict['logWindow-opacity']))
        style = "QWidget{background-color:" + settingsDict['background-color'] + "; color:" + settingsDict[
            'color'] + ";}"
        self.setStyleSheet(style)

        self.allRows = len(self.allRecord)
        allCols = len(self.allCollumn)
        # print ('%10s %5s %10s %16s %8s %8s %8s %15s %15s' % ('QSO_DATE', 'TIME', 'FREQ', 'CALL',
        #			'MODE', 'RST_RCVD', 'RST_SENT',	'NAME', 'QTH')
        #		   )
        self.tableWidget = QTableWidget()
        style_table = "QWidget{background-color:" + settingsDict['form-background'] + "; color:" + settingsDict[
            'color'] + "; font: 12px}"
        self.tableWidget.setStyleSheet(style_table)
        fnt = self.tableWidget.font()
        fnt.setPointSize(8)
        self.tableWidget.setSortingEnabled(True)
        self.tableWidget.setFont(fnt)
        self.tableWidget.setRowCount(self.allRows)
        self.tableWidget.setColumnCount(13)

        self.tableWidget.setHorizontalHeaderLabels(["No", "   Date   ", " Time ", "Band", "   Call   ", "Mode", "RST r",
                                                    "RST s", "      Name      ", "      QTH      ", " Comments ", " Time off ", " eQSL Rcvd "])
        self.tableWidget.resizeColumnsToContents()


        self.tableWidget.resizeRowsToContents()

        if self.allRows == 0:
            print("All Rows:", type(self.allRows), self.allRows)
            for col in range(allCols):
                print ("cols:", col)
                #self.tableWidget.setItem(0, col, QTableWidgetItem())

        for row in range(self.allRows):
            for col in range(allCols):
                pole = self.allCollumn[col]
                #print(self.allRows, row, self.allRows - row )
                #print("Number record:", self.allRecord[row][pole])
                if self.allRecord[(self.allRows-1)-row][pole] != ' ' or self.allRecord[(self.allRows-1)-row][pole] != '':
                    if col == 0:
                        self.tableWidget.setItem(row, col, self.protectionItem(self.allRecord[(self.allRows - 1) - row][pole], Qt.ItemIsSelectable | Qt.ItemIsEnabled))

                                #QTableWidgetItem(self.allRecord[(self.allRows - 1) - row][pole]))

                    else:
                        self.tableWidget.setItem(row, col, QTableWidgetItem(self.allRecord[(self.allRows-1)-row][pole]))
                    #print("Number record:", self.allRecord[row]['records_number'])
                #  print(self.allRecord[row][pole])
       # self.tableWidget.currentItemChanged.connect(self.add_record)
        self.tableWidget.itemActivated.connect(self.store_change_record)

        self.tableWidget.move(0, 0)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tableWidget)
        self.setLayout(self.layout)

        #
        logForm.test('test')
        self.show()

    def protectionItem(self, text, flags):
        tableWidgetItem = QTableWidgetItem(text)
        tableWidgetItem.setFlags(flags)
        return tableWidgetItem


    def store_change_record(self):

            print("store_change_record")
            row = self.tableWidget.currentItem().row()
            record_number = self.tableWidget.item(row, 0).text()
            date = self.tableWidget.item(row, 1).text()
            time = self.tableWidget.item(row, 2).text()
            call = self.tableWidget.item(row, 4).text()
            freq = self.allRecord[int(record_number)-1]['FREQ']
            rstR = self.tableWidget.item(row, 6).text()
            rstS = self.tableWidget.item(row, 7).text()
            name = self.tableWidget.item(row, 8).text()
            qth = self.tableWidget.item(row, 9).text()
            operator = self.allRecord[int(record_number)-1]['OPERATOR']
            band = self.tableWidget.item(row, 3).text()
            comment = self.tableWidget.item(row, 10).text()
            time_off = self.tableWidget.item(row, 11).text()
            eQSL_QSL_RCVD = self.tableWidget.item(row, 12).text()
            mode = self.tableWidget.item(row, 5).text()
            string_in_file = self.allRecord[int(record_number) - 1]['string_in_file']
            records_number = self.allRecord[int(record_number) - 1]['records_number']

            if 'string_in_file' in self.allRecord:
                pass

            else:
                pass






            new_object = {'BAND': band, 'CALL': call, 'FREQ': freq, 'MODE': mode, 'OPERATOR':operator,
                             'QSO_DATE': date, 'TIME_ON': time, 'RST_RCVD': rstR, 'RST_SENT':rstS,
                             'NAME': name, 'QTH': qth, 'COMMENTS': comment, 'TIME_OFF': time_off, 'eQSL_QSL_RCVD': eQSL_QSL_RCVD,
                             'EOR': 'R\n', 'string_in_file': string_in_file, 'records_number': records_number}

            print("store_change_record: NEW Object", new_object)
            Adi_file().store_changed_qso(new_object)
            self.allRecord[int(record_number) - 1] = new_object





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
                              'COMMENTS'] + "<TIME_OFF:"+str(len(recordObject['TIME_OFF']))+">"+recordObject['TIME_OFF']+"<eQSL_QSL_RCVD:1>Y<EOR>\n"
        # print(stringToAdiFile)
        recordObject['string_in_file'] = Adi_file().get_last_string() + 1
        '''
        if len(self.allRecord) == 0:
            recordObject['records_number'] = 0
        else:
            recordObject['records_number'] = len(self.allRecord)
        '''
        file = open(self.filename, 'a')
        resultWrite = file.write(stringToAdiFile)
        # print(resultWrite)
        if resultWrite > 0:
            file.close()
        else:
           print("QSO not write in logfile")
           file.close()
        #####

        # record to allRecord
        print(recordObject)

        self.allRecord.append(recordObject)
        all_rows=len(self.allRecord)
        # record to table
        allCols = len(self.allCollumn)
        #row = self.allRows + 1
        # print(recordObject)
        # print (row)
        self.tableWidget.setRowCount(all_rows)
        self.tableWidget.insertRow(0)
        self.tableWidget.resizeRowsToContents()

        for col in range(allCols):

            self.tableWidget.setItem(0, col, QTableWidgetItem(recordObject[self.allCollumn[col]]))


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
        self.setWindowOpacity(float(settingsDict['logSearch-opacity']))
        style = "QWidget{background-color:" + settingsDict['background-color'] + "; color:" + settingsDict[
            'color'] + "; font: 12px;}"
        self.setStyleSheet(style)

        # print ('%10s %5s %10s %16s %8s %8s %8s %15s %15s' % ('QSO_DATE', 'TIME', 'FREQ', 'CALL',
        #			'MODE', 'RST_RCVD', 'RST_SENT',	'NAME', 'QTH')
        #		   )
        self.tableWidget = QTableWidget()
        style_table = "QWidget{background-color:" + settingsDict['form-background'] + "; color:" + settingsDict[
            'color'] + "; font: 12px}"
        self.tableWidget.setStyleSheet(style_table)
        fnt = self.tableWidget.font()
        fnt.setPointSize(9)
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
        self.tableWidget.setColumnCount(10)
        self.tableWidget.setHorizontalHeaderLabels(["No", "   Date   ", " Time ", "Band", "   Call   ", "Mode", "RST r",
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
        self.tableWidget.resizeColumnsToContents()
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

        logSettingsAction = QAction('Settings', self)
        #logSettingsAction.setStatusTip('Name, Call and other of station')
        logSettingsAction.triggered.connect(self.logSettings)
        #
        window_cluster_action = QAction('Cluster', self)
        #windowAction.setStatusTip('Name, Call and other of station')
        window_cluster_action.triggered.connect(self.stat_cluster)
        #
        window_inet_search_action = QAction ('Internet search', self)
        window_inet_search_action.triggered.connect(self.stat_internet_search)
        #
        window_repeat_qso_action = QAction ('Repeat QSO', self)
        window_repeat_qso_action.triggered.connect(self.stat_repeat_qso)


        menuBar = self.menuBar()
        menuBar.setStyleSheet("QWidget{font: 12px;}")
      #  settings_menu = menuBar.addMenu('Settings')
        menuBar.addAction(logSettingsAction)
        WindowMenu = menuBar.addMenu('&Window')
        #WindowMenu.triggered.connect(self.logSettings)
        WindowMenu.addAction(window_cluster_action)
        WindowMenu.addAction(window_inet_search_action)
        WindowMenu.addAction(window_repeat_qso_action)



        #
        '''
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
        self.comboMode.addItems(["SSB", "ESSB", "CW", "AM", "FM", "DSB", "DIGI"])
        indexMode = self.comboMode.findText(settingsDict['mode'])
        self.comboMode.setCurrentIndex(indexMode)
        self.comboMode.activated[str].connect(self.rememberMode)

        self.comboBand = QComboBox(self)
        self.comboBand.addItems(["160", "80", "40", "30", "20", "17", "15", "12", "10", "6", "2", "100", "200"])
        indexBand = self.comboBand.findText(settingsDict['band'])
        self.comboBand.setCurrentIndex(indexBand)
        self.comboBand.activated[str].connect(self.rememberBand)

        self.labelStatusCat = QLabel('')
        self.labelStatusCat.setFont(QtGui.QFont('SansSerif', 7))

        self.labelStatusTelnet = QLabel('')
        self.labelStatusTelnet.setFont(QtGui.QFont('SansSerif', 7))

        self.labelTime = QLabel()
        self.labelTime.setFont(QtGui.QFont('SansSerif', 7))


        self.labelFreq = QLabel()
        self.labelFreq.setFont(QtGui.QFont('SansSerif', 7))
        self.labelFreq.setText('')

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
            #freq = str(self.labelFreq.text()).strip()

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
            freq = self.get_freq()
            eQSL_QSL_RCVD = "N"
            all_records = logWindow.get_all_record()            # print("'QSO_DATE':'20190703', 'TIME_ON':'124600', 'FREQ':"+freq+" 'CALL':"+cal+"'MODE'"+mode+" 'RST_RCVD':"+rstR+" 'RST_SENT':"+rstS+", 'NAME':"+name+", 'QTH':"+qth+"'OPERATOR':"+operator+"'BAND':"+band+"'COMMENT':"+comment)
            record_number = len(all_records) + 1
            #print("record_number:", record_number)
            datenow = datetime.datetime.now()
            date = datenow.strftime("%Y%m%d")
            time = str(datenow.strftime("%H%M%S"))


            recordObject = {'records_number': str(record_number), 'QSO_DATE': date, 'TIME_ON': time, 'FREQ': freq, 'CALL': call, 'MODE': mode,
                            'RST_RCVD': rstR, 'RST_SENT': rstS, 'NAME': name, 'QTH': qth, 'OPERATOR': operator,
                            'BAND': band, 'COMMENTS': comment, 'TIME_OFF': time,
                            'eQSL_QSL_RCVD': eQSL_QSL_RCVD}

            logWindow.addRecord(recordObject)
            try:
                tci.Tci_sender(settingsDict['tci-server'] + ":" + settingsDict['tci-port']).change_color_spot(call, freq)
            except:
                print ("LogFormInput: can't connect to TCI server (set spot)")

            logForm.inputCall.setFocus(True)

            self.inputCall.clear()
            self.inputRstS.setText('59')
            self.inputRstR.setText('59')
            self.inputName.clear()
            self.inputQth.clear()
            self.comments.clear()

    def changeEvent(self, event):

        if event.type() == QtCore.QEvent.WindowStateChange:
            if self.isMinimized():
                if settingsDict['search-internet-window'] == 'true':
                    internetSearch.showMinimized()
                if settingsDict['log-search-window'] == 'true':
                    logSearch.showMinimized()
                if settingsDict['log-window'] == 'true':
                    logWindow.showMinimized()
                if settingsDict['telnet-cluster-window'] == 'true':
                    telnetCluster.showMinimized()
            QWidget.changeEvent(self, event)
    def showEvent(self, event):
        print ("Show normal")
       # internetSearch.showNormal()
       # logSearch.showNormal()



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
            #print(line, string)
            for key in parameter:
                if key in string:
                    string = key+"="+parameter[key]+"\n"
                    old_data[line] = string
        with open(filename, 'w') as f:
            f.writelines(old_data)




    def empty(self):
        print('hi')

    def logSettings(self):
        print('logSettings')
        #menu_window.show()
        self.menu = settings.Menu(settingsDict,
                                  telnetCluster,
                                  logForm,
                                  logSearch,
                                  logWindow,
                                  internetSearch,
                                  tci_recv)
        self.menu.show()
        # logSearch.close()

    def stat_cluster(self):

        if telnetCluster.isHidden():
            print('statTelnet')
            telnetCluster.show()
        elif telnetCluster.isEnabled():
            telnetCluster.hide()

    def stat_internet_search(self):
        if internetSearch.isHidden():
            print('internet_search')
            internetSearch.show()
        elif internetSearch.isEnabled():
            internetSearch.hide()

    def stat_repeat_qso(self):
        if logSearch.isHidden():
            print('internet_search')
            logSearch.show()
        elif logSearch.isEnabled():
            logSearch.hide()

    def set_band(self, band):
        #print("LogForm.set_band. input band:", band)
        indexMode = self.comboBand.findText(band)
        self.comboBand.setCurrentIndex(indexMode)


    def set_freq(self, freq):
        freq_string = str(freq)
        freq_string = freq_string.replace('.', '')
        len_freq=len(freq)
        freq_to_label = freq[0:len_freq - 6] + "." + freq[len_freq - 6:len_freq - 3] + "." + freq[len_freq - 3:len_freq]
        self.labelFreq.setText("Freq: "+str(freq_to_label))
        band = std.std().get_std_band(freq)
        #print(band)
        indexMode = self.comboBand.findText(band)
        self.comboBand.setCurrentIndex(indexMode)


    def set_call(self, call):
        self.inputCall.setText(str(call))

    def set_mode_tci(self, mode):
        if mode == "lsb" or mode == "usb":
            mode_string = 'SSB'
        if mode == "am" or mode == "sam":
            mode_string = 'AM'
        if mode == "dsb":
            mode_string = 'DSB'
        if mode == "cw":
            mode_string = 'CW'
        if mode == "nfm" or mode == "wfm":
            mode_string = 'FM'
        if mode == "digil" or mode == "digiu" or mode == "drm":
            mode_string = 'DIGI'
        indexMode = self.comboMode.findText(mode_string)
        self.comboMode.setCurrentIndex(indexMode)

    def set_tci_stat(self, values):
        self.labelStatusCat.setStyleSheet("color: #57BD79; font-weight: bold;")
        self.labelStatusCat.setText(values)

    def set_tci_label_found(self, values=''):
        self.labelStatusCat.setStyleSheet("color: #FF6C49; font-weight: bold;")
        self.labelStatusCat.setText("TCI Found "+values)
        time.sleep(0.55)
        self.labelStatusCat.setText("")

    def set_telnet_stat(self):
        self.labelStatusTelnet.setStyleSheet("color: #57BD79; font-weight: bold;")
        self.labelStatusTelnet.setText("✔ Telnet")
        time.sleep(0.15)
        self.labelStatusTelnet.setText("")

    def get_band(self):
        return self.comboBand.currentText()


    def get_freq(self):
        freq_string = self.labelFreq.text()
        if freq_string == '':
            band = self.get_band()
            if band == "160":
                freq_string = '1800000'
            elif band == "80":
                freq_string = '3500000'
            elif band == "40":
                freq_string = '7000000'
            elif band == "30":
                freq_string = '10000000'
            elif band == "20":
                freq_string = '14000000'
            elif band == "17":
                freq_string = '18000000'
            elif band == "15":
                freq_string = '21000000'
            elif band == "12":
                freq_string = '24000000'
            elif band == "10":
                freq_string = '28000000'
            elif band == "6":
                freq_string = '54000000'
            elif band == "144":
                freq_string = '144500000'
            else:
                freq_string = 'non'
        freq_string = freq_string.replace('Freq: ', '')
        freq_string = freq_string.replace('.', '')
        #if len(str(freq_string)) < 8 and len(str(freq_string)) >= 5:
        #    freq_string = freq_string + "00"
        #if len(str(freq_string)) < 5:
         #   freq_string = freq_string + "000"

        return freq_string
    ## updates methods

    def refresh_interface(self):
        self.labelMyCall.setText(settingsDict['my-call'])
        self.update_color_schemes()

    def update_color_schemes(self):
        style = "QWidget{background-color:" + settingsDict['background-color'] + "; color:" + settingsDict[
            'color'] + ";}"
        self.setStyleSheet(style)




    def update_settings(self, new_settingsDict):
        settingsDict.update(new_settingsDict)
        #print(settingsDict['my-call'])



    def test(data):
        pass

class clusterThread(QThread):
    def __init__(self, cluster_window, form_window, parent=None):
        super().__init__()
        self.telnetCluster = cluster_window
        self.form_window = form_window
        # self.run()

    def run(self):
        HOST = settingsDict['telnet-host']
        PORT = settingsDict['telnet-port']
        call = settingsDict['my-call']
        while 1:
            try:
                telnetObj = telnetlib.Telnet(HOST, PORT)
                break
            except:
                time.sleep(3)
                continue

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
          try:
            output_data = telnetObj.read_some()


            if output_data != '':
                    self.form_window.set_telnet_stat()
                    #print (output_data)
                    if output_data[0:2].decode(settingsDict['encodeStandart']) == "DX":
                        splitString = output_data.decode(settingsDict['encodeStandart']).split(' ')
                        count_chars = len(splitString)
                        for i in range(count_chars):
                            if splitString[i] != '':
                                cleanList.append(splitString[i])
                        print("clusterThread: clean list", cleanList)
                        if telnetCluster.cluster_filter(cleanList=cleanList):
    #####
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
                                                                       QTableWidgetItem(cleanList[int(settingsDict['telnet-call-position'])]))

                                self.telnetCluster.tableWidget.setItem(lastRow, 3,
                                                                       QTableWidgetItem(cleanList[int(settingsDict['telnet-freq-position'])]))

                            self.telnetCluster.tableWidget.resizeColumnsToContents()
                            self.telnetCluster.tableWidget.setItem(lastRow, 4,
                                                                   QTableWidgetItem(
                                                                       output_data.decode(settingsDict['encodeStandart'])))

                            self.telnetCluster.tableWidget.resizeColumnsToContents()
                            self.telnetCluster.tableWidget.resizeRowsToContents()
                            self.telnetCluster.tableWidget.scrollToBottom()
                            if settingsDict['spot-to-pan'] == 'enable':
                                freq = std.std().std_freq(freq=cleanList[3])
                                try:
                                    tci.Tci_sender(settingsDict['tci-server']+":"+settingsDict['tci-port']).set_spot(cleanList[4], freq, color="19711680")
                                except:
                                    print("clusterThread: Except in Tci_sender.set_spot")
                        ####
                    # #print(output_data) # Check point - output input-string with data from cluster telnet-server
                    elif output_data[0:3].decode(settingsDict['encodeStandart']) == "WWV":
                        self.telnetCluster.labelIonosphereStat.setText(
                            "Ionosphere status: " + output_data.decode(settingsDict['encodeStandart']))
                        #print("Ionosphere status: ", output_data.decode(settingsDict['encodeStandart']))
                    del cleanList[0:len(cleanList)]
                    time.sleep(0.3)
          except:
              continue
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
        self.setWindowOpacity(float(settingsDict['clusterWindow-opacity']))
        style = "QWidget{background-color:" + settingsDict['background-color'] + "; color:" + settingsDict[
            'color'] + ";}"
        self.setStyleSheet(style)
        self.labelIonosphereStat = QLabel()
        self.labelIonosphereStat.setStyleSheet("font: 12px;")
        style = "QWidget{background-color:" + settingsDict['form-background'] + "; color:" + settingsDict[
            'color'] + "; font: 12px}"
        self.tableWidget.setStyleSheet(style)
        fnt = self.tableWidget.font()
        fnt.setPointSize(9)
        self.tableWidget.setFont(fnt)
        self.tableWidget.setRowCount(0)
        self.tableWidget.horizontalHeader().setStyleSheet("font: 12px; width:100%;")
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setHorizontalHeaderLabels(["Time Loc", "Time GMT", "Call", "Freq", " Spot"])
        self.tableWidget.verticalHeader().hide()
        self.tableWidget.cellClicked.connect(self.click_to_spot)
        self.tableWidget.resizeColumnsToContents()
        #self.tableWidget.move(0, 0)
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.labelIonosphereStat)
        self.layout.addWidget(self.tableWidget)
        self.setLayout(self.layout)

        # logForm.test('test')
        self.show()
        self.start_cluster()


    def stop_cluster(self):

        print("stop_cluster:", self.run_cluster.terminate())

    def start_cluster(self):
        self.run_cluster = clusterThread(cluster_window=self, form_window=logForm)
        self.run_cluster.start()


    def click_to_spot(self):
        row = self.tableWidget.currentItem().row()
        freq = self.tableWidget.item(row, 3).text()
        call = self.tableWidget.item(row, 2).text()
        freq = std.std().std_freq(freq)


        '''len_freq = len(freq)
        if len_freq < 8 and len_freq <= 5:
            while len_freq < 7:
                freq +="0"
                len_freq=len(freq)
            freq = "0"+freq
        if len(freq) < 8 and len(freq) > 5 and len(freq) != 7:
            while len_freq<8:
                freq +="0"
                len_freq=len(freq)

        '''
        logForm.set_freq(freq)
        logForm.set_call(call=call)
        if settingsDict['tci'] == 'enable':
            try:
                tci.Tci_sender(settingsDict['tci-server'] + ":" + settingsDict['tci-port']).set_freq(freq)
            except:
                print("Set_freq_cluster: Can't connection to server:", settingsDict['tci-server'], ":",
                      settingsDict['tci-port'])

        #print("click_to_spot: freq:",freq) # Chek point



    def cluster_filter(self, cleanList):
        flag = False
        if len(cleanList) >= 4:
            #print("cluster_filter: len(cleanList)", len(cleanList))
            #print("cluster_filter: inputlist", cleanList)
            #print("cluster_filter: call", cleanList[4])
            #print("cluster_filter: prefix", cleanList[4][0:2])
            if settingsDict['cluster-filter'] == 'enable':
                ### filtering by spot prefix
                filter_by_band = False
                filter_by_spotter_flag = False
                filter_by_prefix_flag = False

                if settingsDict['filter-by-prefix'] == 'enable':
                    list_prefix_spot=settingsDict['filter-prefix'].split(',')
                    if cleanList[4][0:2] in list_prefix_spot:
                        filter_by_prefix_flag = True
                else:
                    filter_by_prefix_flag = True
                ### filtering by prefix spotter
                if settingsDict['filter-by-prefix-spotter'] == "enable":
                    list_prefix_spotter=settingsDict['filter-prefix-spotter'].split(',')
                    if cleanList[2][0:2] in list_prefix_spotter:
                        filter_by_spotter_flag = True
                else:
                    filter_by_spotter_flag = True
                ### filtering by band
                if settingsDict['filter_by_band'] == "enable":
                    list_prefix_spotter = settingsDict['list-by-band'].split(',')
                    freq = std.std().std_freq(cleanList[3])
                    band = std.std().get_std_band(freq)
                    if band in list_prefix_spotter:
                        filter_by_band = True
                else:
                    filter_by_band = True
                #print("cluster_filter: filter_by_prefix_flag:",filter_by_prefix_flag,
                      #"\nfilter_by_spotter_flag:",filter_by_spotter_flag,"\nfilter_by_band", filter_by_band)
                if filter_by_prefix_flag and filter_by_spotter_flag and filter_by_band:
                    flag = True
                else:
                    flag = False


            else:
                flag = True
        return flag

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
        self.setWindowOpacity(float(settingsDict['searchInetWindow-opacity']))
        style = "QWidget{background-color:" + settingsDict['background-color'] + "; color:" + settingsDict[
            'color'] + ";}"
        self.setStyleSheet(style)
        self.show()

    def update_photo(self):
        pixmap = QPixmap("logo.png")
        self.labelImage.setPixmap(pixmap)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    if settingsDict['log-window'] == 'true':
        logWindow = logWindow()
            #Log_window() logWindow()
    if settingsDict['log-search-window'] == 'true':
        logSearch = logSearch()
    if settingsDict['log-form-window'] == 'true':
        logForm = logForm()
    if settingsDict['telnet-cluster-window'] == 'true':
        telnetCluster = telnetCluster()

    if settingsDict['search-internet-window'] == 'true':
        internetSearch = internetSearch()
    if settingsDict['tci'] == 'enable':
           tci_recv = tci.tci_connect(settingsDict, log_form=logForm)
           tci_recv.start_tci()
           #tci_reciever = tci.Tci_reciever(settingsDict['tci-server']+":"+settingsDict['tci-port'], log_form=logForm)
           #tci_reciever.start()


    Adi_file().record_all_qso(list)
    sys.exit(app.exec_())
