from flask import Flask, request, redirect, render_template, flash, make_response, url_for, session
from flask.ext.script import Manager, Shell
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.mail import Message, Mail
import os
from threading import Thread

basedir = os.path.abspath(os.path.dirname(__file__))


class NameForm(Form):
    name = StringField('what is your name?', validators=[Required()])
    submit = SubmitField('Submit')


app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite') + '?check_same_thread=False'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/first-flask'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['MAIL_SERVER'] = 'smtp.126.com'
app.config['MAIL_PORT'] = 25
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'aaa1058169464@126.com'
app.config['MAIL_PASSWORD'] = 'lizhenbin1209'
# app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = ['Flasky']
# app.config['FLASKY_MAIL_SENDER'] = 'Flasky Admin <aaa1058169464@126.com>'
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
manger = Manager(app)
migrate = Migrate(app, db)
mail = Mail(app)


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    msg = Message('Hello' + subject, sender='aaa1058169464@126.com',
                  recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    t1 = Thread(target=send_async_email,args=[app,msg])
    t1.start()
    return t1


manger.add_command('db', MigrateCommand)
manger.add_command('shell', Shell(make_context=make_shell_context))


@app.route('/', methods=['GET', 'POST'])
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
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        send_email('aaa1058169464@126.com', 'New User', 'mail/new_user'.format(), user=user)
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'), known=session.get('known', False))


@app.route('/user/<name>')
def user(name):
    # return 'hello %s' % name
    return render_template('user.html', name=name, a='<h2>防止转义</h2>')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    manger.run()
