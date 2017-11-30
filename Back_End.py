import pandas as pd
from datetime import date
from pandas import ExcelWriter
from  pandas import ExcelFile

def value_potential(key):
    utilization_percentage = float(user.avg_expense)/user.salary
    monthly_flow = float(user.salary) - user.avg_expense
    # months_to_goal = (user.target_value - user.financial_status) / monthly_flow
    months_to_goal = (user.target_date - date.today()).days/30.41

    # the score composed from 50% of the time that there is and 50% of the utilization of the
    # monthly flow per month
    if key == '0001':
        potential_long_term = (months_to_goal**2)/72
        utilization = ( utilization_percentage**2)*50
        if potential_long_term >50: potential_long_term =50
        if utilization >50: utilization = 50
        return utilization + potential_long_term

    elif key == '0002':
        potential_long_term = (months_to_goal ** 1.5) / 13
        if potential_long_term > 100: potential_long_term = 100
        return  potential_long_term

    elif key == '0003':
        return
    elif key == '0004':
        return
    else:
        for i in xrange(100) : print '[!] problem {} not defined'.format(key)
        return 0

def values_chooser(value):
    if type(value[5]) == float or type(value[6]) == float:
        return False
    elif str(value[0]) != 'nan' and user.life_status != value[0]:
        return False
    # elif str(value[1]) != 'nan' and user.age != value[1]:
    #     return False
    elif str(value[2]) != 'nan' and user.target_name != value[2]:  # need better diagnose
        return False
    # elif str(value[3]) != 'nan' user.motivation < value[]:
    #     return False
    # elif str(value[4]) != 'nan' user.intelligence  value[]: need a separate function
    #     return False
    else:
        return True


def invest_potential():
    return


def establishment_potential():
    value_score=[]
    data = pd.read_excel(r'C:\Users\OR\Desktop\In-Data-DB.xlsx').iloc[8:16, :]
    keys = list(data.columns.values)
    for i in xrange(2, len(keys), 1):
        if values_chooser(list(data.iloc[:, i])):
            value_score.append([keys[i],value_potential(keys[i])])
    return value_score


def debts_potential():
    return


def relevant_subjects():
    value_score = []
    if user.financial_status < 0 - user.salary / 2:
        value_score.extend(debts_potential())
    elif user.financial_status > user.salary * 6:
        value_score.extend(invest_potential())
    value_score.extend(establishment_potential())
    return value_score


######################################################################################


def user_dedication():
    return


def data_evaluation(user_profile):
    global user
    user = user_profile
    user_dedication()
    x = relevant_subjects()

    return
