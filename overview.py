




# The Function
# - gets the data about the user
# - decide which path he need to start to accomplish his goal
# - return &&&

def set_starting_point(user_profile):
    # if user_profile.target_name == 'Debts Deletion':
    #     pass
    # elif user_profile.target_name == 'Safety Fund':
    #     pass
    # elif user_profile.target_name == 'wealth':
    #     pass
    global User
    User = user_profile

    if User.financial_status < 0 - User.salary/2:
        pass
    elif User.financial_status < User.salary * 6:
        pass
    else:
        pass