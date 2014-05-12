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
MAXTIME = 010

RED = MAXRED
GREEN = MAXGREEN
BLUE = MAXBLUE
TIME = MAXTIME

#RGB COLOR program with timing.
def led(RED,GREEN,BLUE,TIME):
    s = "#PR" + str(RED).zfill(3) + "G" + str(GREEN).zfill(3) + "B" + str(BLUE).zfill(3) + "T" + str(TIME).zfill(3)
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
wm.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC #| cwiid.RPT_CLASSIC | cwiid.RPT_NUNCHUK

#turn on led to show connection has been established
wm.led = 1

button_delay = 0.3


print 'connected, starting the loop........'

while True:
    #wiimote
    wiibuttons = wm.state['buttons']
    buttons = wiibuttons
    wiiacc = wm.state['acc']
    #print wiibuttons, wiiacc

    if ((BTN_STATE != wiibuttons)&(wiibuttons!=0)):
        BTN_STATE = wiibuttons
        try:
            print but2act[wiibuttons]['type']
            rapiro.write(but2act[wiibuttons]['pressed'])
        except:
            pass
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