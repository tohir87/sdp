import datetime
from flask_mail import Mail, Message


class Farm:
    def __init__(self, param, conn):
        self.param = param
        self.conn = conn
        # create a cursor
        self.cur = conn.cursor()
        # self.mail = Mail(app)

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

    def checkDataAgaintRules(self):
        # get rules where temperature is set
        self.cur.execute(
            "SELECT rules.*, alerts.tag_name, alerts.message FROM rules INNER JOIN alerts ON alerts.id = rules.alert_id WHERE rules.rule_type = %s", ['Exceed'])

        return self.cur.fetchall()

    def saveFeedQuantity(self):
        weight = self.param['weight']

        print(weight)

        # insert new record inside feed weight table
        self.cur.execute("INSERT INTO weight_sensor_readings (reading_date, reading_time, weight) VALUES (date('now'), now()::time ,%s)", [
            weight])

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

    def getFeedReading(self):
        self.cur.execute(
            "SELECT * FROM weight_sensor_readings ORDER BY id DESC LIMIT 50")
        return self.cur.fetchall()

    def getTempHumidData(self):
        start_date = self.param['start_date']
        end_date = self.param['end_date']

        self.cur.execute(
            "SELECT * FROM dht_sensor_readings WHERE reading_date >= %s and reading_date <= %s", [
                start_date, end_date])
        return self.cur.fetchall()

    def fetchAlerts(self):
        self.cur.execute(
            "SELECT * FROM alerts")
        return self.cur.fetchall()

    def fetchRules(self):
        self.cur.execute(
            "SELECT rules.*, alerts.tag_name FROM rules INNER JOIN alerts ON alerts.id = rules.alert_id")
        return self.cur.fetchall()

    def createAlert(self):
        # Grab form entries
        tag = self.param['tag']
        message = self.param['message']

        # Insert new settings
        self.cur.execute("INSERT INTO alerts (tag_name, message) VALUES (%s, %s)", [
                         tag, message])

        return self.conn.commit()

    def createRule(self):
        # Grab form entries
        sensor = self.param['sensor']
        rule_type = self.param['rule_type']
        rule_value = self.param['rule_value']
        alert_id = self.param['alert_id']

        # Insert new settings
        self.cur.execute("INSERT INTO rules (sensor, rule_type, rule_value, alert_id) VALUES (%s, %s, %s, %s)", [
                         sensor, rule_type, rule_value, alert_id])

        return self.conn.commit()

    def deleteRule(self):
        id = self.param['id']

        # Delete selected ID from rules table
        self.cur.execute("DELETE FROM rules WHERE id = %s", [
                         id])

        return self.conn.commit()

    def deleteAlert(self):
        id = self.param['id']

        # Delete selected ID from rules table
        self.cur.execute("DELETE FROM alerts WHERE id = %s", [
                         id])

        return self.conn.commit()
