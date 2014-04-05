# -*- coding: utf-8 -*-
from math import pi as pi
import wx
import wx.lib.agw.speedmeter as SM
import socket
import time
import re
import os
import rapiro

wildcard = "txt files (*.txt)|*.txt|"    \
           "All files (*.*)|*.*"


HOST = '192.168.1.81'    # The remote host
#HOST = 'rapiro.local'    # The remote host
PORT = 12345              # The same port as used by the server
TIME = 5
MOTION_TIMES = 5
CONNECTED = False
VERSION = '#E'
dist = 0

servo_pos = [90,90,0,130,90,180,50,90,90,90,90,90]
cmd_str = ['S00','S01','S02','S03','S04','S05','S06','S07','S08','S09','S10','S11']
led_str = ['R','G','B']
led_val   = [0,0,255]
#servo_pos_list = []
#led_val_list = []
#time_list = []
frame_tuple = (
(90,90,0,130,90,180,50,90,90,90,90,90,0,0,255,0),
(90,90,0,130,90,180,50,90,90,90,90,90,0,0,255,0),
(90,90,0,130,90,180,50,90,90,90,90,90,0,0,255,0),
(90,90,0,130,90,180,50,90,90,90,90,90,0,0,255,0),
(90,90,0,130,90,180,50,90,90,90,90,90,0,0,255,0),
(90,90,0,130,90,180,50,90,90,90,90,90,0,0,255,0),
(90,90,0,130,90,180,50,90,90,90,90,90,0,0,255,0),
(90,90,0,130,90,180,50,90,90,90,90,90,0,0,255,0)
)
frame_list =list(frame_tuple)
rapiroResponse = ''
index = 0
text_motion = [0,0,0,0,0,0,0,0]
radiobutton = [True,False,False,False,False,False,False,False]

edit_collection = {
    4000:["M-Clear",0],
    4001:["M-Save",1],
#    4002:["M-List",2],
    4003:["M-Play",3],
    4004:["F-Load",4],
    4005:["F-Save",5]
}
action_collection = {
    1000:["Analog", "a,#A6\n"],
    1001:["Foward", "a,#M1\n"],
    1002:["C",      "a,#C\n"],
    1003:["M5",     "a,#M5\n"],
    1004:["M6",     "a,#M6\n"],
    1005:["Left",   "a,#M4\n"],
    1006:["STOP",   "a,#M0\n"],
    1007:["Right",  "a,#M3\n"],
    1008:["M7",     "a,#M7\n"],
    1009:["M8",     "a,#M8\n"],
    1010:["OFF",    "a,#Z\n"],
    1011:["Back",   "a,#M2\n"],
    1012:["Q"  ,    "a,#Q\n"],
    1013:["M9",     "a,#M9\n"],
    1014:["M10",    "a,#M10\n"]
    }
action_collection0 = {
    1000:["Analog", "a,#A6\n"],
    1001:["Foward", "a,#M01\n"],
    1002:["C",      "a,#C\n"],
    1003:["M5",     "a,#M05\n"],
    1004:["M6",     "a,#M06\n"],
    1005:["Left",   "a,#M04\n"],
    1006:["STOP",   "a,#M00\n"],
    1007:["Right",  "a,#M03\n"],
    1008:["M7",     "a,#M07\n"],
    1009:["M8",     "a,#M08\n"],
    1010:["HALT",   "a,#H\n"],
    1011:["Back",   "a,#M02\n"],
    1012:["Q"  ,    "a,#Q\n"],
    1013:["M9",     "a,#M09\n"],
    1014:["M10",    "a,#M10\n"]
    }

servo_collection = {
     2000:[-1],
     2001:[-1],
     2002:[ 0,wx.SL_HORIZONTAL,servo_pos[0],0,180],
     2003:[-1],
     2004:[-1],
     2005:[ 3,wx.SL_HORIZONTAL,servo_pos[3],0,130],
     2006:[ 2,wx.SL_VERTICAL|wx.SL_INVERSE,servo_pos[2],0,180],
     2007:[-1],
     2008:[ 5,wx.SL_VERTICAL,servo_pos[5],0,180],
     2009:[ 6,wx.SL_HORIZONTAL,servo_pos[6],50,180],
     2010:[ 4,wx.SL_HORIZONTAL|wx.SL_INVERSE,servo_pos[4],70,120],
     2011:[-1],
     2012:[ 1,wx.SL_HORIZONTAL,servo_pos[1],0,180],
     2013:[-1],
     2014:[ 7,wx.SL_HORIZONTAL|wx.SL_INVERSE,servo_pos[7],60,110],
     2015:[-1],
     2016:[ 9,wx.SL_HORIZONTAL|wx.SL_INVERSE,servo_pos[9],60,120],
     2017:[-1],
     2018:[11,wx.SL_HORIZONTAL|wx.SL_INVERSE,servo_pos[11],60,120],
     2019:[-1],
     2020:[-1],
     2021:[ 8,wx.SL_HORIZONTAL|wx.SL_INVERSE,servo_pos[8],60,120],
     2022:[-1],
     2023:[10,wx.SL_HORIZONTAL|wx.SL_INVERSE,servo_pos[10],60,120],
     2024:[-1]
}

led_collection = {
    3000:[-1],
    3001:['R',wx.SL_HORIZONTAL, led_val[0], 0, 255, 0,'#FFFFFF','#FF0000'],
    3002:['G',wx.SL_HORIZONTAL, led_val[1], 0, 255, 1,'#FFFFFF','#00FF00'],
    3003:['B',wx.SL_HORIZONTAL, led_val[2], 0, 255, 2,'#FFFFFF','#0000FF'],
    3004:[-1]
}

class resAnalysis:
    def __init__(self, string):
        """
        H: header
        T:time    / t:time(int)
        V:vlotage / v:voltage(int)
        """
        #print string
        self.string = string
        d = re.split('(#?[A-Z][0-9]*)',string)
        self.items = []
        self.H = '#E'
        self.T = 'T000'
        self.t = 0
        self.V = 'V000'
        self.v = 0
        for c in d:
            if c != "":
                self.items.append(c)
                if re.match('T[0-9]*',c):
                    self.T = c
                    self.t = int(re.sub('T','',c))
                if re.match('V[0-9]*',c):
                    self.V = c
                    self.v = int(re.sub('V','',c))
                if re.match('#',c):
                    self.H = c

class mainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,None,wx.ID_ANY,u"Rapiro",size=(600,840))

        self.CreateStatusBar()
        self.SetStatusText("Rapiro")
        self.GetStatusBar().SetBackgroundColour(None)

        root_panel = wx.Panel(self, wx.ID_ANY)

        nb = wx.Notebook(root_panel)
        pnl1 = mainPanel(nb)
        pnl2 = analogPanel(nb)
        pnl3 = wx.Panel(nb, -1)
        nb.AddPage(pnl1, 'Page 1')
        nb.AddPage(pnl2, 'Page 2')
        nb.AddPage(pnl3, 'Page 3')
        #nb.AddPage(host_panel, 'Page 3')


        #StTxt = wx.StaticText(pnl1, -1, 'Text', pos=(20,30))
        root_layout = wx.BoxSizer(wx.VERTICAL)
        root_layout.Add(nb, 1, wx.EXPAND)
        root_panel.SetSizer(root_layout)

class analogPanel(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self,parent,wx.ID_ANY)

        self.timer = wx.PyTimer(self.ClockTimer)
        self.currvalue = 0

        panel = wx.Panel(self, -1)
        sizer = wx.FlexGridSizer(2, 3, 2, 5)

        panel1 = wx.Panel(panel, -1, style=wx.SUNKEN_BORDER)


        self.SpeedWindow1 = SM.SpeedMeter(panel1,
                                            agwStyle=SM.SM_DRAW_HAND|
                                            SM.SM_DRAW_SECTORS|
                                            SM.SM_DRAW_MIDDLE_TEXT|
                                            SM.SM_DRAW_SECONDARY_TICKS
                                            )

        self.SpeedWindow1.SetAngleRange(1*pi/8, 7*pi/8)
        intervals = range(0, 51, 5)
        self.SpeedWindow1.SetIntervals(intervals)
        colours = [wx.WHITE]*10
        self.SpeedWindow1.SetIntervalColours(colours)
        ticks = [str(interval) for interval in intervals]
        self.SpeedWindow1.SetTicks(ticks)
        self.SpeedWindow1.SetTicksColour(wx.BLACK)
        #self.SpeedWindow1.SetNumberOfSecondaryTicks(2)
        self.SpeedWindow1.SetTicksFont(wx.Font(16, wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.SpeedWindow1.SetMiddleText("cm")
        self.SpeedWindow1.SetMiddleTextColour(wx.BLACK)
        self.SpeedWindow1.SetMiddleTextFont(wx.Font(16, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.SpeedWindow1.SetHandColour(wx.Colour(255, 50, 0))
        self.SpeedWindow1.DrawExternalArc(False)
        self.SpeedWindow1.SetSpeedValue(0)

        button1 = wx.Button(panel1, -1, "Start")
        self.stopped = 1
        button1.Bind(wx.EVT_BUTTON, self.click_button1)


        bsizer1 = wx.BoxSizer(wx.VERTICAL)
        hsizer1 = wx.BoxSizer(wx.HORIZONTAL)
        hsizer1.Add(button1, 0, wx.LEFT, 5)
        #hsizer1.Add(stattext1, 1, wx.EXPAND)

        bsizer1.Add(self.SpeedWindow1, 1, wx.EXPAND)
        bsizer1.Add(hsizer1, 0, wx.EXPAND)
        panel1.SetSizer(bsizer1)
        bsizer1.Layout()


        sizer.Add(panel1, 1, wx.EXPAND)

        sizer.AddGrowableRow(0)
        sizer.AddGrowableCol(0)

        panel.SetSizer(sizer)

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(panel, 1, wx.EXPAND)
        self.SetSizer(mainSizer)
        mainSizer.Layout()
        #self.timer.Start(2000)

    def ClockTimer(self):
        global CONNECTED,dist
        command = "a,#A6\n"
        if CONNECTED:
            sendCommand(command)
            rapiroResponse = s.recv(8192)
            if resAnalysis(rapiroResponse).H=="#A6":
                dist = rapiro.a2dist(resAnalysis(rapiroResponse).v)
            else:
                dist = 0


        self.SpeedWindow1.SetMiddleText("%3.2f" % dist)
        self.SpeedWindow1.SetSpeedValue(dist)

    def click_button1(self, event):
        btn = event.GetEventObject()

        if self.stopped == 0:
            self.stopped = 1
            self.timer.Stop()
            btn.SetLabel("Start")
        else:
            self.stopped = 0
            self.timer.Start(2000)
            btn.SetLabel("Stop")

class mainPanel(wx.Panel):

    def __init__(self,parent):
        global text_motion,frame_list, MOTION_TIMES,radiobutton

        wx.Panel.__init__(self,parent,wx.ID_ANY)
        self.text_host = wx.TextCtrl(self,wx.ID_ANY,u"%s" % (HOST),style=wx.TE_RIGHT)
        self.text_port = wx.TextCtrl(self,wx.ID_ANY,u"%s" % (PORT),style=wx.TE_RIGHT)
        self.button_conn = wx.ToggleButton(self,wx.ID_ANY,u"CONNECT",style=wx.TE_RIGHT)
        self.button_conn.Bind(wx.EVT_TOGGLEBUTTON, self.click_button_conn)

        self.text1 = wx.StaticText(self,wx.ID_ANY,'')
        self.text2 = wx.StaticText(self,wx.ID_ANY,'')
        #layout = wx.BoxSizer(wx.HORIZONTAL)

        layout0 = wx.FlexGridSizer(2,1,3,3)
        layout1 = wx.FlexGridSizer(25,5,3,3)
        layout2 = wx.FlexGridSizer(9,3,3,3)
        layout0.Add(layout1, wx.EXPAND)
        layout0.Add(layout2, wx.EXPAND)

        layout1.Add(self.text_host,1,wx.GROW)
        layout1.Add(self.text_port,1)
        layout1.Add(self.button_conn,1)
        layout1.Add(self.text1, 1, wx.GROW)
        layout1.Add(self.text2, 1, wx.GROW)
        #PRISET
        for id, val in action_collection.items():
            b = wx.Button(self,id,val[0],size=(60,25))
            layout1.Add(b ,1,wx.GROW)
            b.Bind(wx.EVT_BUTTON, self.click_action)
        #LED
        for id, val in led_collection.items():
            if val[0] >= 0:
                #label1 = wx.StaticText(self,wx.GROW,u"%s" % val[0],size = (20,20) )
                #label1.SetBackgroundColour(val[6])
                #layout1.Add(label1,flag=wx.SHAPED)
                slider = wx.Slider(self,id,style=val[1]|wx.SL_LABELS)
                slider.SetForegroundColour(val[6])
                slider.SetBackgroundColour(val[7])
                layout1.Add(slider ,1)
                slider.SetMin(val[3])
                slider.SetMax(val[4])
                slider.SetValue(val[2])
                slider.Bind(wx.EVT_SLIDER, self.slider_led)
            else:
                text = wx.StaticText(self,id,'')
                layout1.Add(text, 1, wx.GROW)
        # servo
        for id, val in servo_collection.items():
            if val[0] >= 0:
                #slider = wx.Slider(self,id,val[0],size=(30,25))
                slider = wx.Slider(self,id,style=val[1]|wx.SL_LABELS)
                layout1.Add(slider ,1)
                slider.SetMin(val[3])
                slider.SetMax(val[4])
                slider.SetValue(val[2])
                slider.Bind(wx.EVT_SLIDER, self.slider_servo)
            else:
                text = wx.StaticText(self,id,'')
                layout1.Add(text, 1, wx.GROW)

        #edit
        for id, val in edit_collection.items():
            b = wx.Button(self,id,val[0],size=(60,25))
            layout1.Add(b ,1,wx.GROW)
            b.Bind(wx.EVT_BUTTON, self.click_edit)
        self.label_time = wx.StaticText(self,wx.ID_ANY,u"TIME")
        self.text_time   = wx.TextCtrl(self,wx.ID_ANY,"%d" % (TIME),style=wx.TE_RIGHT)
        layout1.Add(self.label_time,1)
        layout1.Add(self.text_time,1)
        #self.SetSizer(layout1)
        #motion
        label1 = wx.StaticText(self,wx.GROW,u"Repeat",size = (50,20) )
        layout2.Add(label1,flag=wx.SHAPED)
        text_motion_n = wx.TextCtrl(self,wx.ID_ANY,u"%s" % (MOTION_TIMES),style=wx.TE_RIGHT,size=(40,20))
        layout2.Add(text_motion_n,flag=wx.GROW)
        label2 = wx.StaticText(self,wx.GROW,u"",size = (20,20) )
        layout2.Add(label2,flag=wx.SHAPED)
        #self.text_port = wx.TextCtrl(self,wx.ID_ANY,u"%s" % (PORT),style=wx.TE_RIGHT)
        for id in range(8):
            label = wx.StaticText(self,wx.GROW,(u"%s" % id),size = (40,20))
            layout2.Add(label,flag=wx.SHAPED)
            radiobutton[id] = wx.RadioButton(self, 5000+id, "")
            radiobutton[id].Bind(wx.EVT_RADIOBUTTON, self.selected_radiobutton)
            layout2.Add(radiobutton[id],flag=wx.GROW)
            text_motion[id] = wx.TextCtrl(self,id,list2str(frame_list[id]),style=wx.TE_LEFT,size = (380,20))
            #text_motion[id].Enable()
            text_motion[id].Disable()
            layout2.Add(text_motion[id],flag=wx.GROW)
            layout2.AddGrowableCol(id)
        self.SetSizer(layout0)
        radiobutton[0].SetValue(True)

    def selected_radiobutton(self,event):
        global index
        index = event.GetId() - 5000
        pass
    def click_edit(self, event):
        global frame_list,rapiroResponse, index, text_motion, radiobutton
        try:
            edit = edit_collection[event.GetId()]
        except:
            pass
        #print edit

        if edit[0] == 'M-Save':
            tmp_x = []
            for x in servo_pos:
                tmp_x.append(x)
            for x in led_val:
                tmp_x.append(x)
            tmp_x.append(int(self.text_time.GetValue()))
            frame_list[index] = tmp_x
            text_motion[index].SetValue(list2str(tmp_x))
            index +=1
            if index > 7:
                index = 0
            radiobutton[index].SetValue(True)

        elif edit[0] == 'M-Clear':
            clearMotion()
        elif edit[0] == 'M-List':
            print frame_list
        elif edit[0] == 'M-Play':
            for m in range(5):
                for frame in  frame_list:
                   #print frame
                    if frame[15]==0:
                        break
                    #print servo_step, led_step
                    play_cmd = "a, #P"
                    for n, pos in zip(range(12), frame[0:12]):
                        play_cmd += "S"  + str(n).zfill(2) + "A" + str(pos).zfill(3)
                    for led, bright in zip(['R','G','B'], frame[12:15]):
                        play_cmd += led + str(bright).zfill(3)
                    play_cmd += "T" + str(frame[15]).zfill(3) + "\n"
                    #print play_cmd
                    sendCommand(play_cmd)
                    rapiroResponse = s.recv(8192)
                    res = resAnalysis(rapiroResponse)
                    w = res.t
                    #print w
                    while(w > 0 ):
                        time.sleep(0.2)
                        sendCommand("a, #Q\n")
                        #sendCommand("a, #C\n")
                        rapiroResponse = s.recv(8192)
                        res = resAnalysis(rapiroResponse)
                        w = res.t
                        #print rapiroResponse, res.t
        #command = "a, #PS"+str(sv[0]).zfill(2)+"A"+angle+"T001\n"

        elif edit[0] == 'F-Save':
            self.OnButton2()
        elif edit[0] == 'F-Load':
            self.OnButton()

    def OnButton(self):
        #self.log.WriteText("CWD: %s\n" % os.getcwd())

        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultDir=os.getcwd(),
            defaultFile="",
            wildcard=wildcard,
            style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR
            )

        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths()

            for path in paths:
                self.loadFile(path)
        dlg.Destroy()



    def OnButton2(self):
        #self.log.WriteText("CWD: %s\n" % os.getcwd())

        dlg = wx.FileDialog(
            self, message="Save file as ...", defaultDir=os.getcwd(),
            defaultFile="", wildcard=wildcard, style=wx.SAVE
            )

        dlg.SetFilterIndex(2)

        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.saveFile(path)

        dlg.Destroy()

    def saveFile(self, path):
        global frame_list
        #print frame_list
        f = open(path,'w')
        for  frame in frame_list:
            n = 0
            for c in frame:
                if n != 0:
                    f.write(", ")
                f.write("%d"% c)
                n += 1
            f.write("\n")
        f.close()

    def loadFile(self, path):
        global frame_list,led_val_list,time_list
        clearMotion()
        #print path
        f = open(path,'r')
        for i, line in zip(range(8), f):
            d = re.split('[,\n]',line)
            val =map(int,d[:16])
            frame_list[i] = val
            text_motion[i].SetValue(list2str(val))
            #print d
            #print frame_list
        f.close()



    def click_button_conn(self, event):
        st = self.button_conn.GetValue()
        if (st):
            self.button_conn.SetLabel(u'DISCONNECT')
            self.connectServer()
        else:
            self.button_conn.SetLabel(u'CONNECT')
            self.close()
        pass

    def connectServer(self):
        global s, CONNECTED, VERSION
        HOST = self.text_host.GetValue()
        PORT = self.text_port.GetValue()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((HOST, int(PORT)))
            CONNECTED = True
            VERSION = checkVersion()
            frame.SetStatusText("Version value is " + str(VERSION))

        except:
            self.button_conn.SetLabel(u'CONNECT')
            self.button_conn.SetValue(False)
            CONNECTED = False

    def close(self):
        global servo_collection
        s.close()

    def click_action(self, event):
        global VERSION, dist
        try:
            #print VERSION
            if VERSION == '#E':
                act = action_collection[event.GetId()]
            else:
                act = action_collection0[event.GetId()]
        except:
            pass
        if CONNECTED:
            sendCommand(act[1])
            rapiroResponse = s.recv(8192)
            if resAnalysis(rapiroResponse).H=="#A6":
                dist = rapiro.a2dist(resAnalysis(rapiroResponse).v)
            else:
                dist = 0
            frame.SetStatusText("Received value is %s %4.2f" %( str(rapiroResponse), dist))
        else:
            frame.SetStatusText("not connect" )

    def slider_led(self, event):
        color = led_collection[event.GetId()]
        obj = event.GetEventObject()
        brightNum=obj.GetValue()
        bright=str(brightNum).zfill(3)
        command = "a, #P"+str(color[0])+bright+"T002\n"
        #print command, event.GetId()
        if CONNECTED:
            sendCommand(command)
            rapiroResponse = s.recv(8192)
            frame.SetStatusText("Received value is " + str(rapiroResponse))
        led_val[color[5]] = brightNum

    def slider_servo(self,event):
        sv = servo_collection[event.GetId()]
        obj = event.GetEventObject()
        angleNum = obj.GetValue()
        angle=str(angleNum).zfill(3)
        command = "a, #PS"+str(sv[0]).zfill(2)+"A"+angle+"T001\n"
        #print command, event.GetId()
        if CONNECTED:
            sendCommand(command)
            rapiroResponse = s.recv(8192)
            frame.SetStatusText("Received value is " + str(rapiroResponse))
        servo_pos[sv[0]] = angleNum

def list2str(l):
    s = ''
    n = 0
    for c in l:
        if n != 0:
            s+=", "
        s+=("%d"% c)
        n += 1
    return(s)

def clearMotion():
    global frame_list, index, text_motion
    for i,val in zip(range(8), frame_tuple):
        text_motion[i].SetValue(list2str(val))
    frame_list = list(frame_tuple)
    index = 0;

def checkVersion():
    sendCommand("a, #V\n")
    v = s.recv(8192)
    return(v)
def sendCommand(cmd):
    try:
        s.send(cmd)
    except:
        pass
#---------------------------------------------------------------------------

if __name__ == "__main__":
    application = wx.App()
    frame = mainFrame()
    frame.Show()
    application.MainLoop()
