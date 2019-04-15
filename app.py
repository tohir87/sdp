from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import os
from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_restful import Resource, Api
import datetime
from classes.farm import Farm
import psycopg2

app = Flask(__name__)
# app = Flask(__name__, static_url_path=os.getcwd() + 'static/vendor1')
app.config.from_object(os.environ['APP_SETTINGS'])
print(os.environ['APP_SETTINGS'])

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))
    email = db.Column(db.String(128))
    phone = db.Column(db.String(128))
    password = db.Column(db.String(128))


class DhtData(db.Model):
    __tablename__ = "dht_sensor_readings"

    id = db.Column(db.Integer, primary_key=True)
    reading_date = db.Column(db.Date())
    reading_time = db.Column(db.Time())
    temperature = db.Column(db.String(128))
    humidity = db.Column(db.String(128))


class WeightData(db.Model):
    __tablename__ = "weight_sensor_readings"

    id = db.Column(db.Integer, primary_key=True)
    reading_date = db.Column(db.Date())
    reading_time = db.Column(db.Time())
    weight = db.Column(db.String(128))


class Settings(db.Model):
    __tablename__ = "settings"

    id = db.Column(db.Integer, primary_key=True)
    min_temperature = db.Column(db.Integer)
    max_temperature = db.Column(db.Integer)
    emergency_email = db.Column(db.String(128))
    emergency_phone = db.Column(db.String(128))


def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        return psycopg2.connect(os.environ['DATABASE_URL'])

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


@app.route('/api/post_reading', methods=["POST", "GET"])
def post_reading():

    # create a database connection
    conn = connect()
    with conn:
        print("posting data from sensor")
        farm = Farm(request.args, conn)
        # Complete signup
        farm.saveSensorData()

    return "Ok"


@app.route('/api/get_temp_humid', methods=["GET", "POST"])
def get_temp_humid():

    # get url params
    startDate = request.args.get('start_date')
    endDate = request.args.get('end_date')

    temp = []
    humid = []
    dates = []

    # create a database connection
    conn = connect()
    with conn:
        print("2. Query all temps")
        farm = Farm(request.args, conn)
        dht_data = farm.getTempHumidData()

        # build data
        for row in dht_data:
            temp.append(row[3])
            humid.append(row[4])
            dates.append(row[1])

    return jsonify({'temperature': temp, 'humidity': humid, 'categories': dates})


@app.route('/api/post_feed_weight', methods=["POST", "GET"])
def post_feed_weight():

    # create a database connection
    conn = connect()
    with conn:
        print("posting data from weight sensor")
        farm = Farm(request.args, conn)
        # Complete signup
        farm.saveFeedQuantity()

    return "Ok"


@app.route('/setup')
def setup():
    return render_template("setup.html")


@app.route('/')
def login():
    return render_template("login.html")


@app.route('/about')
def about():
    return jsonify({'name': "Thohiru Omoloye", 'student No.': "2950574"})


@app.route('/test')
def test():
    page_title = "Page title"
    page_desc = "Page desc"

    conn = connect()
    # create a cursor
    cur = conn.cursor()

    # execute a statement
    print('PostgreSQL database version:')
    cur.execute('SELECT version()')

    # display the PostgreSQL database server version
    db_version = cur.fetchone()
    page_desc = db_version
    print(db_version)

    # close connection
    conn.close()

    return render_template("test.html", **locals())


@app.route('/doSetUp', methods=['POST'])
def doSetup():
    # Initialise the Farm class and pass submitted form inputs across
    farm = Farm(request.form,  connect())
    # Complete signup
    farm.signUp()

    # redirect to login page
    return redirect(url_for('login'))


@app.route('/doLogin', methods=['POST'])
def doLogin():
    # Initialise the Farm class and pass submitted form inputs across
    farm = Farm(request.form,  connect())
    # Complete signup
    hasAccount = farm.login()

    print(len(hasAccount))

    return_route = "login"
    if (len(hasAccount) > 0):
        return_route = "settings"

    # redirect to needed page
    return redirect(url_for(return_route))


@app.route('/processSettings', methods=['POST'])
def processSettings():
    # Initialise the Farm class and pass submitted form inputs across
    farm = Farm(request.form,  connect())
    # Complete signup
    farm.saveSettings()

    # redirect back to settings page
    return redirect(url_for('settings'))


@app.route('/settings')
def settings():

    page_title = "Settings"
    page_desc = "Available settings"

    max_temp = 0
    min_temp = 0
    emergency_email = ""
    emergency_phone = ""

    # Create connection
    conn = connect()
    with conn:
        print("Getting the previous setting")
        farm = Farm([],  conn)
        # Get settings
        previousSetting = farm.getSetting()

        if previousSetting:
            min_temp = previousSetting[0][1]
            max_temp = previousSetting[0][2]
            emergency_email = previousSetting[0][3]
            emergency_phone = previousSetting[0][4]

    return render_template("settings.html", **locals())


@app.route('/report')
def report():

    page_title = "Report"
    page_desc = "Temperature, humidity, feed and water level report over time"

    # dht_data = []
    # feed_data = []

    # Create connection
    conn = connect()
    with conn:
        print("Getting the sensor readings")
        farm = Farm([],  conn)
        # Get readings
        dht_data = farm.getDHTReading()
        print(dht_data)
        feed_data = farm.getFeedReading()
        print(feed_data)

    return render_template("report.html", **locals())


@app.route('/analytics')
def analytics():

    page_title = "Report"
    page_desc = "Analytics"

    # Create connection
    conn = connect()
    with conn:
        print("Getting the sensor readings")
        farm = Farm([],  conn)
        # Get readings
        dht_data = farm.getDHTReading()
        print(dht_data)
        feed_data = farm.getFeedReading()
        print(feed_data)

    return render_template("analytics.html", **locals())


if __name__ == '__main__':
    app.run()
