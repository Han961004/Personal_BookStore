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
    sql = "select * from book_info where title like '%" + title + "%' "
    cur.execute(sql)
    res = cur.fetchall()
    return res                                                   # 수정필
    
# 바코드로 데이터 불러오기
def search_data_by_num(conn, num):
    cur = conn.cursor()
    sql = "select * from book_info where num = " + num + " " 
    cur.execute(sql)
    res = cur.fetchall()
    return res     

# 연도로 데이터 불러오기
def search_data_by_releases(conn, releases):
    cur = conn.cursor()
    sql = "select count(if(releases = " + releases + ", releases, null)) from book_info" 
    cur.execute(sql)
    res = cur.fetchall()
    return res     


# 대출 버튼 눌렀을 때, 대출가능 -> 대출불가 
def rental_book(conn, num):
    cur = conn.cursor()
    sql = "UPDATE book_info SET state = '대출불가' WHERE num = '" + num + "'"
    cur.execute(sql)
    conn.commit()

# 대출 반납 버튼 눌렀을 때, 대출불가 -> 대출가능
def return_book(conn, num):
    cur = conn.cursor()
    sql = "UPDATE book_info SET state = '대출가능' WHERE num = '" + num + "'"
    cur.execute(sql)
    conn.commit()
    
    
# 회원 가입시 중복체크 
def id_check(conn, id):
    cur = conn.cursor()
    sql = "select id from user_info where id = '" + id + "' "            # 수정필               AND (Age<25  OR Nm_Kor = '홍길동')
    cur.execute(sql)
    res = cur.fetchall()
    return res

# 유저 회원가입
def insert_user_data(conn, id, pw, name, address, phone, e_mail):
    cur = conn.cursor()
    sql = "insert into user_info (id, pw, name, address, phone, e_mail) values ('" + id + "', '" + pw + "', '" + name + "', '" + address + "', '" + phone + "', '" + e_mail + "') "
    cur.execute(sql)
    conn.commit()
    

            
# 책 데이터 추가하기
def insert_book_data(conn, num, title, author, translator, release, price, image):
    cur = conn.cursor()
    sql = "insert into book_info (num, title, author, translator, release, price, image) values ('" + num + "', '" + title + "', '" + author + "', '" + translator + "', '" + release + "', '" + price + "', '" + image + "') "
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






