import time
import sys
import serial
import os
import time
import datetime
import cwiid

# Button
'''
https://github.com/abstrakraft/cwiid/blob/master/libcwiid/cwiid.h
'''
CWIID_BTN_2     = 0x0001
CWIID_BTN_1		= 0x0002
CWIID_BTN_B		= 0x0004
CWIID_BTN_A		= 0x0008
CWIID_BTN_MINUS	= 0x0010
CWIID_BTN_HOME	= 0x0080
CWIID_BTN_LEFT	= 0x0100
CWIID_BTN_RIGHT	= 0x0200
CWIID_BTN_DOWN	= 0x0400
CWIID_BTN_UP	= 0x0800
CWIID_BTN_PLUS	= 0x1000

CWIID_NUNCHUK_BTN_Z = 0x01
CWIID_NUNCHUK_BTN_C =0x02

CWIID_CLASSIC_BTN_UP    = 0x0001
CWIID_CLASSIC_BTN_LEFT  = 0x0002
CWIID_CLASSIC_BTN_ZR    = 0x0004
CWIID_CLASSIC_BTN_X     = 0x0008
CWIID_CLASSIC_BTN_A	    = 0x0010
CWIID_CLASSIC_BTN_Y	    = 0x0020
CWIID_CLASSIC_BTN_B     = 0x0040
CWIID_CLASSIC_BTN_ZL    = 0x0080
CWIID_CLASSIC_BTN_R     = 0x0200
CWIID_CLASSIC_BTN_PLUS  = 0x0400
CWIID_CLASSIC_BTN_HOME  = 0x0800
CWIID_CLASSIC_BTN_MINUS = 0x1000
CWIID_CLASSIC_BTN_L     = 0x2000
CWIID_CLASSIC_BTN_DOWN  = 0x4000
CWIID_CLASSIC_BTN_RIGHT = 0x8000

but2act = {
0:              {'type':'NON',      'pressed':'#M00'},
CWIID_BTN_2:    {'type':'BTN_2',    'pressed':'#M08'},
CWIID_BTN_1:    {'type':'BTN_1',    'pressed':'#M07'},
CWIID_BTN_B:    {'type':'BTN_B',    'pressed':'#M00'},
CWIID_BTN_A:    {'type':'BTN_A',    'pressed':'#M05'},
CWIID_BTN_MINUS:{'type':'BTN_MINUS','pressed':'#M09'},
CWIID_BTN_HOME: {'type':'BTN_HOME', 'pressed':'#M10'},
CWIID_BTN_LEFT: {'type':'BTN_LEFT', 'pressed':'#M04'},
CWIID_BTN_RIGHT:{'type':'BTN_RIGHT','pressed':'#M03'},
CWIID_BTN_DOWN: {'type':'BTN_DOWN', 'pressed':'#M02'},
CWIID_BTN_UP:   {'type':'BTN_UP',   'pressed':'#M01'},
CWIID_BTN_PLUS: {'type':'BTN_PLUS', 'pressed':'#M06'},
CWIID_BTN_PLUS|
CWIID_BTN_MINUS:{'type':'BTN_PLUS&BTN_MINUS', 'pressed':'#M06'}
}
cbut2act = {
0:                      {'type':'NON',      'pressed':'#M00'},
CWIID_CLASSIC_BTN_ZR:   {'type':'CBTN_ZR',   'pressed':'#M00'},
CWIID_CLASSIC_BTN_ZL:   {'type':'CBTN_ZL',   'pressed':'#M00'},
CWIID_CLASSIC_BTN_R:    {'type':'CBTN_R',    'pressed':'#M00'},
CWIID_CLASSIC_BTN_L:    {'type':'CBTN_L',    'pressed':'#M00'},
CWIID_CLASSIC_BTN_Y:    {'type':'CBTN_2',    'pressed':'#M08'},
CWIID_CLASSIC_BTN_X:    {'type':'CBTN_1',    'pressed':'#M07'},
CWIID_CLASSIC_BTN_B:    {'type':'CBTN_B',    'pressed':'#M00'},
CWIID_CLASSIC_BTN_A:    {'type':'CBTN_A',    'pressed':'#M05'},
CWIID_CLASSIC_BTN_MINUS:{'type':'CBTN_MINUS','pressed':'#M09'},
CWIID_CLASSIC_BTN_HOME: {'type':'CBTN_HOME', 'pressed':'#M10'},
CWIID_CLASSIC_BTN_LEFT: {'type':'CBTN_LEFT', 'pressed':'#M04'},
CWIID_CLASSIC_BTN_RIGHT:{'type':'CBTN_RIGHT','pressed':'#M03'},
CWIID_CLASSIC_BTN_DOWN: {'type':'CBTN_DOWN', 'pressed':'#M02'},
CWIID_CLASSIC_BTN_UP:   {'type':'CBTN_UP',   'pressed':'#M01'},
CWIID_CLASSIC_BTN_PLUS: {'type':'CBTN_PLUS', 'pressed':'#M06'},
CWIID_CLASSIC_BTN_PLUS|
CWIID_CLASSIC_BTN_MINUS:{'type':'CBTN_PLUS&CBTN_MINUS', 'pressed':'#M06'}
}

#Serial connection for interfacting with Arduino board on Rapiro
rapiro = serial.Serial('/dev/ttyAMA0', 57600, timeout = 10)

#
BTN_STATE = 0
BTN_PREV  = 0
#Container for joystik input
data = []

#Define colors codes and maximum intensity for the RGB LED
MAXRED = 255
MAXGREEN = 225
MAXBLUE = 255
MAXTIME = 005

RED = MAXRED
GREEN = MAXGREEN
BLUE = MAXBLUE
TIME = MAXTIME

#RGB COLOR program with timing.
def led(RED,GREEN,BLUE,TIME):
    s = "#PR" + str(RED).zfill(3) + "G" + str(GREEN).zfill(3) + "B" + str(BLUE).zfill(3) + "T" + str(TIME).zfill(3)
    return (s)

def PS(RUD, RLR, LUD, LLR):
    s = "#PS02A" + str(RUD).zfill(3) + "S03A" + str(RLR).zfill(3) + "S05A" + str(LUD).zfill(3) + "S06A" + str(LLR).zfill(3) + "T002\r\n"
    return (s)

#Print Max values, and Changing colors. All max= White.
#TIME is the fading speed 000 change the color instantaneously, 255 very slowly.

rapiro.write(led(RED,GREEN,BLUE,TIME))
print(led(RED,GREEN,BLUE,TIME))
time.sleep(0.2)
rapiro.write(led(147,023,239,020))
print rapiro.write('#H')
print 'now we play with the Wiimote..\n'
time.sleep(0.5)

LLRLIMIT    =  70   #20     #S06    Left analog stick Left - Right
LUDLIMIT    = 180   #120    #S05    Left analog stick UP - DOWN
RLRLIMIT    = 110   #100    #S03    Right analog stick Left - Right
RUDLIMIT    =   0           #S02    Right analog stick UP - DOWN
LLR = LLRLIMIT
LUD = LUDLIMIT
RLR = RLRLIMIT
RUD = RUDLIMIT
LSX = 32
LSY = 32
RSX = 15
RSY = 15
befor_LSX = 32
befor_LSY = 32
befor_RSX = 15
befor_RSY = 15
before_time = 0
now_time = 0

#connecting to the wiimote. This allows several attempts
# as first few often fail.

print 'Press 1 + 2 on your Wii Remote now ...'
time.sleep(1)
wm = None
i=2
while not wm:
    try:
        wm=cwiid.Wiimote()

    except RuntimeError:
        if (i>5):
            print("cannot create connection")

            quit()
        print "Error opening wiimote connection"
        print "attempt " + str(i)
        i +=1
print 'Wii Remote connected...\n'
print 'Press PLUS and MINUS together to disconnect and quit.\n'
wm.rumble = 1
time.sleep(0.5)
wm.rumble = 0
#set wiimote to report button presses and accelerometer state
wm.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC | cwiid.RPT_CLASSIC | cwiid.RPT_NUNCHUK

#turn on led to show connection has been established
wm.led = 1

button_delay = 0.3
wiibuttons = 0
before_wiibuttons = 0
classicbuttons = 0
before_classicbuttons = 0
wiiacc = [0,0,0]
before_wiiacc = [0,0,0]
acc_state = 0
CLASSIC_BTN_STATE = 'released'

print 'connected, starting the loop........'

while True:
    #wiimote
    before_wiibuttons = wiibuttons
    before_wiiacc = wiiacc
    wiibuttons = wm.state['buttons']
    wiiacc = wm.state['acc']
    acc_state = 0
    for acc0,acc1 in zip(before_wiiacc, wiiacc):
        if abs(acc0-acc1)>2 :
            acc_state += 1

    if wm.state['ext_type']==cwiid.EXT_CLASSIC:
        if wm.state.has_key('classic'):
            before_classicbuttons = classicbuttons
            classicbuttons = wm.state['classic']['buttons']
            if (classicbuttons != 0):
                CLASSIC_BTN_STATE = 'pressed'
            else:
                CLASSIC_BTN_STATE = 'released'

            LSX = wm.state['classic']['l_stick'][0]
            LSY = wm.state['classic']['l_stick'][1]
            RSX = wm.state['classic']['r_stick'][0]
            RSY = wm.state['classic']['r_stick'][1]
            if ((LSX>33)|(LSX<31)|
                (LSY>33)|(LSY<31)|
                (RSX>16)|(RSX<14)|
                (RSY>16)|(RSY<14)):
                joy = True
            else:
                joy = False
    else:
        joy = False

    if (wiibuttons != 0):
        BTN_STATE = 'pressed'
    else:
        BTN_STATE = 'released'

    if (BTN_STATE == 'pressed'):
        try:
            if (before_wiibuttons!= wiibuttons):
                print but2act[wiibuttons]['type']
                rapiro.write(but2act[wiibuttons]['pressed'])
        except:
            pass
    elif (CLASSIC_BTN_STATE=='pressed'):
        #try:
            if (before_classicbuttons!= classicbuttons):
                print cbut2act[classicbuttons]['type']
                rapiro.write(cbut2act[classicbuttons]['pressed'])
        #except:
        #    pass
    elif joy:
            now = datetime.datetime.now()
            now_time = now.minute * 60000 + now.second * 1000 + now.microsecond/1000
            if LSX < 30:
                LLR += abs(30-LSX)
                if LLR > 180:
                    LLR = 180
            elif LSX > 33:
                LLR -= abs(33-LSX)
                if LLR < LLRLIMIT:
                    LLR = LLRLIMIT
            if LSY < 30:
                LUD += abs(30-LSY)
                if LUD > 180:
                    LUD = 180
            elif LSY > 33:
                LUD -= abs(33-LSY)
                if LUD < 0:
                    LUD = 0

            if RSX < 14:
                RLR += abs(14-RSX)
                if RLR > RLRLIMIT:
                    RLR = RLRLIMIT
            elif RSX > 16:
                RLR -= abs(16-RSX)
                if RLR < 0:
                    RLR = 0

            if RSY > 16:
                RUD += abs(16-RSY)
                if RUD > 180:
                    RUD = 180
            elif RSY < 14:
                RUD -= abs(14-RSY)
                if RUD < 0:
                    RUD = 0
            #print RSX, RSY, LSX, LSY, LLR, LUD, RLR, RUD
            dif = now_time - before_time
            if dif > 110 and joy == True:
                rapiro.write(PS(RUD,RLR,LUD,LLR))
                #rapiro.write("ms : " + str(dif) + "\r\n")
                now = datetime.datetime.now()
                before_time = now.minute * 60000 + now.second * 1000 + now.microsecond/1000
    elif acc_state != 0:
        rapiro.write(led(wiiacc[0],wiiacc[1],wiiacc[2],TIME))

'''
	if (buttons & cwiid.BTN_1):
		print (wm.state)
		time.sleep(0.8)
	if (buttons & cwiid.BTN_2):
		print (wm.state)
		time.sleep(0.2)
	if (buttons - cwiid.BTN_PLUS - cwiid.BTN_MINUS == 0):
		print '\nClosing connection ...'
		wm.rumble = 1
		time.sleep(0.4)
		wm.rumble = 0
		rapiro.write('#M08')
		time.sleep(5)
		rapiro.write('#M00')
		time.sleep(3)
		print '\nExiting program ...'
		rapiro.write('#H')
		exit(wm)
	if (buttons - cwiid.BTN_A - cwiid.BTN_B == 0):
		print '\nExtra rapiro movement STOP'
		time.sleep(1)
		rapiro.write('#H')
	if (buttons & cwiid.BTN_HOME):
		print 'Home Button pressed'
		time.sleep(button_delay)
		rapiro.write("#H")
	if (buttons & cwiid.BTN_LEFT):
		print 'Left pressed'
		time.sleep(button_delay)
	if(buttons & cwiid.BTN_RIGHT):
		print 'Right pressed'
		time.sleep(button_delay)
	if (buttons & cwiid.BTN_UP):
		print 'Up pressed'
		time.sleep(button_delay)
	if (buttons & cwiid.BTN_DOWN):
		print 'Down pressed'
		time.sleep(button_delay)
	if (buttons & cwiid.BTN_A):
		print 'Button A pressed'
		time.sleep(button_delay)
	if (buttons & cwiid.BTN_B):
		print 'INFORMATION YOU NEED TO HACK'
		print(wm.state)
		time.sleep(button_delay)

		print('\nThis is nupposed to change the ligh so adjust the colors to match 0 to 255\n'+"#PR" + str(RED) + "G" + str(GREEN) +  "B" + str(BLUE) + 'T' + str(TIME))
		print str(wiiacc) + 'wii ACC data in str format\n'
		rapiro.write(led(wiiacc[0],wiiacc[1],wiiacc[2],'010'))

	if (buttons & cwiid.BTN_MINUS):
		print 'Minus Button pressed'
		time.sleep(button_delay)
	if (buttons & cwiid.BTN_PLUS):
		print 'Plus Button pressed'
		time.sleep(button_delay)
  '''