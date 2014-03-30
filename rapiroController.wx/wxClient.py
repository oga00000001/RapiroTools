# -*- coding: utf-8 -*-

import wx
import socket
import time
import re
import os

wildcard = "txt files (*.txt)|*.txt|"    \
           "All files (*.*)|*.*"


HOST = '192.168.1.81'    # The remote host
#HOST = 'rapiro.local'    # The remote host
PORT = 12345              # The same port as used by the server
TIME = 1
MOTION_TIMES = 5
CONNECTED = False
VERSION = '#E'

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
    1000:["Analog", "a,#A06\n"],
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
    3000:['R',wx.SL_HORIZONTAL, led_val[0], 0, 255, 0,'#FFFFFF','#FF0000'],
    3001:['G',wx.SL_HORIZONTAL, led_val[1], 0, 255, 1,'#FFFFFF','#00FF00'],
    3002:['B',wx.SL_HORIZONTAL, led_val[2], 0, 255, 2,'#FFFFFF','#0000FF']
}





class resAnalysis:
    def __init__(self, string):
        #print string
        self.string = string
        d = re.split('(#?[A-Z][0-9]*)',string)
        self.items = []
        self.SH = '#E'
        self.T = 'T000'
        self.t = 0
        for c in d:
            if c != "":
                self.items.append(c)
                if re.match('T[0-9]*',c):
                    self.T = c
                    self.t = int(re.sub('T','',c))
                if re.match('#',c):
                    self.SH = c

def OnSaveAs():

    saveFileDialog = wx.FileDialog(self, "Save XYZ file", "", "",
                                   "XYZ files (*.xyz)|*.xyz", wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)

    if saveFileDialog.ShowModal() == wx.ID_CANCEL:
        return     # the user changed idea...

    # save the current contents in the file
    # this can be done with e.g. wxPython output streams:
    output_stream = wx.FileOutputStream(saveFileDialog.GetPath())

    if not output_stream.IsOk():
        wx.LogError("Cannot save current contents in file '%s'."%saveFileDialog.GetPath())
        return

def saveFile():
    pass



class RapiroFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,None,wx.ID_ANY,u"Rapiro",size=(600,900))
        log = 'log'
        #    ステータスバーの初期化
        self.CreateStatusBar()
        self.SetStatusText("Rapiro")
        self.GetStatusBar().SetBackgroundColour(None)

        #    メニューバーの初期化
        self.SetMenuBar(RapiroMenu())

        #    本体部分の構築
        root_panel = wx.Panel(self,wx.ID_ANY)

        host_panel       = HostPanel(root_panel)
        action_panel     = ActionPanel(root_panel)
        servo_panel      = ServoPanel(root_panel)
        led_panel        = LedPanel(root_panel)
        edit_panel       = EditPanel(root_panel)
        motion_panel     = MotionPanel(root_panel)

        root_layout = wx.BoxSizer(wx.VERTICAL)
        root_layout.Add(host_panel,0,wx.GROW|wx.ALL,border=10)
        root_layout.Add(action_panel,0,wx.GROW|wx.ALL,border=10)
        root_layout.Add(led_panel,0,wx.GROW|wx.ALL,border=10)
        root_layout.Add(servo_panel,0,wx.GROW|wx.LEFT|wx.RIGHT,border=20)
        root_layout.Add(edit_panel,0,wx.GROW|wx.ALL,border=10)
        root_layout.Add(motion_panel,0,wx.GROW|wx.ALL,border=10)
        root_panel.SetSizer(root_layout)
        root_layout.Fit(root_panel)

class RapiroMenu(wx.MenuBar):

    def __init__(self):

        wx.MenuBar.__init__(self)

        menu_file = wx.Menu()
        menu_file.Append(wx.ID_ANY,u"保存")
        menu_file.Append(wx.ID_ANY,u"終了")
        #menu_edit = wx.Menu()
        #menu_edit.Append(wx.ID_ANY,u"コピー")
        #menu_edit.Append(wx.ID_ANY,u"ペースト")

        self.Append(menu_file,u"ファイル")
        #self.Append(menu_edit,u"編集")

class HostPanel(wx.Panel):

    def __init__(self,parent):

        wx.Panel.__init__(self,parent,wx.ID_ANY)

        self.text_host = wx.TextCtrl(self,wx.ID_ANY,u"%s" % (HOST),style=wx.TE_RIGHT)
        self.text_port = wx.TextCtrl(self,wx.ID_ANY,u"%s" % (PORT),style=wx.TE_RIGHT)
        self.button_conn = wx.ToggleButton(self,wx.ID_ANY,u"CONNECT",style=wx.TE_RIGHT)
        self.Bind(wx.EVT_TOGGLEBUTTON, self.click_button_conn)
        #layout = wx.BoxSizer(wx.HORIZONTAL)
        layout = wx.FlexGridSizer(1,3,3,3)

        layout.Add(self.text_host,1,wx.GROW)
        layout.Add(self.text_port,1)
        layout.Add(self.button_conn,1)
        self.SetSizer(layout)

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

class ActionPanel(wx.Panel):

    def __init__(self,parent):

        wx.Panel.__init__(self,parent,wx.ID_ANY)

        layout = wx.FlexGridSizer(5,5,3,3)
        for id, val in action_collection.items():
            b = wx.Button(self,id,val[0],size=(60,25))
            layout.Add(b ,1,wx.GROW)
            b.Bind(wx.EVT_BUTTON, self.click_action)
        self.SetSizer(layout)

    def click_action(self, event):
        global VERSION
        try:
            #print VERSION
            if VERSION == '#E':
                act = action_collection[event.GetId()]
            else:
                act = action_collection0[event.GetId()]
        except:
            pass
        if CONNECTED:
            s.send(act[1])
            rapiroResponse = s.recv(8192)
            frame.SetStatusText("Received value is " + str(rapiroResponse))


class ServoPanel(wx.Panel):
    def __init__(self,parent):

        wx.Panel.__init__(self,parent,wx.ID_ANY)

        layout = wx.FlexGridSizer(5,5,3,3)
        for id, val in servo_collection.items():
            if val[0] >= 0:
                #slider = wx.Slider(self,id,val[0],size=(30,25))
                slider = wx.Slider(self,id,style=val[1]|wx.SL_LABELS)
                layout.Add(slider ,1)
                slider.SetMin(val[3])
                slider.SetMax(val[4])
                slider.SetValue(val[2])
                slider.Bind(wx.EVT_SLIDER, self.slider_servo)
            else:
                text = wx.StaticText(self,id,'')
                layout.Add(text, 1, wx.GROW)

        self.SetSizer(layout)

    def slider_servo(self,event):
        sv = servo_collection[event.GetId()]
        obj = event.GetEventObject()
        angleNum = obj.GetValue()
        angle=str(angleNum).zfill(3)
        command = "a, #PS"+str(sv[0]).zfill(2)+"A"+angle+"T001\n"
        #print command, event.GetId()
        if CONNECTED:
            s.send(command)
            rapiroResponse = s.recv(8192)
            frame.SetStatusText("Received value is " + str(rapiroResponse))
        servo_pos[sv[0]] = angleNum

class LedPanel(wx.Panel):
    def __init__(self,parent):

        wx.Panel.__init__(self,parent,wx.ID_ANY)

        layout = wx.FlexGridSizer(1,3,3,3)
        for id, val in led_collection.items():
            if val[0] >= 0:
                #label1 = wx.StaticText(self,wx.GROW,u"%s" % val[0],size = (20,20) )
                #label1.SetBackgroundColour(val[6])
                #layout.Add(label1,flag=wx.SHAPED)
                slider = wx.Slider(self,id,style=val[1]|wx.SL_LABELS)
                slider.SetForegroundColour(val[6])
                slider.SetBackgroundColour(val[7])
                layout.Add(slider ,1)
                slider.SetMin(val[3])
                slider.SetMax(val[4])
                slider.SetValue(val[2])
                slider.Bind(wx.EVT_SLIDER, self.slider_led)
            else:
                text = wx.StaticText(self,id,'')
                layout.Add(text, 1, wx.GROW)

        self.SetSizer(layout)

    def slider_led(self, event):
        color = led_collection[event.GetId()]
        obj = event.GetEventObject()
        brightNum=obj.GetValue()
        bright=str(brightNum).zfill(3)
        command = "a, #P"+str(color[0])+bright+"T002\n"
        #print command, event.GetId()
        if CONNECTED:
            s.send(command)
            rapiroResponse = s.recv(8192)
            frame.SetStatusText("Received value is " + str(rapiroResponse))
        led_val[color[5]] = brightNum


class EditPanel(wx.Panel):
    def __init__(self,parent):

        wx.Panel.__init__(self,parent,wx.ID_ANY)

        layout = wx.FlexGridSizer(1,7,3,3)
        for id, val in edit_collection.items():
            b = wx.Button(self,id,val[0],size=(60,25))
            layout.Add(b ,1,wx.GROW)
            b.Bind(wx.EVT_BUTTON, self.click_edit)

        self.text_time = wx.TextCtrl(self,wx.ID_ANY,"%d" % (TIME),style=wx.TE_RIGHT)
        layout.Add(self.text_time,1)
        self.SetSizer(layout)


    def click_edit(self, event):
        global frame_list,rapiroResponse, index, text_motion
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
                    s.send(play_cmd)
                    rapiroResponse = s.recv(8192)
                    res = resAnalysis(rapiroResponse)
                    w = res.t
                    #print w
                    while(w > 0 ):
                        time.sleep(0.2)
                        s.send("a, #Q\n")
                        #s.send("a, #C\n")
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


class MotionPanel(wx.Panel):
    def __init__(self,parent):
        global text_motion,frame_list, MOTION_TIMES
        wx.Panel.__init__(self,parent,wx.ID_ANY)
        layout = wx.FlexGridSizer(9,2,3,3)
        label1 = wx.StaticText(self,wx.GROW,u"Repeat",size = (100,20) )
        layout.Add(label1,flag=wx.SHAPED)
        text_motion_n = wx.TextCtrl(self,wx.ID_ANY,u"%s" % (MOTION_TIMES),style=wx.TE_RIGHT)
        layout.Add(text_motion_n,flag=wx.GROW)
        #self.text_port = wx.TextCtrl(self,wx.ID_ANY,u"%s" % (PORT),style=wx.TE_RIGHT)
        for id in range(8):
            label = wx.StaticText(self,wx.GROW,(u"%s" % id),size = (100,20))
            layout.Add(label,flag=wx.SHAPED)
            text_motion[id] = wx.TextCtrl(self,id,list2str(frame_list[id]),style=wx.TE_LEFT,size = (400,20))
            #text_motion[id].Enable()
            text_motion[id].Disable()
            layout.Add(text_motion[id],flag=wx.GROW)
            layout.AddGrowableCol(id)
        self.SetSizer(layout)

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
    s.send("a, #V\n")
    v = s.recv(8192)
    return(v)
#---------------------------------------------------------------------------

if __name__ == "__main__":
    application = wx.App()
    frame = RapiroFrame()
    frame.Show()
    application.MainLoop()
