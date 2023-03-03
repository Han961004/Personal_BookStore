# 클라이언트에서 책이나 서적의 정보들을 소켓을 통해 받아서 서버에서 실행하여 서버의 DB에 저장하도록 함


import pymysql


# DAO class userDAO:        class bookDAO:          DAO를 쓸까?



# db 연결               user password db host 각자의 상황에 맞게 변경                     은닉화 필요?
def dbconnect():
    conn = pymysql.connect(host='localhost', user='root', password='1234', db='book', charset='utf8')
    # cur = con.cursor()
    return conn

# 책이름으로 데이터 가져오기
def search_data_by_title(conn, title):
    cur = conn.cursor()
    sql = 'select * from book_info where title = ' + title       # ; 붙?
    cur.execute(sql)
    res = cur.fetchall()
    print(res)                                                   # 수정필
    
# id pw 로 유저정보 가져오기  ->  로그인 
def search_data_by_id_pw(conn, id, pw):
    cur = conn.cursor()
    sql = 'select * from user_info where id = ' + id             # 수정필               AND (Age<25  OR Nm_Kor = '홍길동')
    cur.execute(sql)
    res = cur.fetchall()
    print(res)                                                   # 수정필
    

            
# 책 데이터 추가하기
def insert_book_data(conn, num, title, author, translator, release, price, image):
    cur = conn.cursor()
    sql = "insert into book_info (num, title, author, translator, release, price, image) values ('" + num + "', '" + title + "', '" + author + "', '" + translator + "', '" + release + "', '" + price + "', '" + image + "') "
    cur.execute(sql)
    conn.commit()

# 유저 회원가입
def insert_user_data(conn, id, pw, name, address, phone, e_mail, purchase, mileage):
    cur = conn.cursor()
    sql = "insert into user_info (id, pw, name, address, phone, e-mail, purchase, mileage) values ('" + id + "', '" + pw + "', '" + name + "', '" + address + "', '" + phone + "', '" + e_mail + "', '" + purchase + "', '" + mileage + "') "
    cur.execute(sql)
    conn.commit()
    
# 책 데이터 삭제
def delete_book_data(conn, num):
    cur = conn.cursor()
    sql = "delete from book_info where num = '" + num + "' "
    cur.execute(sql)
    conn.commit()


# 유저 (회원 탈퇴) 데이터 삭제  ->  로그인 한 상태에서 회원탈퇴 버튼 클릭시 경고문 한번 띄우고 바로 탈퇴
def delete_user_data(conn, id):
    cur = conn.cursor()
    sql = "delete from user_info where id = '" + id + "' "
    cur.execute(sql)
    conn.commit()


# 책 데이터 수정




# 유저 데이터 수정




#






