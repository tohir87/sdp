import os
from flask import Flask, render_template, jsonify, request, redirect, url_for

app = Flask(__name__, static_url_path=os.getcwd() + 'templates/vendor')
app.config.from_object(os.environ['APP_SETTINGS'])
print(os.environ['APP_SETTINGS'])


@app.route('/')
def home():
    return render_template("setup.html")


@app.route('/about')
def about():
    return jsonify({'name': "Thohiru Omoloye", 'student No.': "2950574"})


if __name__ == '__main__':
    app.run()
