USER, SUPERVISOR, ADMIN = range(3)


# Need to merge create_supervisor, and create_user

def create_user(db, user, account_type):
    """
    Fulfill requirement(s) 27, 28
    Creates a new user, and inserts it into the database.
    :param db: db object that should already be connected to the databse.
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


def edit_user(db, user):
    """Fulfill requirement(s) 29, 30"""
    pass


def assign_user(db, assignee, assigned):
    """Fulfill requirement(s) 31"""
    pass


def user_exists(db, email, account_type):
    """
    Checks whether a user is in the database, given an email.
    :param db: db object that should already be connected to the databse.
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
"""
INSERT INTO users
(userID, supervisorID, email, password, phone, fname, mname, lname, gender,
birthday, affiliation, ethnicity, active, isLoggedIn, dateCreated,
lastActive, picture)
VALUES
(6, NULL, "nyost448@live.kutztown.edu", "nope", 4843007777, "Nathan",
"Bruce", "Yost", "male", NULL, "Kutztown", "white", 1, 0, NULL, NULL,
NULL);
"""