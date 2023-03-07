import os
import sys

########
import sql_server 
########


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
        
    def lobby_to_search(self):
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
        
    def book_search(self):
        # 검색어 입력받은 변수, 이걸로 sql 검색할 것
        text = self.book_search_edit.text()
        category = self.book_search_category.currentText()

        # 검색할 때 마다 테이블 초기화
        self.tableWidget.setRowCount(0)
        
        # 콤보박스가 제목일 때
        if(category == "제목"):
            for i in sql_server.search_data_by_title(sql_server.dbconnect(), text):
                row = self.tableWidget.rowCount()
                self.tableWidget.insertRow(row)
                self.tableWidget.setItem(row, 0, QTableWidgetItem(sql_server.search_data_by_title(sql_server.dbconnect(), text)[row][1]))
                self.tableWidget.setItem(row, 1, QTableWidgetItem(sql_server.search_data_by_title(sql_server.dbconnect(), text)[row][2]))
                self.tableWidget.setItem(row, 2, QTableWidgetItem(sql_server.search_data_by_title(sql_server.dbconnect(), text)[row][3]))
                self.tableWidget.setItem(row, 3, QTableWidgetItem(sql_server.search_data_by_title(sql_server.dbconnect(), text)[row][5]))
        # 콤보박스가 저자
        # 콤보박스가 출판사
        # 콤보박스가 연도
        
        
        
    # 테이블의 원소를 클릭했을 때 도서 현황 나오기
    def onRightClick(self):
        
        x = self.tableWidget.currentRow()
        #y = self.tableWidget.currentColumn()
        #print('onClick index.row: %s, index.col: %s' % (x, y))
        
        text = self.tableWidget.item(x, 0).text()
        for i in sql_server.search_data_by_title(sql_server.dbconnect(), text):
            self.num_line.setText(sql_server.search_data_by_title(sql_server.dbconnect(), text)[x][0])
            self.title_line.setText(sql_server.search_data_by_title(sql_server.dbconnect(), text)[x][1])
            self.author_line.setText(sql_server.search_data_by_title(sql_server.dbconnect(), text)[x][2])
            self.publisher_line.setText(sql_server.search_data_by_title(sql_server.dbconnect(), text)[x][3])
            #self.translator_line.setText(sql_server.search_data_by_title(sql_server.dbconnect(), text)[x][4])
            self.release_line.setText(sql_server.search_data_by_title(sql_server.dbconnect(), text)[x][5])
            #self.page_line.setText(sql_server.search_data_by_title(sql_server.dbconnect(), text)[x][6])
            #self.location_line.setText(sql_server.search_data_by_title(sql_server.dbconnect(), text)[x][7])
            
            

        
        
            
            
        



if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()