#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time, ctypes, threading, win32con
import binascii
from ctypes import wintypes



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

def beep():
    dll = ctypes.windll.LoadLibrary('function.dll')
    buzzer = dll.ControlBuzzer
    buzzer.argtypes = [ctypes.c_int,ctypes.c_int,ctypes.c_char_p]
    buzzer.restypes = ctypes.c_int
    freq = 16
    duration = 1
    buf = ctypes.create_string_buffer(16)
    nRtn = buzzer(freq,duration,buf)
    if nRtn == 0:
        print("been once")
    
class HotKey(threading.Thread):  #创建一个Thread.threading的扩展类
 
    def run(self):
        global EXIT  #定义全局变量，这个可以在不同线程见共用。
        byref = ctypes.byref
        user32 = ctypes.windll.user32  #加载user32.dll
        print("run is run.")
        
        '''
        /*
         * RegisterHotKey函数原型及说明：
         * BOOL RegisterHotKey(
         * HWND hWnd,         // window to receive hot-key notification
         * int id,            // identifier of hot key
         * UINT fsModifiers,  // key-modifier flags
         * UINT vk            // virtual-key code);
         * 参数 id为你自己定义的一个ID值
         * 对一个线程来讲其值必需在0x0000 - 0xBFFF范围之内,十进制为0~49151
         * 对DLL来讲其值必需在0xC000 - 0xFFFF 范围之内,十进制为49152~65535
         * 在同一进程内该值必须唯一参数 fsModifiers指明与热键联合使用按键
         * 可取值为：MOD_ALT MOD_CONTROL MOD_WIN MOD_SHIFT参数，或数字0为无，1为Alt,2为Control，4为Shift，8为Windows
         * vk指明热键的虚拟键码
         */
         '''

           
        # 定义快捷键
        HOTKEYS = {
                    77 : (win32con.VK_F9,0),
                    88 : (win32con.VK_F9,win32con.MOD_WIN) # (win32con.VK_F9,win32con.MOD_WIN)
                    }
        # 快捷键对应的函数
        HOTKEY_ACTIONS = {
                77 : handle_start_Event,
                88 : handle_stop_Event
            }
        # 注册快捷键
        for id, (vk, modifiers) in HOTKEYS.items():
            if not user32.RegisterHotKey(None,id,modifiers,vk):        
                print "Unable to register id ",id
        # 启动监听
        try:
            msg = ctypes.wintypes.MSG()
            while user32.GetMessageA(byref(msg),None,0,0) != 0:              
                if msg.message == win32con.WM_HOTKEY: #786
                    action_to_take = HOTKEY_ACTIONS.get(msg.wParam)
                    if(action_to_take):
                        action_to_take()
                user32.TranslateMessage(byref(msg))
                user32.DispatchMessageA(byref(msg))

        finally:
            for id in HOTKEYS.keys():
                user32.UnregisterHotKey(None,id)


                
        '''
        #if not user32.RegisterHotKey(None, 99, win32con.MOD_ALT, win32con.VK_F3):   # 注册快捷键 alt + f3 并判断是否成功。
        if not user32.RegisterHotKey(None, 99, 0, win32con.VK_F9):   # 注册快捷键 F9 并判断是否成功。
            print("F9已被注册为其它的快捷键")
            user32.UnregisterHotKey(None,99)
            raise                                                                   # 返回一个错误信息
        
	#以下为判断快捷键冲突，释放快捷键
        try:
            msg = ctypes.wintypes.MSG()
            #print msg
            while user32.GetMessageA(ctypes.byref(msg), None, 0, 0) != 0:
                if msg.message == win32con.WM_HOTKEY:
                    if msg.wParam == 99:
                        print "xxx"
                        cardId = getCardId()
                        if cardId != None:
                            for i in range(1,9): #删除当前光标之前的8个字符
                                PressKey(0x0E)                
                                ReleaseKey(0x0E)
            
                            for c in cardId:
                                scanCode = scanCodeDict[c]               
                                PressKey(scanCode)                
                                ReleaseKey(scanCode)
                user32.TranslateMessage(ctypes.byref(msg))
                user32.DispatchMessageA(ctypes.byref(msg))        
        finally:
            print "Oh Hot key is over"
            user32.UnregisterHotKey(None, 99)
        '''
      
def handle_start_Event():
    cardId = getCardId()   
    if cardId != None:
        for i in range(1,9): # 删除当前光标之前的8个字符
            PressKey(0x0E)
            ReleaseKey(0x0E)
        for c in cardId:
            scanCode = scanCodeDict[c]
            PressKey(scanCode)
            ReleaseKey(scanCode)
        beep()
    else:
        print("未取得卡信息，请重刷")
    #print "start"
def handle_stop_Event():
    print "stop"

	 
def main():    
    hotKey = HotKey()
    hotKey.setDaemon(True)
    hotKey.start()
    
    while 1:
        time.sleep(1)
        
if __name__ == "__main__":  
    
    main()
