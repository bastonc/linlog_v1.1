# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8

import urllib
from bs4 import BeautifulSoup
from PyQt5.QtGui import QPixmap
#import urllib.request
#import urllib.parse
from urllib.request import urlretrieve
from PyQt5.QtCore import QThread
from PyQt5 import QtCore
import main

class internetWorker (QThread):


    def __init__(self, window, callsign, settings, parrent=None):
        super().__init__()
        self.internet_search_window = window
        self.callsign = callsign
        self.settings=settings

    def run(self):
        #print (self.callsign)
        info_from_internet_array = internetWorker.get_image_from_server(self)
        print (info_from_internet_array)
        pixmap=QPixmap(info_from_internet_array.get('img'))
        pixmap_resized = pixmap.scaled(int(self.settings['image-width']),
                                       int(self.settings['image-height']),
                                       QtCore.Qt.KeepAspectRatio)
        self.internet_search_window.labelImage.setPixmap(pixmap_resized)
        #return info_from_internet_array

    def get_image_from_server(self):
        '''
        метод загружает изображение с qrz.com
        принимает callsign - позывной
        '''
        url_found="https://www.qrz.com/lookup"
        print(self.callsign)
        parameter_request = "tquery=" + self.callsign + "&mode: callsign"
        parameter_to_byte = bytearray(parameter_request, "utf-8")
        data_dictionary = {}

        response = urllib.request.urlopen(url_found, parameter_to_byte)
        html = response.read().decode("utf-8")
        soup = BeautifulSoup(html, 'html.parser')
        try:
            img = soup.find(id="mypic")

            urllib.request.urlretrieve(img['src'], "image/"+self.callsign + ".jpg")
            data_dictionary.update({'img': "image/"+self.callsign + ".jpg"})
            print(data_dictionary)
        except Exception:
            print("Exception")




        return data_dictionary
