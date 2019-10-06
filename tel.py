# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8

import sys
import telnetlib


def telnet_cluster(call, host, port):
    HOST = host
    PORT = port

    telnetObj = telnetlib.Telnet(HOST, PORT)

    message = (call + "\n").encode('ascii')
    telnetObj.write(message)
    message2 = (call + "\n").encode('ascii')
    telnetObj.write(message2)
    splitString = []
    cleanList = []
    i = 0
    print('Starting Telnet cluster:', host, ':', port, '\nCall:', call, '\n\n')
    while 1:
        output_data = telnetObj.read_some()

        if output_data != '':
            #print(output_data[0:2])
            if output_data[0:2].decode('utf-8') == "DX":
                # print (output[0:2])
                splitString = output_data.decode('utf-8').split(' ')
                count_chars = len(splitString)
                for i in range(count_chars):
                    if splitString[i] != '':
                        cleanList.append(splitString[i])

                print(cleanList)
                print(output_data)
            elif output_data[0:3] == "WWV":
                print("Ionosphere status: ", output_data)
            del cleanList[0:len(cleanList)]


# print (output)
# telnetObj.close()
call = input("Enter callsign: ")
telnet_cluster(call, "dxfun.com", "8000")
