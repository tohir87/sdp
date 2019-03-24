import datetime


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

    def saveSensorData(self):
        temperature = self.param['temperature']
        humidity = self.param['humidity']

        print(temperature, humidity)

        # insert new record inside temp table
        self.cur.execute("INSERT INTO dht_sensor_readings (reading_date, reading_time, temperature, humidity) VALUES (date('now'), now()::time ,%s,%s)", [
            temperature, humidity])

        return self.conn.commit()
