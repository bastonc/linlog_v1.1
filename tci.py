#!/usr/bin/python3
# -*- coding: utf-8 -*-

import websocket
import time
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QApplication

class tci_connect:

    def __init__(self, settingsDict, log_form, parent=None):
        super().__init__()
        self.settingsDict = settingsDict
        self.log_form = log_form
        self.settingsDisct = settingsDict



    def start_tci(self, host, port):

        self.tci_reciever = Tci_reciever(host + ":" + port,
                                         log_form=self.log_form)

        self.tci_reciever.set_flag("run")
        self.tci_reciever.start()
        print(self.settingsDict['tci-server'],
              self.settingsDict['tci-port'])
        print("Tci start:", self.tci_reciever.currentThreadId())

    def stop_tci(self):
        print ("Tci stop 1", self.tci_reciever.currentThreadId())
        self.tci_reciever.set_flag("stop")
        if self.tci_reciever.isFinished():
            print("Tci stop 2", self.tci_reciever.currentThreadId())
        #self.log_form.set_tci_stat(' ')

class Tci_reciever(QThread):

    def __init__(self, uri, log_form, parent=None):
        super().__init__()
        self.uri = uri
        self.log_form = log_form
        self.ws = websocket.WebSocket()

    def set_flag(self, flag):
        print("set_flag:", flag)
        self.flag = flag


    def run(self):

        while self.flag == "run":
            try:

                self.ws.connect(self.uri)
                self.log_form.set_tci_stat('•TCI')

                break
                #time.sleep(3)
            except Exception:
                #self.log_form.set_tci_label_found()
                print("Tci_reciever: Except connection")
                self.log_form.set_tci_stat('--', "#ff5555")
                time.sleep(2)

                continue
        while self.flag == "run":
            try:
                #print("Connect to ")
                reciever = self.ws.recv()
                #print(reciever)
                tci_string=reciever.split(":")
                if tci_string[0] == 'vfo':
                    values = tci_string[1].split(",")
                    if values[1] == '0' and values[0] == '0':

                        self.log_form.set_freq(values[2].replace(';', ''))


                        #print("Частота:", values[2])
                if tci_string[0] == 'protocol':
                    values = tci_string[1].replace(',', ' ')
                    values = values.replace(";", "")
                    self.log_form.set_tci_stat('•TCI: '+ values)

                if tci_string[0] == 'modulation':
                     values = tci_string[1].split(",")
                     if values[0] == '0':
                         self.log_form.set_mode_tci(values[1].replace(';', ''))



                time.sleep(0.002)
            except:
                print("Tci_reciever: Exception in listen port loop")
                self.log_form.set_tci_stat(' ')
                #self.log_form.set_tci_label_found()
                try:
                    self.ws.close()
                    self.ws = websocket.WebSocket()
                    self.ws.connect(self.uri)
                    self.log_form.set_tci_stat("•TCI")

                except:
                    time.sleep(2)
                    self.log_form.set_tci_label_found()
                #time.sleep(2)
                continue
        else:
            self.ws.close()


class Tci_sender (QApplication):

    def __init__(self, uri):
        try:
         self.uri = uri
         self.ws = websocket.WebSocket()
         self.ws.connect(self.uri)
         self.ws.send("READY;")

        except:
            self.log_form.set_tci_stat('Check')
            print("Can't connect to Tci_sender __init__:", uri)





    def send_command(self, string_command):
        self.ws.send(string_command)

    def set_freq(self, freq):
        print ("set_freq:", freq)
        freq_string=str(freq)
        if len(str(freq))<8 and len(str(freq))>=5:
            freq_string=str(freq)+"00"
        if len(str(freq))<5:
            freq_string=str(freq)+"000"
        string_command = "VFO:0,0,"+str(freq_string)+";"
        self.ws.send(string_command)

 ### spots

    def set_spot(self, call, freq, color="12711680"):
        string_command = "SPOT:"+str(call)+", ,"+str(freq)+","+color+", ;"
        self.ws.send(string_command)

    def del_spot(self, call):
        string_command = "SPOT_DELETE:"+str(call)+";"
        self.ws.send(string_command)

    def change_color_spot(self, call, freq, color="21711680"):
        string_command = "SPOT_DELETE:"+str(call)+";"
        self.ws.send(string_command)
        string_command = "SPOT:"+str(call)+", ,"+str(freq)+","+color+", ;"
        self.ws.send(string_command)

##########

    def set_mode(self, reciever, mode):
        string_command = "MODULATION:"+str(reciever)+","+str(mode)+";"
        self.ws.send(string_command)

