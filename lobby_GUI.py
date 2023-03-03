import os
import sys

from PyQt5.QtWidgets import *
from PyQt5 import uic

def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


# 서로 다른 GUI 연결위해 필요한 코드들
form = resource_path('lobby.ui')
form_class = uic.loadUiType(form)[0]
form_second = resource_path('book_search.ui')
form_secondwindow = uic.loadUiType(form_second)[0]




# 로비 창
class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
    def book_search_btn_click(self):
        self.hide()                     # 메인윈도우 숨김
        self.second = secondwindow()    # 
        self.second.exec()              # 두번째 창을 닫을 때 까지 기다림
        self.show()                     # 두번째 창을 닫으면 다시 첫 번째 창이 보여짐짐



# 도서검색 창
class secondwindow(QDialog,QWidget,form_secondwindow):
    def __init__(self):
        super(secondwindow,self).__init__()
        self.initUi()
        self.show()

    def initUi(self):
        self.setupUi(self)

#    def btn_second_to_main(self):
#        self.close()                    #클릭시 종료됨.







if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()