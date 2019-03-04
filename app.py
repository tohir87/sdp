import os
from flask import Flask, render_template, jsonify, request, redirect, url_for

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


if __name__ == '__main__':
    app.run()
