#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import serial
import os
import time
import datetime
import threading

_str = ''
if os.name == 'posix':
    com = serial.Serial('/dev/ttyAMA0', 57600, timeout = 0.05)
else:
    com = sys.stdout

def a2dist(v):
    d = 26.59*pow(v/1024.0*5.0,-1.209)
    return(d)

def rxData():
    global _str
    while (1):
        n = com.inWaiting()
        #print n, _str
        if n > 0:
            _str += com.read(n)

def command(data):
    inst = data.split(',')
    r = ''
    try:
        t = inst[0]
        s = inst[1]
    except:
        t = 'x'
        s = 'Not define'
    if t == 'a':
        """
        Arduino
        """
        com.write(s)
        r = com.readline()
    elif t == 'p':
        """
        Raspberry pi
        """
        os.system(s)
    else:
        pass
    return(t, s, r)

def main():
    #print(command('a,#M0'))
    #print(command('a,#Z'))
    #print(command('a,#PS02A090S05A000T001'))
    print(command('a,#M0'))
    print(command('a,#Q'))
    print(command('a,#A6'))
    #print(command('a,#A1'))
    #print(command('a,#A2'))
    #print(command('a,#A3'))
    #print(command('a,#A4'))
    #print(command('a,#A5'))
    print(command('a,#A6'))
    #print(command('a,#A7'))
    print(command('a,#C'))
    print(command('a,#D'))

if __name__ == '__main__':
    #t1 = threading.Thread(target=rxData)
    #t1.setDaemon(True)
    #t1.start()
    main()
