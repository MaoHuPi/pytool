import os
import sys
import mouse
import win32gui
from PyQt5.QtCore import *
from PyQt5 import QtWebChannel
from PyQt5.QtWebChannel import *
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import *

app = QApplication(sys.argv)
# app.setAttribute(Qt.AA_UseSoftwareOpenGL, True)

web = QWebEngineView()
winId = int(web.winId())
web.setWindowTitle('desktopBackground')
web.setWindowFlags(Qt.FramelessWindowHint)

class Handler(QObject):
    def __init__(self):
        super(Handler, self).__init__()

    @pyqtSlot(str, result = bool)
    def log(self, msg):
        print(msg)
        return(True)
    
    @pyqtSlot(str, result = bool)
    def setMousePosition(self, text):
        mousePosition = mouse.get_position()
        web.page().runJavaScript('''
            window.mousePosition = {'x': %d, 'y': %d}
            window.mouseDown = true;
        ''' % (int(mousePosition[0]), int(mousePosition[1])))
        return(True)

# web.setGeometry(0, 0, 500, 300)
# web.load(QUrl('https://maohupi.github.io/cvsArt/%E7%81%AB%E8%8A%B1/index.html'))

''' qurl '''
web.load(QUrl.fromLocalFile(sys.argv[1]))

''' fopen '''
# file = open(sys.argv[1], 'r', encoding = 'utf-8')
# html = file.read()
# file.close()
# page = QWebEnginePage()
# page.setHtml(html)
# web.setPage(page)

channel = QWebChannel()
handler = Handler()
channel.registerObject('handler', handler)
web.page().setWebChannel(channel) # qurl
# page.setWebChannel(channel) # fopen

def pretreatmentHandle():
    hwnd = win32gui.FindWindow("Progman", "Program Manager")
    win32gui.SendMessageTimeout(hwnd, 0x052C, 0, None, 0, 0x03E8)
    hwnd_WorkW = None
    while 1:
        hwnd_WorkW = win32gui.FindWindowEx(None, hwnd_WorkW, "WorkerW", None)
        if not hwnd_WorkW:
            continue
        hView = win32gui.FindWindowEx(hwnd_WorkW, None, "SHELLDLL_DefView", None)
        # print('hwmd_hView: ', hView)
        if not hView:
            continue
        h = win32gui.FindWindowEx(None, hwnd_WorkW, "WorkerW", None)
        while h:
            win32gui.SendMessage(h, 0x0010, 0, 0)  # WM_CLOSE
            h = win32gui.FindWindowEx(None, hwnd_WorkW, "WorkerW", None)
        break
    return hwnd

if __name__ == "__main__":
    # web.show()
    web.showFullScreen()

    win32gui.SetParent(winId, pretreatmentHandle())

    # os.system('taskkill /f /pid %d' % (winId))
    # sys.exit()

    sys.exit(app.exec())
