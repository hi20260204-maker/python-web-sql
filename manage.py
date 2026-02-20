import pymysql

class Database:

    def __init__(self):
        self.conn = pymysql.connect(
            host = 'localhost',
            port = 3306,
            user = 'root',
            password = 'root1234',
            database = 'user'
            )
        self.cursor = self.conn.cursor()

    #유저의 내용을 DB에서 꺼내옴 if 없으면?
    def get_user(self):
        try:
            select_query = "SELECT * FROM users"
            self.cursor.execute(select_query)
        return self.cursor.fetchall()
    
    #INSERT 쿼리
    def set_user(self, p_name):
        insert_query = "INSERT INTO users VALUES(%S, %S)"
        self.cursor.execute(sql, (p_name))


    
    #close
    def clsoe(self):
        self.conn.close()