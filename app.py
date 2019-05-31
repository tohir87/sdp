from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import os
from flask import Flask, session, escape, render_template, jsonify, request, redirect, url_for, abort, flash
from flask_restful import Resource, Api
from datetime import datetime, timedelta
from classes.farm import Farm
import psycopg2
from flask_login import current_user, LoginManager, login_user, UserMixin
from flask_mail import Mail, Message
from sqlalchemy import desc, update
from urllib.request import urlopen

app = Flask(__name__)
# Init mail
mail = Mail(app)
app.config.from_object(os.environ['APP_SETTINGS'])
print(os.environ['APP_SETTINGS'])
mail = Mail(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))
    email = db.Column(db.String(128))
    phone = db.Column(db.String(128))
    password = db.Column(db.String(128))
    user_type_id = db.Column(db.SmallInteger(), default=0)
    farm_name = db.Column(db.String(128))


class DhtData(db.Model):
    __tablename__ = "dht_sensor_readings"

    id = db.Column(db.Integer, primary_key=True)
    reading_date = db.Column(db.Date())
    reading_time = db.Column(db.Time())
    temperature = db.Column(db.String(128))
    humidity = db.Column(db.String(128))
    water_level = db.Column(db.Integer)
    feed_level = db.Column(db.String(128))


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


class Alerts(db.Model):
    __tablename__ = "alerts"

    id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String(255))
    message = db.Column(db.String(255))


class Rules(db.Model):
    __tablename__ = "rules"

    id = db.Column(db.Integer, primary_key=True)
    sensor = db.Column(db.String(255))
    rule_type = db.Column(db.String(255))
    rule_value = db.Column(db.Integer)
    alert_id = db.Column(db.Integer, db.ForeignKey('alerts.id'))

class Devices(db.Model):
    __tablename__ = "devices"

    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(255))
    serial = db.Column(db.String(255))
    acquired_on = db.Column(db.Date())

class UserDevices(db.Model):
    __tablename__ = "user_devices"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    device_id = db.Column(db.Integer, db.ForeignKey('devices.id'))



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


def sendNotification(row):
    print(row.rule_type, row.rule_value, row.message)

    print('sending ' + row.message)
    msg = Message('Alert: ' + row.tag_name, sender='bot@smartfarm.com',
                  recipients=['otcleantech@gmail.com'])
    msg.body = row.message
    mail.send(msg)
    url = "https://api.africastalking.com/restless/send?message=" + row.message + \
        "&username=tbasetest2018&Apikey=ceeabb27657cd6cfb3952dfae8b7943b4975dbee6a5b55fd4819f333bb1100ee&to=" + \
            "+353894574866" 
            # + str(session['phone'])
    # urlopen(url)
    return


@app.route('/api/post_reading', methods=["POST", "GET"])
def post_reading():
    print("posting data from sensor")

    temperature = request.args['temperature']
    humidity = request.args['humidity']
    water_level = request.args['water_level']
    feed_level = 0 #request.args['feed_level']
    reading_date = datetime.now().strftime('%Y-%m-%d')
    reading_time = datetime.now().strftime('%H:%M:%S')

    # Save new sensor readings
    new_reading = DhtData(reading_date=reading_date,reading_time=reading_time,temperature=temperature,humidity=humidity,water_level=water_level,feed_level=feed_level)

    # Add new record to db
    db.session.add(new_reading)
    db.session.commit()

    rule_type_below = "Below"
    rule_type_exceed = "Exceed"
    # results = farm.checkDataAgaintRules()
    results_exceed = Rules.query.join(Alerts, Alerts.id == Rules.alert_id).add_columns(
        Rules.sensor, Rules.rule_type, Rules.rule_value, Alerts.message, Alerts.tag_name).filter(Rules.rule_type == rule_type_exceed)

    # with results xceeding settings:
    if results_exceed.count() > 0:
        for row in results_exceed:
            if row.sensor == 'Temperature' and int(request.args['temperature']) > row.rule_value:
                sendNotification(row)
            elif row.sensor == 'Humidity' and int(request.args['humidity']) > row.rule_value:
                sendNotification(row)

    results_below = Rules.query.join(Alerts, Alerts.id == Rules.alert_id).add_columns(Rules.sensor, Rules.rule_type, Rules.rule_value, Alerts.message, Alerts.tag_name).filter(Rules.rule_type == rule_type_below)

    # with results below settings:
    if results_below.count() > 0:
        for row in results_below:
            if row.sensor == 'Water Level' and int(request.args['water_level']) < row.rule_value:
                sendNotification(row)
            elif row.sensor == 'Humidity' and int(request.args['humidity']) < row.rule_value:
                sendNotification(row)
            elif row.sensor == 'Temperature' and int(request.args['temperature']) < row.rule_value:
                sendNotification(row)

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
            temp.append(float(row[3]))
            humid.append(float(row[4]))
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


@app.route('/logout')
def logout():
    # destroy session
    session.pop('id', None)
    session.pop('first_name', None)
    session.pop('last_name', None)
    session.pop('email', None)
    session.pop('phone', None)

    return redirect(url_for('login'))


@app.route('/about')
def about():
    return jsonify({
        'name': "Thohiru Omoloye",
        'student No.': "2950574",
        'email': "thohiru.omoloye@student.griffith.ie",
        'level': "Year 4",
        'course': "Computing Science"
    })


@app.route('/test_mail')
def testMail():
    msg = Message('Hello', sender='bot@smartfarm.com',
                  recipients=['otcleantech@gmail.com'])
    msg.body = "Hello, this is just a test email"
    mail.send(msg)
    return "Sent"


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
    error = None

    email = request.form['email']
    password = request.form['password']

    userInfo = User.query.filter_by(email=email,password=password).first()

    if (userInfo):
        print(userInfo)
        # Set session vars
        session['id'] = userInfo.id
        session['first_name'] = userInfo.first_name
        session['last_name'] = userInfo.last_name
        session['email'] = userInfo.email
        session['phone'] = userInfo.phone
        session['farm_name'] = userInfo.farm_name
        session['logged_in'] = True
        # redirect to needed page
        return redirect(url_for('home'))
    else:
        error = 'Invalid email or password. Please try again'
    return render_template("login.html", error=error)


@app.route('/settings')
def settings():

    if 'first_name' in session:
        page_title = "Settings"
        page_desc = "Available settings"

        user_id = session['id']
        farm = User.query.filter_by(id=user_id).first()

        return render_template("settings/settings.html", **locals())

    else:
        flash("You are not logged in")
        return redirect(url_for('login'))
    

@app.route('/report')
def report():

    page_title = "Report"
    page_desc = "Temperature, humidity, feed and water level report over time"

   
    print("Getting the sensor readings")
    # Get readings
    dht_data = DhtData.query.order_by(desc('id')).all()
    print(dht_data)

    return render_template("report.html", **locals())


@app.route('/home')
def home():
    if 'first_name' in session:
        page_title = "Home"
        page_desc = "Welcome " + session['first_name']

        # get the last row from dht table
        recent_reading = DhtData.query.order_by(desc('id')).first()
        # get the last recorded feed weight
        recent_weight = WeightData.query.order_by(desc('id')).first()

        return render_template("home.html", **locals())
    else:
        flash("You are not logged in")
        return redirect(url_for('login'))


@app.route('/analytics')
def analytics():

    page_title = "Report"
    page_desc = "Analytics"

    # Get readings
    dht_data = DhtData.query.order_by(desc('id')).all()
    print(dht_data)

    return render_template("analytics.html", **locals())


@app.route('/settings/alert')
def alert():
    if 'first_name' in session:
        # Initialise the Farm class and pass submitted form inputs across
        farm = Farm(request.form,  connect())
        # Complete signup
        alerts = farm.fetchAlerts()

        page_title = "Settings"
        page_desc = ""

        return render_template("settings/alert.html", **locals())
    else:
        flash("You are not logged in")
        return redirect(url_for('login'))


@app.route('/settings/rules')
def rule():
    if 'first_name' in session:
        # Initialise the Farm class and pass submitted form inputs across
        farm = Farm(request.form,  connect())
        # Complete signup
        rules = farm.fetchRules()
        alerts = farm.fetchAlerts()

        page_title = "Settings"
        page_desc = ""
        return render_template("settings/rules.html", **locals())
    else:
        flash("You are not logged in")
        return redirect(url_for('login'))


@app.route('/processSettings', methods=['POST'])
def processSettings():
    # Get form fields
    farm_name = request.form['farm_name']
    phone = request.form['phone']
    id = session['id']

    # update info in database
    user = User.query.get(id)
    user.farm_name = farm_name
    user.phone = phone
    db.session.commit()

    # redirect back to settings page
    return redirect(url_for('settings'))


@app.route('/createAlert', methods=['POST'])
def createAlert():
    if 'first_name' in session:
        # Initialise the Farm class and pass submitted form inputs across
        farm = Farm(request.form,  connect())
        # Complete signup
        farm.createAlert()

        # redirect back to alert page
        return redirect(url_for('alert'))
    else:
        flash("You are not logged in")
        return redirect(url_for('login'))


@app.route('/settings/delete_alert', methods=["POST", "GET"])
def deleteAlert():
    # Initialise the Farm class and pass submitted form inputs across
    farm = Farm(request.args,  connect())
    # Complete signup
    farm.deleteAlert()

    # redirect back to alert page
    return redirect(url_for('alert'))


@app.route('/settings/delete_rule', methods=["POST", "GET"])
def deleteRule():
    # Initialise the Farm class and pass submitted form inputs across
    farm = Farm(request.args,  connect())
    # Complete signup
    farm.deleteRule()

    # redirect back to rules page
    return redirect(url_for('rule'))


@app.route('/createRule', methods=['POST'])
def createRule():
    if 'first_name' in session:
        # Initialise the Farm class and pass submitted form inputs across
        farm = Farm(request.form,  connect())
        # Complete signup
        farm.createRule()

        # redirect back to alert page
        return redirect(url_for('rule'))
    else:
        flash("You are not logged in")
        return redirect(url_for('login'))

@app.route('/config/devices')
def config_devices():
    if 'first_name' in session:

        page_title = "Config"
        page_desc = "Devices"

        # fetch all devices from db
        devices = Devices.query.all()

        return render_template("config/devices.html", **locals())
    else:
        flash("You are not logged in")
        return redirect(url_for('login'))

@app.route('/config/farms')
def config_farms():
    if 'first_name' in session:

        page_title = "Config"
        page_desc = "Farms"

        # fetch all farms from db
        farms = User.query.all()

        return render_template("config/farms.html", **locals())
    else:
        flash("You are not logged in")
        return redirect(url_for('login'))

@app.route('/config/new_device', methods=['POST'])
def config_device_post():
    if 'first_name' in session:
        model = request.form['model']
        serial = request.form['serial']
        acquired_on = datetime.strptime(request.form['acquired_on'], '%m/%d/%Y').strftime('%Y-%m-%d') 

        new_reading = Devices(model=model,serial=serial,acquired_on=acquired_on)

        # Add new record to db
        db.session.add(new_reading)
        db.session.commit()

        flash("Device added successfully")
        return redirect(url_for('config_devices'))
    else:
        flash("You are not logged in")
        return redirect(url_for('login'))

@app.route('/config/farm_device', methods=["POST", "GET"])
def farmDevices():
    if 'first_name' in session:
        user_id = request.args['id']

        devices = []
        device_count = UserDevices.query.filter_by(user_id=user_id).count()

        if device_count < 0:
            devices = Devices.query.all()

        return render_template("config/user_devices.html", **locals())
       
    else:
        flash("You are not logged in")
        return redirect(url_for('login'))


if __name__ == '__main__':
    app.config['SESSION_TYPE'] = 'filesystem'
    app.secret_key = os.urandom(24)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    # sess.init_app(app)
    app.run()
