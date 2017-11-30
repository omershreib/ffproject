from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_login import UserMixin
from flask import Flask


# from app import app
import datetime

#set time format
i = datetime.datetime.now()
mysql_date_format = ("%s-%s-%s" % (i.year, i.month, i.day) )

"""
config

"""

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Dor==mysqlDB@localhost/ff_db_test'
db = SQLAlchemy(app)

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)



"""
models

"""
class Test(db.Model):
    __tablename__ = 'test'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    testname = db.Column('testname', db.String(10))
    number = db.Column('number', db.Integer)

    def __init__(self, tname):
        self.testname = tname

    def __repr__(self):
        return "<Test(id = '%s', testname='%s')>" % (self.id, self.testname)


class User(UserMixin ,db.Model):
    __tablename__ = 'users'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement = True)
    username = db.Column('username', db.String(30), unique=True, nullable=False)
    password = db.Column('password', db.String(80), nullable=False)
    email = db.Column('email', db.String(50), unique=True, nullable=False)
    age = db.Column('age', db.Integer, unique=False, default=0)
    gender = db.Column('gender', db.Boolean, unique=False, default=True)
    test = db.Column('test', db.String(20))

    def __init__(self, username, password, email, age, gender):
        self.username = username
        self.password = password
        self.email = email
        self.age = age
        self.gender = gender

    def __repr__(self):
        return "<User(id = '%s', username='%s', password = '%s'," \
                "email = '%s', age = '%s')>" % (self.id, self.username, self.password,
                                    self.email, self.age)

class Profile(db.Model):
    __tablename__ = 'profiles'

    id = db.Column('id' ,db.Integer, primary_key=True, autoincrement = True)
    fullname = db.Column('fullname', db.String(30), unique=False, nullable=False)
    life_status = db.Column('life status', db.String(30), unique=False)
    financial_status = db.Column('fin status', db.Integer, unique=False, default=0)
    salary = db.Column('salary', db.Integer, unique=False, default=0)
    avg_expense = db.Column('avg expense', db.Integer, unique=False, default=0)
    target_name = db.Column('target name' ,db.String(50), unique=False, nullable=False, default='Unset')
    target_value = db.Column('target value', db.Integer, unique=False, default=0)
    target_date = db.Column('target date', db.Date, default = mysql_date_format)
    user_related = db.Column('user related', db.ForeignKey('users.id'), unique=True)

    def __init__(self, fullname, life_status, fin_status, salary, avg_exp, tname, tvalue, tdate):
        self.fullname = fullname
        self.life_status = life_status
        self.financial_status = fin_status
        self.salary = salary
        self.avg_expense = avg_exp
        self.target_name = tname
        self.target_value = tvalue
        self.target_date = tdate

    def __repr__(self):
        return "<Profile(id = '%s', fullname='%s', financial_status = '%s'," \
               "salary = '%s', avg_expense = '%s', user_related = '%s', life_status = '%s', target_name = '%s'," \
               "target_value = '%s', target_date = '%s')>" % \
               (self.id, self.fullname, self.financial_status,
                self.salary, self.avg_expense, self.user_related, self.life_status,
                self.target_name, self.target_value, self.target_date)

class AppLogin(db.Model):
    __tablename__ = 'applogin'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement = True)
    username = db.Column('username' ,db.String(30))
    # login_time = Column(DateTime(timezone=True),server_default=func.now(), onupdate=datetime.datetime.now())

    def __repr__(self):
        return "<AppLogin(id = '%s', username='%s', login_time = '%s')>" % \
               (self.id, self.username, self.login_time)



class StepPull(db.Model):
    __tablename__ = 'steps_pull'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement = True)
    name = db.Column('name', db.String(20))
    details = db.Column('details', db.String(80))
    reason = db.Column('reason', db.String(80))

    def __init__(self, name, details, reason):
        self.name = name
        self.details = details
        self.reason = reason

    def __repr__(self):
        return "<AppLogin(id = '%s', name='%s', details = '%s',reason = '%s')>" % \
               (self.id, self.name, self.details, self.reason)


class ConceptPull(db.Model):
    __tablename__ = 'concepts_pull'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement = True)
    name = db.Column('name', db.String(20))
    details = db.Column('details', db.String(80))

    def __init__(self, name, details):
        self.name = name
        self.details = details

    def __repr__(self):
        return "<AppLogin(id = '%s', name='%s', details = '%s')>" % \
               (self.id, self.name, self.details)


db.create_all()


# if __name__ == '__main__':
#     manager.run()