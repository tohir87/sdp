import datetime


class Farm:
    def __init__(self, param, conn):
        self.param = param
        self.conn = conn
        # create a cursor
        self.cur = conn.cursor()

    def login(self):
        email = self.param['email']
        password = self.param['password']

        self.cur.execute(
            'SELECT * FROM users WHERE email = %s and password = %s', [email, password])
        return self.cur.fetchall()

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

    def saveSensorData(self):
        temperature = self.param['temperature']
        humidity = self.param['humidity']

        print(temperature, humidity)

        # insert new record inside temp table
        self.cur.execute("INSERT INTO dht_sensor_readings (reading_date, reading_time, temperature, humidity) VALUES (date('now'), now()::time ,%s,%s)", [
            temperature, humidity])

        return self.conn.commit()

    def saveSettings(self):
        # delete previous setting
        self.cur.execute('DELETE FROM settings')

        # Grab form entries
        min_temperature = self.param['min_temperature']
        max_temperature = self.param['max_temperature']
        emergency_email = self.param['emergency_email']
        emergency_phone = self.param['emergency_phone']

        # Insert new settings
        self.cur.execute("INSERT INTO settings (min_temperature, max_temperature, emergency_email, emergency_phone) VALUES (%s, %s, %s, %s)", [
                         min_temperature, max_temperature, emergency_email, emergency_phone])

        return self.conn.commit()

    def getSetting(self):
        self.cur.execute("SELECT * FROM settings ORDER BY id DESC LIMIT 1")
        return self.cur.fetchall()
