from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import os
from flask import Flask, render_template, jsonify, request, redirect, url_for
from classes.farm import Farm
import psycopg2

app = Flask(__name__, static_url_path=os.getcwd() + 'templates/vendor')
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
    # get submitted form inputs
    farm = Farm(request.form)
    print("response")
    print(farm.signUp())

    # complete setup process


@app.route('/settings')
def settings():

    page_title = "Settings"
    page_desc = "Available settings"

    return render_template("settings.html", **locals())


@app.route('/report')
def report():

    page_title = "Report"
    page_desc = "Temperature Report over time"

    return render_template("plot.html", **locals())


if __name__ == '__main__':
    app.run()
