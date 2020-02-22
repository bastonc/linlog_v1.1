# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8

import urllib
import std
import requests
from bs4 import BeautifulSoup
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QPixmap
# import urllib.request
# import urllib.parse
from urllib.request import urlretrieve
from urllib.parse import quote
from PyQt5.QtCore import QThread
from PyQt5 import QtCore
from PyQt5.QtWidgets import  QWidget
import main


class internetWorker(QThread):

    def __init__(self, window, callsign, settings, parrent=None):
        super().__init__()
        self.internet_search_window = window
        self.callsign = callsign
        self.settings = settings

    def run(self):
        # print (self.callsign)
        info_from_internet_array = internetWorker.get_image_from_server(self)
        print (info_from_internet_array)
        pixmap = QPixmap(info_from_internet_array.get('img'))
        pixmap_resized = pixmap.scaled(int(self.settings['image-width']),
                                       int(self.settings['image-height']),
                                       QtCore.Qt.KeepAspectRatio)
        self.internet_search_window.labelImage.setPixmap(pixmap_resized)
        # return info_from_internet_array

    def get_image_from_server(self):
        '''
        метод загружает изображение с qrz.com
        принимает callsign - позывной
        '''
        url_found = "https://www.qrz.com/lookup"
        print(self.callsign)
        parameter_request = "tquery=" + self.callsign + "&mode: callsign"
        parameter_to_byte = bytearray(parameter_request, "utf-8")
        data_dictionary = {}

        response = urllib.request.urlopen(url_found, parameter_to_byte)
        html = response.read().decode("utf-8")
        soup = BeautifulSoup(html, 'html.parser')
        try:
            img = soup.find(id="mypic")

            urllib.request.urlretrieve(img['src'], "image/" + self.callsign + ".jpg")
            data_dictionary.update({'img': "image/" + self.callsign + ".jpg"})
            print(data_dictionary)
        except Exception:
            print("Exception")

        return data_dictionary


class Eqsl_services (QThread):

    def __init__(self, settingsDict, recordObject, std, parent_window):
        super().__init__()
        self.recordObject = recordObject
        self.settingsDict = settingsDict
        self.std = std
        self.parrent_window = parent_window

    def send_qso_to_qrz(self):
        server_url_post = 'https://logbook.qrz.com/api'
        key_account = "KEY=81FE-08CA-D97D-8709&"
        action = "ACTION=INSERT&ADIF=<band:3>80m<mode:3>SSB<call:5>RN6XC<qso_date:8>20140121<station_callsign:6>UR4LGA<time_on:4>0346<eor>"
        print ("key+action", key_account + action)
        response = requests.post(server_url_post, data=key_account + action)

        print ("send_to_qrz", response.text)

    def run(self):

        api_url_eqsl = 'https://www.eQSL.cc/qslcard/importADIF.cfm?ADIFData=LinLog upload'
        data_qso_string = '<BAND:'+str(len(self.recordObject['BAND']))+'>'+str(self.recordObject['BAND'])+' <CALL:'+str(len(self.recordObject['CALL']))+'>'+str(self.recordObject['CALL'])+' <MODE:'+str(len(self.recordObject['MODE']))+'>'+str(self.recordObject['MODE'])+' <QSO_DATE:'+str(len(self.recordObject['QSO_DATE']))+'>'+str(self.recordObject['QSO_DATE'])+' <RST_RCVD:'+str(len(self.recordObject['RST_RCVD']))+'>'+str(self.recordObject['RST_RCVD'])+' <RST_SENT:'+str(len(self.recordObject['RST_SENT']))+'>'+str(self.recordObject['RST_SENT'])+' <TIME_ON:'+str(len(self.recordObject['TIME_ON']))+'>'+str(self.recordObject['TIME_ON'])+' <EOR>'
        data_string_code_to_url = urllib.parse.quote(data_qso_string)
        user_pasword_eqsl = '&EQSL_USER='+self.settingsDict['eqsl_user']+'&EQSL_PSWD='+self.settingsDict['eqsl_password']
        #data_qso_string = 'ADIFData=LinLog%20upload%20%3CBAND%3A'+str(len(band))+'%3AC%3E'+str(band)+'%20%2D%20%3CCALL%3A'+str(len(call))+'%3AC%3'+str(call)+'%20%3CMODE%3A'+str(len(mode))+'%3AC%3E'+str(mode)+'%20%3CQSO%5FDATE%3A'+str(len(qso_date))+'%3AD%3E'+str(qso_date)+'%20%3CRST%5FRCVD%3A'+str(len(rst_rsvd))+'%3AC%3E'+str(rst_rsvd)+'%20%3CRST%5FSENT%3A'+str(len(rst_send))+'%3AC%3E'+str(rst_send)+'%20%2D%20%3CTIME%5FON%3A'+str(len(time_on))+'%3AC%3E'+str(time_on)+'%20%3CEOR%3E&EQSL_USER='+self.settingsDict['eqsl_user']+'&EQSL_PSWD='+self.settingsDict['eqsl_password']
        print ("end_qso_to_eqsl", api_url_eqsl+data_string_code_to_url)

        request_eqsl = requests.get(api_url_eqsl+data_string_code_to_url+user_pasword_eqsl)

        if request_eqsl.status_code != 200:

            std.std().message("Can't send to eQSL", "")
            print("request_eqsl.status_code", request_eqsl.status_code)
        else:
            soup = BeautifulSoup(request_eqsl.text, 'html.parser')
            response = soup.body.contents[0]
            print ("SOUP", soup.body.contents[0])
            if (response.find('Warning')!= -1) or (response.find('Error')!= -1):
                message = QMessageBox()
                #message.setFixedHeight(200)
                #message.setGeometry(500, 300, 1000, 500)
                message.setStyleSheet("font: 12px;")
                message.setWindowTitle("Warning!")
                message.setText("Can't send to eQSL.cc")
                message.setInformativeText(soup.body.contents[0])
                message.setStandardButtons(QMessageBox.Ok)
                message.exec_()
            #print(request_eqsl.text)
        


        #request_eqsl = requests.get(
         #   'https://www.eQSL.cc/qslcard/importADIF.cfm?ADIFData=LinLog%20upload%20%3CADIF%5FVER%3A4%3E1%2E00%20%3CEOH%3E%20%3CBAND%3A3%3AC%3E30M%20%2D%20%3CCALL%3A6%3AC%3EWB4WXX%20%3CMODE%3A3%3AC%3ESSB%20%3CQSO%5FDATE%3A8%3AD%3E20010503%20%3CRST%5FRCVD%3A2%3AC%3E52%20%3CRST%5FSENT%3A2%3AC%3E59%20%2D%20%3CTIME%5FON%3A6%3AC%3E122500%20%3CEOR%3E&EQSL_USER=ur4lga&EQSL_PSWD=a9minx3m')

