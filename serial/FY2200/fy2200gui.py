# fy2200gui --- control a FeelTech FY2200 via the serial port  2020-03-08
# Copyright (c) 2020 John Honniball. All rights reserved.

from tkinter import *
from tkinter import ttk

import serial
import serial.tools.list_ports

Row = 0

def poopoo():
    global Ser

    print("POO")
    if Ser.is_open:
        Ser.write(b'cf\n')
        str = Ser.read(12)
        print(str)
        Ser.write(b'cd\n')
        str = Ser.read(4)
        print(str)


def spinChange1():
    print(Channel1FreqStr.get())


def spinChange2():
    print(Channel2FreqStr.get())


def comboChange(arg):
    global c

    c.selection_clear()
    #print(setting.get())


def EnableAllControls(enabled):
    if enabled == True:
        Sine1.config(state=NORMAL)
        Square1.config(state=NORMAL)
        Triangle1.config(state=NORMAL)
        Sine2.config(state=NORMAL)
        Square2.config(state=NORMAL)
        Triangle2.config(state=NORMAL)
        Channel1FreqSpin.config(state=NORMAL)
        Channel1AmpSpin.config(state=NORMAL)
        Channel1DutySpin.config(state=NORMAL)
        Channel2FreqSpin.config(state=NORMAL)
        Channel2AmpSpin.config(state=NORMAL)
        Channel2DutySpin.config(state=NORMAL)
    else:
        Sine1.config(state=DISABLED)
        Square1.config(state=DISABLED)
        Triangle1.config(state=DISABLED)
        Sine2.config(state=DISABLED)
        Square2.config(state=DISABLED)
        Triangle2.config(state=DISABLED)
        Channel1FreqSpin.config(state=DISABLED)
        Channel1AmpSpin.config(state=DISABLED)
        Channel1DutySpin.config(state=DISABLED)
        Channel2FreqSpin.config(state=DISABLED)
        Channel2AmpSpin.config(state=DISABLED)
        Channel2DutySpin.config(state=DISABLED)


def OpenSerialPort():
    global Row
    global Ser
    global c
    global w

    Ser.port = setting.get()
    Ser.baud = 9600
    Ser.timeout = 0.5
    Ser.open()
    if Ser.is_open:
        Row = 0
        c.config(state=DISABLED)
        OpenButton.config(state=DISABLED)
        CloseButton.config(state=NORMAL)
        EnableAllControls(True)
        Ser.write(b'a\n')
        str = Ser.read(8).decode('utf-8')
        if len(str) > 0:
            w.config(text="FeelTech " + str[0:-1])
        else:
            w.config(text="Instrument did not respond")


def CloseSerialPort():
    global Ser
    global c
    global w

    if Ser.is_open:
        Ser.close()
        c.config(state=NORMAL)
        OpenButton.config(state=NORMAL)
        CloseButton.config(state=DISABLED)
        EnableAllControls(False)
        w.config(text="FeelTech FY22XX")


root = Tk()
root.title("FeelTech FY2200S")

w = Label(root, text="FeelTech FY22XX")
w.pack()

f = Frame(root)
f.pack()

b1 = Button(f, text="POO", command=poopoo)
#b1.config(command=poopoo)
b1.pack(side='left')

b2 = Button(f, text="Quit", command=root.destroy)
b2.pack(side='right')

Channel1Freq = Frame(root)
Channel1Freq.pack()

Freq1 = Label(Channel1Freq, text='Frequency 1')
Freq1.pack(side='left')

hz1 = Label(Channel1Freq, text='Hz')
hz1.pack(side='right')

Channel1FreqStr = StringVar()
Channel1FreqSpin = Spinbox(Channel1Freq, from_=1, to=12000000, increment=1, width=10, textvariable=Channel1FreqStr, command=spinChange1)
Channel1FreqSpin.pack(side='right')

Channel1Amp = Frame(root)
Channel1Amp.pack()

Amp1 = Label(Channel1Amp, text='Amplitude 1')
Amp1.pack(side='left')

volt1 = Label(Channel1Amp, text='V')
volt1.pack(side='right')

Channel1AmpStr = StringVar()
Channel1AmpSpin = Spinbox(Channel1Amp, from_=0, to=10.0, increment=0.01, width=5, textvariable=Channel1AmpStr)
Channel1AmpSpin.pack(side='right')

Channel1Duty = Frame(root)
Channel1Duty.pack()

Duty1 = Label(Channel1Duty, text='Duty Cycle 1')
Duty1.pack(side='left')

percent1 = Label(Channel1Duty, text='%')
percent1.pack(side='right')

Channel1DutyStr = StringVar()
Channel1DutyStr.set('50')
Channel1DutySpin = Spinbox(Channel1Duty, from_=0, to=100, increment=1, width=5, textvariable=Channel1DutyStr)
Channel1DutySpin.pack(side='right')

Wave1 = StringVar()
Wave1.set('sine')
WaveControls1 = Frame(root)
WaveControls1.pack()
Form1 = Label(WaveControls1, text='Waveform 1')
Sine1 = Radiobutton(WaveControls1, text='Sine', variable=Wave1, value='sine')
Square1 = Radiobutton(WaveControls1, text='Square', variable=Wave1, value='square')
Triangle1 = Radiobutton(WaveControls1, text='Triangle', variable=Wave1, value='triangle')
Form1.pack(side='left')
Sine1.pack(side='left')
Square1.pack(side='left')
Triangle1.pack(side='left')

Channel2Freq = Frame(root)
Channel2Freq.pack()

Freq2 = Label(Channel2Freq, text='Frequency 2')
Freq2.pack(side='left')

hz2 = Label(Channel2Freq, text='Hz')
hz2.pack(side='right')

Channel2FreqStr = StringVar()
Channel2FreqSpin = Spinbox(Channel2Freq, from_=1, to=12000000, increment=1, width=10, textvariable=Channel2FreqStr, command=spinChange2)
Channel2FreqSpin.pack(side='right')

Channel2Amp = Frame(root)
Channel2Amp.pack()

Amp2 = Label(Channel2Amp, text='Amplitude 2')
Amp2.pack(side='left')

volt2 = Label(Channel2Amp, text='V')
volt2.pack(side='right')

Channel2AmpStr = StringVar()
Channel2AmpSpin = Spinbox(Channel2Amp, from_=0, to=10.0, increment=0.01, width=5, textvariable=Channel2AmpStr)
Channel2AmpSpin.pack(side='right')

Channel2Duty = Frame(root)
Channel2Duty.pack()

Duty2 = Label(Channel2Duty, text='Duty Cycle 2')
Duty2.pack(side='left')

percent2 = Label(Channel2Duty, text='%')
percent2.pack(side='right')

Channel2DutyStr = StringVar()
Channel2DutyStr.set('50')
Channel2DutySpin = Spinbox(Channel2Duty, from_=0, to=100, increment=1, width=5, textvariable=Channel2DutyStr)
Channel2DutySpin.pack(side='right')


Wave2 = StringVar()
Wave2.set('sine')
WaveControls2 = Frame(root)
WaveControls2.pack()
Form2 = Label(WaveControls2, text='Waveform 2')
Sine2 = Radiobutton(WaveControls2, text='Sine', variable=Wave2, value='sine')
Square2 = Radiobutton(WaveControls2, text='Square', variable=Wave2, value='square')
Triangle2 = Radiobutton(WaveControls2, text='Triangle', variable=Wave2, value='triangle')
Form2.pack(side='left')
Sine2.pack(side='left')
Square2.pack(side='left')
Triangle2.pack(side='left')


# Look for available serial ports
ports = serial.tools.list_ports.comports()

portList = []
for p in ports:
    portList.append(p.device)

setting = StringVar()
if len(ports) > 0:
    setting.set(ports[0].device)
else:
    setting.set('')

PortControls = Frame(root)
PortControls.pack()

c = ttk.Combobox(PortControls, textvariable=setting, state='readonly')
c['values'] = portList

c.bind('<<ComboboxSelected>>', comboChange)
c.pack(side='left')

CloseButton = Button(PortControls, text='Close', command=CloseSerialPort)
CloseButton.pack(side='right')

OpenButton = Button(PortControls, text='Open', command=OpenSerialPort)
OpenButton.pack(side='right')

CloseButton.config(state=DISABLED)
EnableAllControls(False)

Ser = serial.Serial()

root.mainloop()
