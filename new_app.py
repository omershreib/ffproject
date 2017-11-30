from datetime import date

import math

import Back_End
from pygal.style import SaturateStyle
from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash, escape, send_from_directory, send_file
from sqlalchemy.exc import InvalidRequestError

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_required, login_user, logout_user, current_user

import pygal,sys
#from model import *
from new_model import *

import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

LIFE_STARTUS_PULL = {

    '1': 'Solider',
    '2': 'Student',
    '3': 'Released Solider'
}

GENDER_PULL = {
    'Male': True,
    'Female': False
}

TARGET_PULL = {
    '1': 'Debts Deletion',
    '2': 'Trip',
    '3': 'Student Living wage',
    '4': 'regular economy'
}


STEPS_PULL = {
    'Solider' : {
        'Mashakit Tash' : 'A',
        'Solider Loan' : 'B',
        'Work Vacation' : 'C',
        'Overall' : 'D'
    },
    'Fortune Creation' : {},
    'Released Solider' : {}
}

CONCEPTS_PULL = {
    'Solider' : {
        'Army Gratitude' : 'A',
        'Pikadon' : 'B',
        'Clean Value' : 'C',
        'Passive Income' : 'D'
    },
    'Fortune Creation' : {
        'Passive Investment': 'E',
        'Ribit Deribit': 'F',
        'Opening Investment Bag': 'G',
        'Choosing Investment': 'H'
    },


}

SOURCE_URL = {
    'Army Gratitude' : 'https://www.hachvana.mod.gov.il/maanak/Pages/infomaanakvepikadon.aspx',
    'Clean Value' : 'http://www.maot.co.il/lex6/glossary/g_3807.asp',
    'Army Deposit' : 'https://pikadon.co.il/index',
    'Passive Income' : 'http://www.hasolidit.com/%D7%9E%D7%99-%D7%A8%D7%95%D7%A6%D7%94-%D7%9C%D7%94%D7%99%D7%95%D7%AA-%D7%9E%D7%99%D7%9C%D7%99%D7%95%D7%A0%D7%A8'



}

# app
app.config['SECRET_KEY'] = 'thisissecret'
login_manager = LoginManager()
login_manager.init_app(app)

# database connection & querying setting
# s = db_session()
s = db.session()



def graph_time_labes():
    time_lable = []
    date_now = datetime.datetime.now().month, datetime.datetime.now().year
    for i in xrange(-4, 0, 1):
        month = date_now[0] + i
        year = date_now[1]
        if month < 1:
            month = month + 12
            year = date_now[1] - 1
        time_lable.append(date(year, month, 1))
    time_lable.append(date(date_now[1], date_now[0], 1))
    for i in xrange(1, 8, 1):
        month = date_now[0] + i
        year = date_now[1]
        if month > 12:
            month = month - 12
            year = date_now[1] + 1
        time_lable.append(date(year, month, 1))
    return time_lable


def graph_data(user_profile):
    starting_point = user_profile.financial_status
    graph_data_point = {'financial status': [], 'expense': []}
    monthly_flow = (user_profile.salary - user_profile.avg_expense)
    labels='salary: {}\nexpense: {}'.format(user_profile.salary, user_profile.avg_expense)
    for i in xrange(4, 0, -1):
        if user_profile.target_name == 'Debts Deletion':
            data_point = starting_point + i * math.fabs(monthly_flow)
            graph_data_point['financial status'].append({'value': data_point, 'label': '{}'.format(labels)})
            graph_data_point['expense'].append(user_profile.avg_expense)
        else:
            data_point = starting_point - i * monthly_flow
            graph_data_point['financial status'].append({'value': data_point, 'label': '{}'.format(labels)})
            graph_data_point['expense'].append(user_profile.avg_expense)
    graph_data_point['financial status'].append({'value': starting_point, 'label': '{}'.format(labels)})
    graph_data_point['expense'].append(user_profile.avg_expense)
    last_point = starting_point
    for i in xrange(8):
        hypothesis = int(round(user_profile.avg_expense - user_profile.salary * (0.02 * i)))
        labels = 'salary: {} expense: {}'.format(user_profile.salary, hypothesis)
        data_point = last_point + (monthly_flow + round(user_profile.salary * (0.02 * i)))
        graph_data_point['financial status'].append({'value': data_point, 'label': '{}'.format(labels)})
        graph_data_point['expense'].append(hypothesis)
        last_point = graph_data_point['financial status'][-1]['value']
    return graph_data_point


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



@app.route('/')
def index():
    return render_template('index.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # user = s.query(User).filter_by(username=request.form['usr']).first()
        user = s.query(User).filter_by(username=request.form['usr']).first()
        if user:
            if check_password_hash(user.password, request.form['pwd']):
                # user_login = AppLogin(username=user.username)
                # s.add(user_login)
                # s.commit()
                login_user(user)

                return redirect(url_for('home'))


    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    # username = request.args['user_login']
    # # login_engine.logout(username)
    # user_logout = s.query(AppLogin).filter_by(username=username).first()
    # s.delete(user_logout)
    # s.commit()
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['usr']
        password = request.form['pwd']
        confirm_password = request.form['con_pwd']
        email = request.form['email']
        age = request.form['age']
        gender = request.form['gender']

        if password == confirm_password:
            hashed_password = generate_password_hash(password, method='sha256')
            new_user = User(
                username=username,
                password=hashed_password,
                email=email,
                age=age,
                gender=gender
            )

            new_profile = Profile(
                fullname=None,
                life_status=None,
                fin_status=None,
                salary=None,
                avg_exp=None,
                tname=None,
                tvalue=None,
                tdate=None
            )
            new_profile.fullname = 'Unset'

            s.add(new_user)

            try:
                s.commit()

            except InvalidRequestError:
                s.rollback()

            uid = s.query(User.id).filter_by(username=username).first()
            new_profile.user_related = uid[0]
            s.add(new_profile)
            s.commit()

            flash("New User was successfully created!")

            return redirect(url_for('index'))

    return render_template('register.html', gender_list=GENDER_PULL)


@app.route('/home')
@login_required
def home():
    saturate_style = SaturateStyle('#609f86')
    x = s.query(AppLogin.username).all()
    # username = request.args['user_login']
    uid = s.query(User.id).filter_by(username=current_user.username).first()
    fullname = s.query(Profile.fullname).filter_by(user_related=uid[0]).first()

    if fullname[0] == 'Unset':
        return redirect(url_for('basic_profile', user_login=current_user.username))

    user_profile = s.query(Profile).filter_by(user_related=uid[0]).first()
    line_chart = pygal.Line(interpolate='hermite', interpolation_parameters={'type': 'finite_difference'},dots_size=4)
    # line_chart = pygal.Line()
    line_chart.title = 'Target: {}'.format(user_profile.target_name)
    # line_chart.x_labels = map(str, range(1, 12))
    line_chart.x_labels = graph_time_labes()
    line_chart.add('financial status', graph_data(user_profile)['financial status'], style=saturate_style)
    line_chart.add('expense', graph_data(user_profile)['expense'])
    # line_chart.x_value_formatter = lambda x: '%s%%' % x
    line_chart.render()
    chart = line_chart.render_data_uri()
    Back_End.data_evaluation(user_profile)
    return render_template('home.html', username=current_user.username, x=x, chart=chart)


@app.route('/basic_profile', methods=['GET', 'POST'])
@login_required
def basic_profile():
    username = request.args['user_login']

    if request.method == 'POST':
        try:
            uid = s.query(User.id).filter_by(username=username).first()
            user_profile = s.query(Profile).filter_by(user_related=uid[0]).first()

            user_profile.fullname = request.form['fullname']
            user_profile.life_status = request.form['life_status']
            user_profile.financial_status = request.form['financial_status']
            user_profile.salary = request.form['salary']
            user_profile.avg_expense = request.form['avg_expense']
            user_profile.target_name = request.form['target_name']
            user_profile.target_value = request.form['target_value']
            user_profile.target_date = request.form['target_date']


            s.add(user_profile)
            s.commit()
            flash("User Profile has been modified")

            return redirect(url_for('home', user_login=username))
        except InvalidRequestError:
            s.rollback()
            return "Error! The Transaction was rolled back"




    return render_template('basic_profile.html', username=username, target_list=TARGET_PULL, life_status=LIFE_STARTUS_PULL)


@app.route('/update_profile', methods=['GET', 'POST'])
@login_required
def update_profile():
    username = request.args['user_login']
    uid = s.query(User.id).filter_by(username=username).first()
    user_profile = s.query(Profile).filter_by(user_related=uid[0]).first()

    if request.method == 'POST':

        user_profile.life_status = request.form['life_status']
        user_profile.salary = request.form['salary']
        user_profile.target_name = request.form['target_name']
        user_profile.target_value = request.form['target_value']
        user_profile.target_date = request.form['target_date']

        s.add(user_profile)
        s.commit()
        flash("User Profile has been modified")

        return redirect(url_for('home', user_login=username))

    return render_template('update_profile.html',profile=user_profile, username=username, target_list=TARGET_PULL, life_status=LIFE_STARTUS_PULL)


@app.route('/next_step', methods=['GET', 'POST'])
@login_required
def next_step():
    username = request.args['user_login']
    uid = s.query(User.id).filter_by(username=username).first()
    user_profile = s.query(Profile).filter_by(user_related=uid[0]).first()
    profile_steps = {}


    if user_profile.life_status == 'Solider':
        profile_steps['Solider Loan'] = s.query(StepPull).filter_by(name='Solider Loan').first()
        profile_steps['Mashakit Tash'] = s.query(StepPull).filter_by(name='Mashakit Tash').first()
        profile_steps['Work Vacation'] = s.query(StepPull).filter_by(name='Work Vacation').first()
        profile_steps['Overall'] = s.query(StepPull).filter_by(name='Overall').first()

    return  render_template('next_step.html', profile=user_profile, username=username, steps = profile_steps)


@app.route('/learning', methods=['GET', 'POST'])
@login_required
def learning():
    username = request.args['user_login']
    uid = s.query(User.id).filter_by(username=username).first()
    user_profile = s.query(Profile).filter_by(user_related=uid[0]).first()
    profile_concepts = {}

    if user_profile.life_status == 'Solider':
        profile_concepts['Army Gratitude'] = s.query(ConceptPull).filter_by(name='Army Gratitude').first()
        profile_concepts['Army Deposit'] = s.query(ConceptPull).filter_by(name='Army Deposit').first()
        profile_concepts['Clean Value'] = s.query(ConceptPull).filter_by(name='Clean Value').first()
        profile_concepts['Passive Income'] = s.query(ConceptPull).filter_by(name='Passive Income').first()

    return render_template('learning.html', profile=user_profile, username=username, concepts=profile_concepts, url = SOURCE_URL)


@app.route('/add_step', methods=['GET', 'POST'])
@login_required
def add_step():
    if request.method == 'POST':

        new_step = StepPull(
            name = request.form['name'],
            details = request.form['details'],
            reason = request.form['reason']
        )

        s.add(new_step)
        try:
            s.commit()
            return redirect(url_for('show'))

        except InvalidRequestError:
            s.rollback()
            return "Error! The Transaction was rolled back"

    return render_template('add_step.html')

@app.route('/add_concept', methods=['GET', 'POST'])
@login_required
def add_concept():
    if request.method == 'POST':

        new_concept = ConceptPull(
            name = request.form['name'],
            details = request.form['details'],

        )

        s.add(new_concept)
        try:
            s.commit()
            return redirect(url_for('show'))

        except InvalidRequestError:
            s.rollback()
            return "Error! The Transaction was rolled back"

    return render_template('new_concep.html')

@app.route('/show')
@login_required
def show():
    all_steps = s.query(StepPull).all()
    all_concepts = s.query(ConceptPull).all()

    return render_template('show.html', steps = all_steps, concepts = all_concepts)




# @app.route('/source_reading')
# def source_reading(name):
#     return



@app.context_processor
def override_url_for():
    """

    update staticfiles
    """
    return dict(url_for=dated_url_for)


def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

# if __name__ == '__main__':
#     manager.run()

if __name__ == '__main__':
    #manager.run()
    # app.run(host='0.0.0.0',port=80, debug=True)
    app.run(debug=True)
