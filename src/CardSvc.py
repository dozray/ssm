#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import ctypes
import time
import binascii

from ctypes import wintypes
import pythoncom
import pyHook

scanCodeDict={'1':0x02,'2':0x03,'3':0x04,'4':0x05,'5':0x06,'6':0x07,'7':0x08,'8':0x09,'9':0x0A,'0':0x0B,'A':0x1E,'B':0x30,'C':0x2E,'D':0x20,'E':0x12,'F':0x21}

SendInput = ctypes.windll.user32.SendInput

# C struct redefinitions 
PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

# Actuals Functions

def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))



def getCardId():
    dll = ctypes.windll.LoadLibrary('function.dll')
    mfGetsnr = dll.MF_Getsnr
    mfGetsnr.argtypes = [ctypes.c_int,ctypes.c_int,ctypes.c_char_p,ctypes.c_char_p]
    mfGetsnr.restypes = ctypes.c_int
    mode = 0x26
    halt = 0x00
    snr = "      "
    buf = ctypes.create_string_buffer(16)
    nRet = mfGetsnr(mode,halt,snr,buf)

    #print binascii.hexlify('hello')
    if nRet == 0:
        #print 'query success!'
        hexCode=''
        for i in range(0,4):
            #print binascii.b2a_hex(buf[i])
            hexCode = hexCode+binascii.hexlify(buf[i])         
        return hexCode.upper()

def onKeyboardEvent(event):
  
    # 监听键盘事件 F9
    if event.ScanCode==0x43:
       
        cardId = getCardId()        
        if cardId != None:
            for i in range(1,9):
                PressKey(0x0E)                
                ReleaseKey(0x0E)
            
            for c in cardId:
                scanCode = scanCodeDict[c]               
                PressKey(scanCode)                
                ReleaseKey(scanCode)
                #time.sleep(0.1)
        '''
        else:
            print "getCardId is none"   '''             
        #print getCardId()
   
    return True 
 
def main():   
    # 创建一个“钩子”管理对象   
    hm = pyHook.HookManager()   
    # 监听所有键盘事件   
    hm.KeyDown = onKeyboardEvent   
    # 设置键盘“钩子”   
    hm.HookKeyboard()      
    # 进入循环，如不手动关闭，程序将一直处于监听状态   
    pythoncom.PumpMessages() 
 
if __name__ == "__main__":   
    main()
