from flask import Flask, request, redirect, render_template, flash, make_response
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)
manger = Manager(app)


@app.route('/')
def index():
    # return 'Hello World!'
    # user_agent = request.headers.get('User-Agent')
    # return '<p>Your browser is %s</p>' % user_agent
    # return '<p>Bad Response</p>', 400
    # response = make_response('<h1>this is a cookie</h1>')
    # response.set_cookie('answer','42')
    # return response
    # return redirect('http://www.baidu.com')
    # return render_template('super.html')
    return render_template('index.html')


@app.route('/user/<name>')
def user(name):
    # return 'hello %s' % name
    return render_template('user.html', name=name, a='<h2>防止转义</h2>')


if __name__ == '__main__':
    manger.run()
