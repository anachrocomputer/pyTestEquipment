# fy2200ctl --- control a FeelTech FY2200 via the serial port  2020-03-08
# Copyright (c) 2020 John Honniball. All rights reserved.

from tkinter import *
from tkinter import ttk

import serial
import serial.tools.list_ports

Row = 0

def poopoo():
   print("POO")


def spinChange():
   print(spinval.get())


def comboChange(arg):
   global c

   c.selection_clear()
   #print(setting.get())


def EnableAllControls(enabled):
   if enabled == True:
      Sine.config(state=NORMAL)
      Square.config(state=NORMAL)
      Triangle.config(state=NORMAL)
   else:
      Sine.config(state=DISABLED)
      Square.config(state=DISABLED)
      Triangle.config(state=DISABLED)


def OpenSerialPort():
   global Row
   global Ser

   Ser.port = setting.get()
   Ser.baud = 9600
   Ser.open()
   if Ser.open:
      Row = 0
      root.after(1000, sendPoll)
      c.config(state=DISABLED)
      OpenButton.config(state=DISABLED)
      CloseButton.config(state=NORMAL)
      EnableAllControls(True)


def CloseSerialPort():
   global Ser

   if Ser.is_open:
      Ser.close()
      c.config(state=NORMAL)
      OpenButton.config(state=NORMAL)
      CloseButton.config(state=DISABLED)
      EnableAllControls(False)


def sendPoll():
   global Row
   global Ser

   if Ser.is_open:
      print("POLL %d" % Row)
      t.insert(END, "\n ROW OF TEXT %d" % Row)
      t.see(END)
      Row += 1
      root.after(5000, sendPoll)


root = Tk()
root.title("FeelTech FY2200S")

w = Label(root, text="FeelTech FY2200S")
w.pack()

f = Frame(root)
f.pack()

b1 = Button(f, text="POO", command=poopoo)
#b1.config(command=poopoo)
b1.pack(side='left')

b2 = Button(f, text="Quit", command=root.destroy)
b2.pack(side='right')

f2 = Frame(root)
f2.pack()

l = Label(f2, text='Interval')
l.pack(side='left')

spinval = StringVar()
s = Spinbox(f2, from_=5, to=30, increment=5, width=4, textvariable=spinval, command=spinChange)
s.pack(side='right')

t = Text(root, width=40, height=8)
t.pack()

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

Ser = serial.Serial()

Wave = StringVar()
Wave.set('sine')
WaveControls = Frame(root)
WaveControls.pack()
Sine = Radiobutton(WaveControls, text='Sine', variable=Wave, value='sine')
Square = Radiobutton(WaveControls, text='Square', variable=Wave, value='square')
Triangle = Radiobutton(WaveControls, text='Triangle', variable=Wave, value='triangle')
Sine.pack(side='left')
Square.pack(side='left')
Triangle.pack(side='left')

EnableAllControls(False)

root.mainloop()
