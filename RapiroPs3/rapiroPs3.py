#!/usr/bin/env python
import sys
import serial
import os
import time
import datetime

file = open('/dev/input/js0', 'r')
com = serial.Serial('/dev/ttyAMA0', 57600, timeout = 10)
data = []
MAXANGLE    = 180   #120
COEF1       = 1.42  #2.13   256/MAXANGLE
COEF2       = 1.66  #1.66
LLRLIMIT    =  70   #20     #S06    Left analog stick Left - Right
LUDLIMIT    = 180   #120    #S05    Left analog stick UP - DOWN
RLRLIMIT    = 110   #100    #S03    Right analog stick Left - Right
RUDLIMIT    =   0           #S02    Right analog stick UP - DOWN
LLR = LLRLIMIT
LUD = LUDLIMIT
RLR = RLRLIMIT
RUD = RUDLIMIT

mode = "wait"
before_time = 0
now_time = 0

state4 = {
    '00': 'released',
    '01': 'pressed'
}
tconv = {
    'released':'rt',
    'pressed':'pt'
}
mode6 = {
    '01':'button',
    '02':'analog',
    '81':'',
    '82':''
}
button7 = {
    '00':{'type':'SELECT',  'pressed':'#PR255G000B000T001', 'pt':0,     'released':'#PR255G000B000T001','rt':0},
    '01':{'type':'L3',      'pressed':'#M0',                'pt':0,     'released':'#M0',               'rt':0},
    '02':{'type':'R3',      'pressed':'#M0',                'pt':0,     'released':'#M0',               'rt':0},
    '03':{'type':'START',   'pressed':'#Z',                 'pt':0,     'released':'#Z',                'rt':0},
    '04':{'type':'UP',      'pressed':'#M1',                'pt':0,     'released':'#M0',               'rt':0},
    '05':{'type':'RIGHT',   'pressed':'#M3',                'pt':0,     'released':'#M0',               'rt':0},
    '06':{'type':'DOWN',    'pressed':'#M2',                'pt':0,     'released':'#M0',               'rt':0},
    '07':{'type':'LEFT',    'pressed':'#M4',                'pt':0,     'released':'#M0',               'rt':0},
    '08':{'type':'L2',      'pressed':'#PS07A070T001',      'pt':0.11,  'released':'#PS07A090T001',     'rt':0.11},
    '09':{'type':'R2',      'pressed':'#PS04A110T001',      'pt':0.11,  'released':'#PS04A090T001',     'rt':0.11},
    '0A':{'type':'L1',      'pressed':'#PS07A110T001',      'pt':0.11,  'released':'#PS07A090T001',     'rt':0.11},
    '0B':{'type':'R1',      'pressed':'#PS04A070T001',      'pt':0.11,  'released':'#PS04A090T001',     'rt':0.11},
    '0C':{'type':'TRIANGLE','pressed':'#M5',                'pt':0,     'released':'#M0',               'rt':0},
    '0D':{'type':'CIRCLE',  'pressed':'#M6',                'pt':0,     'released':'#M0',               'rt':0},
    '0E':{'type':'CROSS',   'pressed':'#M7',                'pt':0,     'released':'#M0',               'rt':0},
    '0F':{'type':'SQUARE',  'pressed':'#M8',                'pt':0,     'released':'#M0',               'rt':0}
    }

stick7 = {
    '00':[COEF1,-MAXANGLE, -1, -MAXANGLE/2, COEF2,  0, 180,  70],
    '01':[COEF1,        0,  1,           0,  2.00,  0, 180,   0],
    '02':[COEF1,-MAXANGLE, -1,           0, COEF2,  0, 110,   0],
    '03':[COEF1,-MAXANGLE, -1, -MAXANGLE/2,  2.00,  0, 180,   0]
}


def timeSleep(t):
    if t>0:
        time.sleep(t)
def a_calc(x, c):
    x = 255 & (x + 128)
    y = (int(x/c[0]) + c[1] ) * c[2]
    z = int((y + c[3]) * c[4] + c[5])
    if z >= c[6]:
        z = c[6]
    elif z <= c[7]:
        z = c[7]
    return(z)
def PS(RUD, RLR, LUD, LLR):
    s = "#PS02A" + str(RUD).zfill(3) + "S03A" + str(RLR).zfill(3) + "S05A" + str(LUD).zfill(3) + "S06A" + str(LLR).zfill(3) + "T002\r\n"
    return (s)

while 1:
    for character in file.read(1):
        data += ['%02X' % ord(character)]
        if len(data) == 8:
            if mode6[data[6]] == 'button':
                #print(data)
                mode    = mode6[data[6]]
                state   = state4[data[4]]
                type    = button7[data[7]]['type']
                act     = button7[data[7]][state]
                actWait = button7[data[7]][tconv[state]]
                sys.stdout.write('You %s the %s %s. action=%s\n' % (state, type, mode, act))
                timeSleep(actWait)
                com.write(act)
            elif mode6[data[6]] == 'analog':
                now = datetime.datetime.now()
                now_time = now.minute * 60000 + now.second * 1000 + now.microsecond/1000
                a_data = int(data[5],16)

                if data[7] == '00': #Left stick L-R     PS06
                    LLR = a_calc(a_data, stick7[data[7]])
                    joy = True

                elif data[7] == '01':   #Left stick U-D     PS05
                    LUD = a_calc(a_data, stick7[data[7]])
                    joy = True

                elif data[7] == '02':   #Right stick L-R    PS03
                    RLR = a_calc(a_data, stick7[data[7]])
                    joy = True

                elif data[7] == '03':   #Right stick U-D    PS02
                    RUD = a_calc(a_data, stick7[data[7]])
                    joy = True

                else:
                    joy = False
                dif = now_time - before_time
                if dif > 110 and joy == True:
                    com.write(PS(RUD,RLR,LUD,LLR))
                    com.write("ms : " + str(dif) + "\r\n")
                    now = datetime.datetime.now()
                    before_time = now.minute * 60000 + now.second * 1000 + now.microsecond/1000
            sys.stdout.flush()
            data = []
    now = datetime.datetime.now()
    j_time = now.minute * 60000 + now.second * 1000 + now.microsecond/1000
    dif = j_time - before_time
    if dif > 200 and mode == "analog":
        com.write(PS(RUD,RLR,LUD,LLR))
        now = datetime.datetime.now()
        before_time = now.minute * 60000 + now.second * 1000 + now.microsecond/1000
sys.stdout.flush()
data = []