# -*- coding: utf-8 -*-

__author__ = 'virtual'

from datetime import datetime, timedelta
import time
import serial


class RS232(object):

    port_config = {
        'speed': 115200,
        'stop': 1,
        'check': 0, # n
        'data': 8,
        'timeout': 50,
    }

    def __init__(self, port='/dev/ttyUSB1', speed=9600):
        ser = serial.Serial(
            port=port,
            baudrate=speed,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS
        )

        ser.isOpen()
        self.ser = ser

    def __del__(self):
        self.ser.close()

    def send(self, msg_str):
        #print 'send data:', str(msg_str)
        self.ser.writeTimeout = 50
        if type(msg_str) == list:
            for el in msg_str:
                self.ser.write(el)
        else:
            self.ser.write(msg_str)

    def recv(self, timeout):
        out = []
        w_time = timeout
        while w_time > 0:
            #self.ser.timeout = timeout
            while self.ser.inWaiting() > 0:
                out.append(self.ser.read(1))
            if len(out) > 0:
                break
            w_time -= 50
            #print w_time
            time.sleep(0.05)

        #print 'recv data:', out
        if len(out) > 0:
            return out
        else:
            return None
