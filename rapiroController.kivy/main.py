import sys
import socket
import time
import re
import os
#import rapiro
import kivy
kivy.require('1.0.5')
from kivy.uix.floatlayout import FloatLayout
from kivy.app import App
from kivy.properties import OptionProperty, ObjectProperty, StringProperty
from kivy.uix.slider import Slider

TIME = 5
MOTION_TIMES = 5
CONNECTED = False
VERSION = '#E'
dist = 0

class Controller(FloatLayout):
    def do_connect(self, *arg):
        global s, CONNECTED
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if arg[0] == 'CONN':
            HOST = arg[1]
            PORT = arg[2]
            try:
                s.connect((HOST, int(PORT)))
                CONNECTED = True
                #VERSION = checkVersion()
            except:
                CONNECTED = False
        elif CONNECTED:
            s.close()
            CONNECTED = False
        print arg


    def do_action(self, *cmd):
        global VERSION, dist
        try:
            act = cmd[0]
        except:
            pass
        if CONNECTED:
            sendCommand(act)
            rapiroResponse = s.recv(8192)
            #if resAnalysis(rapiroResponse).H=="#A6":
            #    dist = rapiro.a2dist(resAnalysis(rapiroResponse).v)
            #else:
            #    dist = 0

    def do_slide(self, servo, angle, rev):
        if rev < 0:
            angle = 180 - angle
        cmd = 'a, #P'+servo+'A'+str(angle).zfill(3)+'T001\n'
        if CONNECTED:
            sendCommand(cmd)
            rapiroResponse = s.recv(8192)
            print cmd

    def on_pause(self):
        return True

def checkVersion():
    global s
    sendCommand( "a, #V\n")
    v = s.recv(8192)
    return(v)
def sendCommand(cmd):
    global s
    try:
        s.send(cmd)
    except:
        pass


class ControllerApp(App):
    def select(self, case):
        pass

    def build(self):
        self.root = Controller()

    def on_start(self):
        print 'start'
    def on_stop(self):
        print 'stop'
    def on_pause(self):
        print 'pause'
if __name__ == '__main__':
    ControllerApp().run()
