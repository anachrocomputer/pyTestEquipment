# FY2200

Scripts to control the FeelTech FY2200 dual signal generator.

The FY2200 has a USB serial interface which accepts a limited set
of commands and status requests.
Not all of the device's functions may be controlled via the serial
interface, nor can all of its state be read back.

## fy2200gui.py

A GUI based on 'tkinter' that can control the signal generator via its
USB serial interface.
