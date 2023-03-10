import os
import sys
import sql_server
import barCode
from datetime import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
from PyQt5.QtCore import *

def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


# 서로 다른 GUI 연결위해 필요한 코드들  -> 경로에 ui\\ 붙여야 하위 폴더 경로로 감
# 메인 로비 창 프레임
form = resource_path('ui_set\\lobby.ui')
form_class = uic.loadUiType(form)[0]

# 도서 검색 창 프레임
form_search = resource_path('ui_set\\book_search.ui')
form_searchwindow = uic.loadUiType(form_search)[0]

# 도서 위치 이미지 창 프레임
form_location = resource_path('ui_set\\book_location.ui')
form_locationwindow = uic.loadUiType(form_location)[0]

# 도서 대출 창 프레임
form_rental = resource_path('ui_set\\book_rental.ui')
form_rentalwindow = uic.loadUiType(form_rental)[0]

# 회원가입 창 프레임
form_sign = resource_path('ui_set\\sign.ui')
form_signwindow = uic.loadUiType(form_sign)[0]

# 가입 성공 다이얼
sign_suc = resource_path('ui_set\\sign_up_suc_dial.ui')
sign_suc_dial = uic.loadUiType(sign_suc)[0]

# 가입 실패 다이얼
sign_fail = resource_path('ui_set\\sign_up_fail_dial.ui')
sign_fail_dial = uic.loadUiType(sign_fail)[0]

# 대출 성공 다이얼
rental_suc = resource_path('ui_set\\rental_suc_dial.ui')
rental_suc_dial = uic.loadUiType(rental_suc)[0]

# 반납 성공 다이얼
return_suc = resource_path('ui_set\\return_suc_dial.ui')
return_suc_dial = uic.loadUiType(return_suc)[0]






# 로비 창 프레임
class WindowClass(QMainWindow, form_class):
    
    
    releases = datetime.today().year - 1 # 2023년이지만 책이 2022 뿐이니까      # type int
    # 올해의 신간도서 갯수
    i = sql_server.search_data_by_releases(sql_server.dbconnect(), str(releases))[0][0]
    i -= 1  # 스크롤바의 시작이 0인듯 그래서 3 -> 4 개되니까 하나 줄여야겠어
    count = 0 # 스크롤바의 무빙
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        
        self.new_sb.setMaximum(WindowClass.i)      # 스크롤바 처음 생성시의 크기
        # 시간마다 #
        self.timer = QTimer(self)                   # timer 변수에 QTimer 할당
        self.timer.start(10000)                     # 10000msec(10sec) 마다 반복
        self.timer.timeout.connect(self.scrollbar)    # start time out시 연결할 함수
        
        
    # 초 마다 신간 보여줄 #    
    def scrollbar(self):
        WindowClass.count += 1
        if WindowClass.count > WindowClass.i:
            WindowClass.count = 0
        self.new_sb.setValue(WindowClass.count)             # 10 초마다 1칸 씩 움직임
        
        
        
    
    
        
    def lobby_to_search(self):
        self.hide()                     # 메인윈도우 숨김
        self.search = searchwindow()    # 
        self.search.exec()              # 두번째 창을 닫을 때 까지 기다림
        self.show()                     # 두번째 창을 닫으면 다시 첫 번째 창이 보여짐짐

    def lobby_to_sign(self):
        self.hide()
        self.sign = signwindow() 
        self.sign.exec()
        self.show()
        
    def lobby_to_rental(self):
        self.hide()
        self.rental = rentalwindow() 
        self.rental.exec()
        self.show()    
        
    
# 도서검색 창 프레임
class searchwindow(QDialog,QWidget,form_searchwindow):
    def __init__(self):
        super(searchwindow,self).__init__()
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
        
        
    def location_search(self):
        self.location = locationwindow()
        self.show()
        
        
    # 테이블의 원소를 클릭했을 때 도서 현황 나오기
    def onRightClick(self):
        
        x = self.tableWidget.currentRow()
        #y = self.tableWidget.currentColumn()
        #print('onClick index.row: %s, index.col: %s' % (x, y))
        
        text = self.tableWidget.item(x, 0).text()
        for i in sql_server.search_data_by_title(sql_server.dbconnect(), text):
            # 동일 제목 검색시 / 검색시 딱 하나만 나올 때
            if len(sql_server.search_data_by_title(sql_server.dbconnect(), text)) > 1:
                self.num_line.setText(sql_server.search_data_by_title(sql_server.dbconnect(), text)[x][0])
                self.title_line.setText(sql_server.search_data_by_title(sql_server.dbconnect(), text)[x][1])
                self.author_line.setText(sql_server.search_data_by_title(sql_server.dbconnect(), text)[x][2])
                self.publisher_line.setText(sql_server.search_data_by_title(sql_server.dbconnect(), text)[x][3])
                self.translator_line.setText(sql_server.search_data_by_title(sql_server.dbconnect(), text)[x][4])
                self.release_line.setText(sql_server.search_data_by_title(sql_server.dbconnect(), text)[x][5])
                self.page_line.setText(sql_server.search_data_by_title(sql_server.dbconnect(), text)[x][6])
                self.state_line.setText(sql_server.search_data_by_title(sql_server.dbconnect(), text)[x][8])
                
                #self.location_line.setText(sql_server.search_data_by_title(sql_server.dbconnect(), text)[x][7])    
            else :    
                self.num_line.setText(sql_server.search_data_by_title(sql_server.dbconnect(), text)[0][0])
                self.title_line.setText(sql_server.search_data_by_title(sql_server.dbconnect(), text)[0][1])
                self.author_line.setText(sql_server.search_data_by_title(sql_server.dbconnect(), text)[0][2])
                self.publisher_line.setText(sql_server.search_data_by_title(sql_server.dbconnect(), text)[0][3])
                self.translator_line.setText(sql_server.search_data_by_title(sql_server.dbconnect(), text)[0][4])
                self.release_line.setText(sql_server.search_data_by_title(sql_server.dbconnect(), text)[0][5])
                self.page_line.setText(sql_server.search_data_by_title(sql_server.dbconnect(), text)[0][6])
                self.state_line.setText(sql_server.search_data_by_title(sql_server.dbconnect(), text)[0][8])
                
                #self.location_line.setText(sql_server.search_data_by_title(sql_server.dbconnect(), text)[x][7])
            
            
              
# 도서대출 창 프레임
class rentalwindow(QDialog,QWidget,form_rentalwindow):
    def __init__(self):
        super(rentalwindow,self).__init__()
        self.initUi()
        self.show()

    def initUi(self):
        self.setupUi(self)
    
    # 바코드 입력할려고 카메라 켰을 시
    def input_barcode(self):
        try:
            text = barCode.barcode()
            self.num_line.setText(sql_server.search_data_by_num(sql_server.dbconnect(), text)[0][0])
            self.title_line.setText(sql_server.search_data_by_num(sql_server.dbconnect(), text)[0][1])
            self.author_line.setText(sql_server.search_data_by_num(sql_server.dbconnect(), text)[0][2])
            self.publisher_line.setText(sql_server.search_data_by_num(sql_server.dbconnect(), text)[0][3])
            # self.translator_line.setText(sql_server.search_data_by_num(sql_server.dbconnect(), text)[0][4])
            self.release_line.setText(sql_server.search_data_by_num(sql_server.dbconnect(), text)[0][5])
            self.page_line.setText(sql_server.search_data_by_num(sql_server.dbconnect(), text)[0][6])
            
        except:
            print("에러")
    
    # 도서 대출 버튼 클릭 시
    def book_rental(self):
        text = self.num_line.text()
        sql_server.rental_book(sql_server.dbconnect(), text)
        self.rental_dial = rental_dial()
        self.show()
     
    # 도서 반납 버튼 클릭 시
    def book_return(self):
        text = self.num_line.text()
        sql_server.return_book(sql_server.dbconnect(), text) #
        self.return_dial = return_dial()
        self.show()
    
    
    
# 도서위치 이미지 창 프레임 -> 나중에 이미지 붙임
class locationwindow(QDialog,QWidget,form_locationwindow):
    def __init__(self):
        super(locationwindow,self).__init__()
        self.initUi()
        self.show()

    def initUi(self):
        self.setupUi(self)
        
        # 코드로 위젯 만들었음
        self.lbl = QLabel(self)
        self.lbl.resize(400, 400)
        pixmap = QPixmap('ui_set\\지도.jpg')
        self.lbl.setPixmap(QPixmap(pixmap))
        self.show()
    


# 회원 가입 창 프레임
class signwindow(QDialog,QWidget,form_signwindow):
    def __init__(self):
        super(signwindow,self).__init__()
        self.initUi()
        self.show()

    def initUi(self):
        self.setupUi(self)
        
    
    ## id 중복 체크 버튼 ##
    def id_check(self):
        text = self.id_line.text()
        
        try:
            if sql_server.id_check(sql_server.dbconnect(), text)[0][0] == text:
                print("중복")
        except:
            print("중복없음")
    
    # 회원 가입 버튼
    def sign(self):
        id = self.id_line.text()
        pw = self.pw_line.text()
        name = self.name_line.text()
        address = self.address_line.text()
        phone = self.phone_line.text()
        e_mail = self.e_mail_line.text()
        
        # 가입 성공시 / 실패시
        try:
            sql_server.insert_user_data(sql_server.dbconnect(), id, pw, name, address, phone, e_mail)
            self.suc_dial = suc_dial()
            self.show()
        except:
            self.fail_dial = fail_dial()
            self.show()
     



# ↓ 다이얼 , ↑ 프레임

# 가입 성공 다이얼
class suc_dial(QDialog,QWidget, sign_suc_dial):
    def __init__(self):
        super(suc_dial, self).__init__()
        self.initUi()
        self.show()

    def initUi(self):
        self.setupUi(self)
    
    def dial_close(self):
        self.close()
        
# 가입 실패 다이얼
class fail_dial(QDialog,QWidget, sign_fail_dial):
    def __init__(self):
        super(fail_dial, self).__init__()
        self.initUi()
        self.show()

    def initUi(self):
        self.setupUi(self)
    
    def dial_close(self):
        self.close()

# 대출 성공 다이얼
class rental_dial(QDialog,QWidget, rental_suc_dial):
    def __init__(self):
        super(rental_dial, self).__init__()
        self.initUi()
        self.show()

    def initUi(self):
        self.setupUi(self)
    
    def dial_close(self):
        self.close()
        
# 반납 성공 다이얼
class return_dial(QDialog,QWidget, return_suc_dial):
    def __init__(self):
        super(return_dial, self).__init__()
        self.initUi()
        self.show()

    def initUi(self):
        self.setupUi(self)
    
    def dial_close(self):
        self.close()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()