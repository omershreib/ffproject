
from sqlalchemy import Sequence
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import  declarative_base
from sqlalchemy import  Column, Integer, String, ForeignKey, Date, Boolean
from sqlalchemy.orm import sessionmaker, Session, relationship
from sqlalchemy.sql import func
from sqlalchemy.exc import InvalidRequestError
import datetime

from flask_migrate import Migrate, MigrateCommand

i = datetime.datetime.now()

mysql_date_format = ("%s-%s-%s" % (i.year, i.month, i.day) )



Base = declarative_base()
engine = create_engine('mysql+mysqlconnector://root:Dor==mysqlDB@localhost:3306/ffproject_db',
                           encoding='latin1', echo=True)



class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    username = Column(String(30), unique=True, nullable=False)
    password = Column(String(80), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    age = Column(Integer, unique=False, default=0)
    gender = Column(Boolean, unique=False, default=True)

    def __repr__(self):
        return "<User(id = '%s', username='%s', password = '%s'," \
                "email = '%s', age = '%s')>" % (self.id, self.username, self.password,
                                    self.email, self.age)

class Profile(Base):
    __tablename__ = 'profiles'

    id = Column(Integer, Sequence('profile_id_seq'), primary_key=True)
    fullname = Column(String(30), unique=False, nullable=False)
    life_status = Column(String(30), unique=False)
    financial_status = Column(Integer, unique=False, default=0)
    salary = Column(Integer, unique=False, default=0)
    avg_expense = Column(Integer, unique=False, default=0)
    target_name = Column(String(50), unique=False, nullable=False, default='Unset')
    target_value = Column(Integer, unique=False, default=0)
    target_date = Column(Date, default = mysql_date_format)
    user_related = Column(ForeignKey('users.id'), unique=True)

    def __repr__(self):
        return "<Profile(id = '%s', fullname='%s', financial_status = '%s'," \
               "salary = '%s', avg_expense = '%s', user_related = '%s', life_status = '%s', target_name = '%s'," \
               "target_value = '%s', target_date = '%s')>" % \
               (self.id, self.fullname, self.financial_status,
                self.salary, self.avg_expense, self.user_related, self.life_status,
                self.target_name, self.target_value, self.target_date)

class AppLogin(Base):
    __tablename__ = 'applogin'

    id = Column(Integer, primary_key=True)
    username = Column(String(30))
    # login_time = Column(DateTime(timezone=True),server_default=func.now(), onupdate=datetime.datetime.now())

    def __repr__(self):
        return "<AppLogin(id = '%s', username='%s', login_time = '%s')>" % \
               (self.id, self.username, self.login_time)



class StepPull(Base):
    __tablename__ = 'steps_pull'

    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    details = Column(String(80))
    reason = Column(String(80))

    def __repr__(self):
        return "<AppLogin(id = '%s', name='%s', details = '%s',reason = '%s')>" % \
               (self.id, self.name, self.details, self.reason)


class ConceptPull(Base):
    __tablename__ = 'concepts_pull'

    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    details = Column(String(80))

    def __repr__(self):
        return "<AppLogin(id = '%s', name='%s', details = '%s')>" % \
               (self.id, self.name, self.details)




db_session = sessionmaker()
db_session.configure(bind=engine)
Base.metadata.create_all(engine)


