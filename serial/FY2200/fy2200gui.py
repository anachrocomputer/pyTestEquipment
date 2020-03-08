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
   print(spinval1.get())


def spinChange2():
   print(spinval2.get())


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
      s1.config(state=NORMAL)
      s2.config(state=NORMAL)
   else:
      Sine1.config(state=DISABLED)
      Square1.config(state=DISABLED)
      Triangle1.config(state=DISABLED)
      Sine2.config(state=DISABLED)
      Square2.config(state=DISABLED)
      Triangle2.config(state=DISABLED)
      s1.config(state=DISABLED)
      s2.config(state=DISABLED)


def OpenSerialPort():
   global Row
   global Ser
   global c
   global w

   Ser.port = setting.get()
   Ser.baud = 9600
   Ser.timeout = 0.5
   Ser.open()
   if Ser.open:
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

Channel1 = Frame(root)
Channel1.pack()

Freq1 = Label(Channel1, text='Frequency 1')
Freq1.pack(side='left')

hz1 = Label(Channel1, text='Hz')
hz1.pack(side='right')

spinval1 = StringVar()
s1 = Spinbox(Channel1, from_=1, to=12000000, increment=1, width=12, textvariable=spinval1, command=spinChange1)
s1.pack(side='right')

Wave1 = StringVar()
Wave1.set('sine')
WaveControls1 = Frame(root)
WaveControls1.pack()
Sine1 = Radiobutton(WaveControls1, text='Sine', variable=Wave1, value='sine')
Square1 = Radiobutton(WaveControls1, text='Square', variable=Wave1, value='square')
Triangle1 = Radiobutton(WaveControls1, text='Triangle', variable=Wave1, value='triangle')
Sine1.pack(side='left')
Square1.pack(side='left')
Triangle1.pack(side='left')

Channel2 = Frame(root)
Channel2.pack()

Freq2 = Label(Channel2, text='Frequency 2')
Freq2.pack(side='left')

hz2 = Label(Channel2, text='Hz')
hz2.pack(side='right')

spinval2 = StringVar()
s2 = Spinbox(Channel2, from_=1, to=12000000, increment=1, width=12, textvariable=spinval2, command=spinChange2)
s2.pack(side='right')

Wave2 = StringVar()
Wave2.set('sine')
WaveControls2 = Frame(root)
WaveControls2.pack()
Sine2 = Radiobutton(WaveControls2, text='Sine', variable=Wave2, value='sine')
Square2 = Radiobutton(WaveControls2, text='Square', variable=Wave2, value='square')
Triangle2 = Radiobutton(WaveControls2, text='Triangle', variable=Wave2, value='triangle')
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
