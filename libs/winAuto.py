from pywinauto import Application
from PIL import ImageGrab
import os
import time
import datetime
import win32gui
import win32con

def check_fde_status():
      cptrayUI = os.environ["ProgramFiles(x86)"] + "\\CheckPoint\\Endpoint Security\\UIFramework\\bin\\cptrayUI.exe"
      app = Application().connect(path=cptrayUI)
      dlg = app.window(title='Check Point Endpoint Security')

      #print(pywinauto.findwindows.find_element(title='Check Point Endpoint Security'))
      #print(app.findwindows.find_elements())

      if dlg.exists():
          dlg.set_focus()
          print("dlg found", dlg)
      else:
         print("No dlg found")

      dlg.wait('ready')

      dlg[u'Full Disk Encryption'].click_input()

      screenshot()
      dlg.minimize()

      app.kill()

def open_tray():

    def get_handle(name):
        def check(hwnd, param):
            title = win32gui.GetWindowText(hwnd)
            if name in title:
                param.append(hwnd)
        winds = []
        win32gui.EnumWindows(check, winds)
        return winds

    handle = get_handle('Check Point Endpoint Security')


    win32gui.SendMessage(handle[0], 0xC248)
    win32gui.SendMessage(handle[0], 0xC0A8)

   # win32gui.ShowWindow(handle[0], win32con.SW_SHOW)
   # win32gui.ShowWindow(handle[0], win32con.SW_SHOWNORMAL)
   # win32gui.ShowWindow(handle[0], win32con.SW_RESTORE)
   # win32gui.RedrawWindow(handle[0], None, None, win32con.RDW_UPDATENOW)
   # win32gui.UpdateWindow(handle[0])


def collect_polices():
    time.sleep(1)

def screenshot():
    time.sleep(0.5)
    imgdir = os.environ["HOMEDRIVE"]+'\\test_screenshots'

    if not os.path.exists(imgdir):
        os.makedirs(imgdir)

    os.chdir(imgdir)
    currentTime = str(datetime.datetime.now().strftime('%Y%m%d%H%M%S')+'.png')
    ImageGrab.grab().save(currentTime)

    print(currentTime+' saved to '+os.getcwd())


def main():
    print()
if __name__ == '__main__':
    main()