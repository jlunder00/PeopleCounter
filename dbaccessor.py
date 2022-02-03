import mysql.connector

class DBAccessor:
    def __init__(self, usr, pwd, hst, db):
        self.usr = usr
        self.pwd = pwd
        self.hst = hst
        self.db = db
        self.con, self.rs = self.connect(self.usr, self.pwd, self.hst, self.db)
        if self.con is None and self.rs is None:
            print("Connection Refused")
        
        

    def connect(self, usr, pwd, hst, db):
        try:
            # create a connection
            con = mysql.connector.connect(user=usr,password=pwd, host=hst, database=db)
            # create a result set
            rs = con.cursor()

            return con, rs
        except mysql.connector.Error as err:
            print(err)
            return None, None

    def close_connection(self):
        if self.con is not None and self.rs is not None:
            self.rs.close()
            self.con.close()
        
    def query_db(self, qy, vals = None):
        if self.con is not None and self.rs is not None:
            print(qy, vals)
            if vals is not None:
                self.rs.execute(qy, vals)
            else:
                self.rs.execute(qy)
            if 'UPDATE' in qy or 'INSERT' in qy:
                self.con.commit()

    def get_rs(self):
        return self.rs




