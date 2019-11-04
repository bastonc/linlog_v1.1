#!/usr/bin/python3
# -*- coding: utf-8 -*-

import websocket
import time
import main
import sys
#from main import logForm
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QApplication


class Tci_reciever(QThread):

    def __init__(self, uri, log_form, parent=None):
        super().__init__()
        self.uri=uri
        self.log_form = log_form






    def run(self):
        while 1:
            try:
                self.ws = websocket.WebSocket()
                self.ws.connect(self.uri)
                break
                time.sleep(3)
            except:
                time.sleep(2)
                continue
        while 1:
            try:
                reciever = self.ws.recv()
                print(reciever)
                tci_string=reciever.split(":")
                if tci_string[0] == 'vfo':
                    values = tci_string[1].split(",")
                    if values[1]=='0' and values[0]=='0':

                        self.log_form.set_freq(values[2].replace(';', ''))

                        print("Частота:", values[2])
                time.sleep(0.002)
            except:
                print("Tci_reciever: Exception in listen port loop")
                try:
                    self.ws = websocket.WebSocket()
                    self.ws.connect(self.uri)

                except:
                    time.sleep(2)
                #time.sleep(2)
                continue


class Tci_sender (QApplication):

    def __init__(self, uri):
        try:
         self.ws = websocket.WebSocket()
         self.ws.connect(uri)
         self.ws.send("READY;")
        except:
            print("Can't connect to Tci_sender __init__:", uri)


    def send_command(self, string_command):
        self.ws.send(string_command)

    def set_freq(self, freq):
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



'''

if __name__ == '__main__':
    app = QApplication(sys.argv)
    tci_reciever = Tci_reciever("ws://localhost:40001")
    tci_reciever.start()
    tci = Tci_sender("ws://localhost:40001")
    #tci.send_command("SPOT:UR4LGA,SSB,7110000,16711680, Good Modulation;")
    tci.set_freq(7110000)

    tci.set_spot("UR4LG", "7112000")
    time.sleep(7)
    tci.change_color_spot("UR4LG", 7112000)
    time.sleep(7)
    tci.set_mode(0, "lsb")
    tci.del_spot("UR4LG")
    sys.exit(app.exec_())

# get_all()


try:
    import thread
except ImportError:
    import _thread as thread
import time
from PyQt5.QtCore import QThread

class Tci (QThread):

    def __init__(self):
        websocket.enableTrace(True)
        self.ws = websocket.WebSocketApp("ws://localhost:40001",
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close)
        #self.on_message()
        self.ws.on_open=self.on_send_tci_command
        self.ws.run_forever()


    def on_message(self, message):

        #vfo:0,0,14175000;
        print(message)

        #list = self.ws.on_message.split(':')
     #  if len(list) > 1:
            #string[1].find(',') != -1:
      #      string2 = list[1].split(',')
      #      list[1] = string2
        #print(list)

    def on_error(ws, error):
        print(error)

    def on_close(ws):
        print("### closed ###")

    def on_send_tci_command(self, command_string='START;'):

        #print('on_send_tci_command')
        self.ws.send(command_string)
        #self.ws.close()

    def on_open(ws):
        pass
        #def run(*args):
            #for i in range(3):
             #   time.sleep(1)
             #   ws.send("")
            #time.sleep(1)
           # ws.close()
           # print("thread terminating...")
        #thread.start_new_thread(run, ())





        
                                    #on_message=on_message,
                                    #on_error=on_error,
                                    #on_close=on_close
        

if __name__ == "__main__":
    tci = Tci
    #tci().on_message()
    tci().on_send_tci_command("SS")

    #ws.on_open = on_open
    #ws.on_send_tci_command = on_send_tci_command()


### ws://echo.websocket.org/
'''
