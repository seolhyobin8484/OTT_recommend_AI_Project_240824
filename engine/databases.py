import pymysql


# 데이터베이스 연결 설정 함수
def connect_db():
    global connect, cursor
    connect = pymysql.connect(
        host='localhost',
        user='root',
        password='1234',
        db='ccm_cinema',
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor
    )
    cursor = connect.cursor()


# 데이터베이스 연결 해제 함수
def disconnect_db():
    if connect:
        connect.close()


# 사용자 데이터를 데이터베이스에 삽입하는 함수
def insert_user(id,password,name,sex,genre):
    """
    user_data는 딕셔너리 형태로, 사용자 정보가 포함되어 있습니다.
    예: {'ID': 'comedian', 'PASSWORD': '12345678', 'NAME': 'KIM DO', 'COUNTRY': 'KOR', 'SEX': 'M', 'GENRE': 'Action'}
    """
    try:
        connect_db()
        query = f"""
        INSERT INTO users (ID, PASSWORD, NAME, SEX, GENRE)
        VALUES ('{id}', '{password}', '{name}', '{sex}', '{genre}')
        """

        cursor.execute(query)
        connect.commit()
        print("사용자 데이터가 성공적으로 삽입되었습니다.")
        return True
    except Exception as e:
        print(f"사용자 삽입 중 오류 발생: {e}")
        return False
    finally:
        disconnect_db()


# 사용자 로그인 함수
def login_user(id, password):
    try:
        connect_db()
        query = "SELECT * FROM users WHERE ID = %s AND PASSWORD = %s"
        cursor.execute(query, (id, password)) #admin 1234
        user = cursor.fetchone()

        if user:
            print(f"로그인 성공! 환영합니다, {user['NAME']}님!")

            return True , user['NAME']
        else:
            print("로그인 실패: ID 또는 비밀번호가 잘못되었습니다.")
            return False, None

    except Exception as e:
        print(f"로그인 중 오류 발생: {e}")
    finally:
        disconnect_db()
def update_user_info(id,password,name,country,sex,genre):
    try:
        connect_db()
        query = "UPDATE ccm_cinema.users SET  PASSWORD = %s, NAME = %s,COUNTRY=%s, SEX=%s, GENRE=%s WHERE (ID = %s);"
        cursor.execute(query, (password,name,country,sex,genre,id))  # admin 1234
        user = cursor.fetchone()
        if user:
            print(f"변경 완료")

            return True, user['NAME']
        else:
            print("변경 실패 정확한 정보를 입력해주세요")
            return False, None

    except Exception as e:
        print(f"로그인 중 오류 발생: {e}")

    query = "UPDATE * FROM users WHERE ID = %s AND PASSWORD = %s"


# 사용자 탈퇴 함수
def delete_user(id):
    # 데이터베이스에 연결
    connect_db()

    try:
        # 사용자를 삭제하는 SQL 쿼리 작성
        query = "DELETE FROM users WHERE ID = %s"

        # 쿼리 실행, 지정된 ID를 가진 사용자 삭제 시도
        cursor.execute(query, (id,))

        # 변경사항 커밋 (실제 데이터베이스에 반영)
        connect.commit()

        # 삭제된 행의 수를 확인하여 삭제 성공 여부를 판단
        if cursor.rowcount > 0:
            # 삭제된 행이 있으면 True 반환
            return True
        else:
            # 삭제된 행이 없으면 False 반환
            return False
    finally:
        # 데이터베이스 연결 해제
        disconnect_db()

# # 메인 프로그램 실행
# while True:
#     print("\n1. 회원가입")
#     print("2. 로그인")
#     print("3. 종료")
#     choice = input("선택하세요: ")
#
#     if choice == '1':
#         user_data = get_user_input()  # 사용자 입력 받기
#         insert_user(user_data)  # 데이터 삽입 함수 호출
#     elif choice == '2':
#         login_user()  # 로그인 함수 호출
#     elif choice == '3':
#         print("프로그램을 종료합니다.")
#         break
#     else:
#         print("잘못된 선택입니다. 다시 시도하세요.")
