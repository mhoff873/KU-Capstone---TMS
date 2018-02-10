# Author:           Nathaniel Yost
# Creation Date:    January 31, 2018
# Professor:        Dr. Tan
# Class:            CSC 355
# Purpose:          Functions to deal with managing a user (Supervisor, or
#                   User).
USER, SUPERVISOR, ADMIN = range(3)


def create_user(db, user, account_type):
    """
    Fulfill requirement(s) 27, 28
    Creates a new user, and inserts it into the database.
    :param db: db object that should already be connected to the database.
    :param user: List that defines each column for the new user.
    :param account_type: Type of account that your dealing with.
    :return: void
    """
    query = None
    if account_type == USER:
        query = """INSERT INTO users
        (supervisorID, email, password, phone,
        fname, mname, lname, gender,
        birthday, affiliation, ethnicity, active,
        isLoggedIn, dateCreated, lastActive, picture)
        VALUES
        (%s, '%s', '%s', %s, '%s', '%s', '%s', '%s', '%s', '%s', '%s', %s,
        %s,'%s', '%s', '%s')
        """
    elif account_type == SUPERVISOR:
        query = """INSERT INTO supervisors
        (email, password, fname, mname,
         lname, isLoggedIn, dateCreated, gender,
         active, birthday, ethnicity, picture, affiliation, phone)
        VALUES
        ('%s', '%s', '%s', '%s', '%s', %s, '%s', '%s', %s, '%s', '%s', '%s',
        '%s', %s)
        """
    else:
        print("Invalid account_type = %d" % account_type)
        return False

    cursor = db.cursor()
    cursor.execute(query % tuple(user))
    db.commit()
    return True


def edit_user(db, email, user, account_type):
    """
    Fulfill requirement(s) 29, 30
    Edits a user's info., given their email address.
    :param db: db object that should already be connected to the database.
    :param email: email address of the user that will be editted.
    :param user: List that defines each column for the new user.
    :param account_type: Type of account that your dealing with.
    :return: void
    """
    query = None
    if account_type == USER:
        query = """UPDATE users
        SET supervisorID=%s, email='%s', password='%s', phone=%s,
        fname='%s', mname='%s', lname='%s', gender='%s',
        birthday='%s', affiliation='%s', ethnicity='%s', active=%s,
        isLoggedIn=%s, dateCreated='%s', lastActive='%s', picture='%s'
        WHERE email='%s'
        """
    elif account_type == SUPERVISOR:
        query = """UPDATE supervisors
        SET email='%s', password='%s', fname='%s', mname='%s',
        lname='%s', isLoggedIn=%s, dateCreated='%s', gender='%s',
        active=%s, birthday='%s', ethnicity='%s', picture='%s',
        affiliation='%s', phone=%s
        WHERE email='%s'
        """
    else:
        print("Invalid account_type = %d" % account_type)
        return False
    user.append(email)
    cursor = db.cursor()
    cursor.execute(query % (tuple(user[1:])))
    db.commit()
    return True


def assign_user(db, assignee, assigned):
    """
    Fulfill requirement(s) 31
    Assigns the supervisor id to the assignee, given emails of user, and
    supervisor.
    :param db: db object that should already be connected to the database.
    :param assignee: Email of user to be assigned a supervisor.
    :param assigned: Email of the supervisor.
    """
    user = get_user(db, assignee, USER)
    supervisor = get_user(db, assigned, SUPERVISOR)
    if user is False or supervisor is False:
        return False
    user[1] = supervisor[0]
    edit_user(db, assignee, user, USER)
    return True


def user_exists(db, email, account_type):
    """
    Checks whether a user is in the database, given an email.
    :param db: db object that should already be connected to the database.
    :param email: Email that coincides with the user that is being searched.
    :return: boolean on whether the user exists in the database.
    """
    table = None
    if account_type == USER:
        table = "users"
    elif account_type == SUPERVISOR:
        table = "supervisors"
    else:
        print("Invalid account_type = %d" % account_type)
        return False

    query = "SELECT * FROM %s WHERE email='%s'"
    cursor = db.cursor()
    cursor.execute(query % (table, email))
    if cursor.fetchone():
        return True
    else:
        return False


def get_user(db, email, account_type):
    """
    Gets a user from the database, given an account type (ie: USER,
    SUPERVISOR).
    :param db: db object that should already be connected to the database.
    :param email: email address of the user that will be editted.
    :param account_type: Type of account that your dealing with.
    :return: List of columns pertaining to the user with the given email.
    """
    table = None
    if account_type == USER:
        table = "users"
    elif account_type == SUPERVISOR:
        table = "supervisors"
    else:
        print("Invalid account_type = %d" % account_type)
        return False
    query = "SELECT * FROM %s WHERE email='%s'"
    cursor = db.cursor()
    cursor.execute(query % (table, email))
    user = cursor.fetchone()
    if user:
        user = list(user)
        # Change None to NULL for database
        for i in range(len(user)):
            if user[i] is None:
                user[i] = "NULL"
        return user
    else:
        return False


def get_assigned_users(db, email):
    """
    Gets all assigned users under a supervisor.
    :param db: db object that should already be connected to the database.
    :param email: email address of the supervisor to search users for.
    :return: List of users (List[User1, User2, ...]), User# is a list of
            columns.
    """
    supervisor = get_user(db, email, SUPERVISOR)
    query = "SELECT *  FROM users WHERE supervisorID=%s"
    cursor = db.cursor()
    cursor.execute(query % (supervisor[0]))
    return cursor.fetchall()
