class Farm:
    def __init__(self, param, conn):
        self.param = param
        self.conn = conn
        # create a cursor
        self.cur = conn.cursor()

    def signUp(self):
        first_name = self.param['first_name']
        last_name = self.param['last_name']
        email = self.param['email']
        phone = self.param['phone']
        password = self.param['password1']

        print(first_name, last_name, email, phone, password)

        # insert record
        self.cur.execute('INSERT INTO users (first_name, last_name, email, phone, password) values (%s, %s, %s, %s, %s )', [
                         first_name, last_name, email, phone, password])
        self.conn.commit()
        return self.conn.commit()
