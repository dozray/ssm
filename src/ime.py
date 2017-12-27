import win32con  
import win32api  
  
class InputMethod(list):  
    def __init__(self):  
        name = "Keyboard Layout\\Preload"  
        key_id = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER, name)  
        
        name = "System\\CurrentControlSet\\Control\\Keyboard Layouts\\"  
        _i, _running, _ids = 1, True, list()  
        while _running:  
            try:  
                _id = win32api.RegQueryValueEx(key_id, str(_i))[0]
                print _id
                _i += 1  
                _k_name = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE, name + _id)
                print _k_name
                _name = win32api.RegQueryValueEx(_k_name, 'Layout Text')[0]  
                self.append((_id, _name))  
                win32api.RegCloseKey(_k_name)  
            except:  
                _running = False  
                win32api.RegCloseKey(key_id)  
  
    def set(self, _im):       
        hkl = win32api.LoadKeyboardLayout(_im[0], win32con.KLF_ACTIVATE)
        print hkl
        #if hkl is None
            #return -2
        #else
        win32api.ActivateKeyboardLayout(hkl,win32con.KLF_SETFORPROCESS) # Active ime
  
      
if __name__ == '__main__':  
    im = InputMethod()  
    for i, v in enumerate(im):  
        print '【输入法%d】: %s'  % (i, v[1])  
    try:  
        i = input('设置输入法(输入数字并回车): ')  
        im.set(im[i])  
        print '成功将输入法设置为【%s】' % im[i][1]  
    except:  
        print '输入有误'  
