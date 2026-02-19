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

    #SELECT 쿼리
    def get_user(self):
        try:
            select_query = "SELECT * FROM users"
            self.cursor.execute("SELECT * FROM users")
        return self.cursor.fetchall()
    
    #INSERT 쿼리
    def set_user(self)

    
    #close
    def clsoe(self):
        self.conn.close()