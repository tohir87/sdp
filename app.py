import os
from flask import Flask, render_template, jsonify, request, redirect, url_for
from classes.farm import Farm

app = Flask(__name__, static_url_path=os.getcwd() + 'templates/vendor')
app.config.from_object(os.environ['APP_SETTINGS'])
print(os.environ['APP_SETTINGS'])


@app.route('/setup')
def home():
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

    return render_template("test.html", **locals())


@app.route('/doSetUp', methods=['POST'])
def doSetup():
    # get submitted form inputs
    farm = Farm(request.form)
    print("response")
    print(farm.signUp())
    # first_name = request.form['first_name']
    # last_name = request.form['last_name']
    # email = request.form['email']
    # phone = request.form['phone']
    # password = request.form['password']

    # complete setup process


if __name__ == '__main__':
    app.run()
