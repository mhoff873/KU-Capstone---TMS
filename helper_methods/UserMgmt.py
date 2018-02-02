def create_supervisor(db, supervisor):
    """
    Fulfill requirement(s) 27
    :param db: db object that should already be connected to the databse.
    :param user: List that defines each column for the new supervisor.
    :return: void
    """
    supervisor[0] = __get_supervisorid(db)
    pass


def create_user(db, user):
    """
    Fulfill requirement(s) 28
    Creates a new user, and inserts it into the database table users.
    :param db: db object that should already be connected to the databse.
    :param user: List that defines each column for the new user.
    :return: void
    """
    query = """INSERT INTO users
    (userID, supervisorID, email, password,
    phone, fname, mname, lname,
    gender, birthday, affiliation, ethnicity,
    active, isLoggedIn, dateCreated, lastActive, picture)
    VALUES
    (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor = db.cursor()
    cursor.execute(query % tuple(user))
    db.commit()


def edit_user(db, user):
    """Fulfill requirement(s) 29, 30"""
    pass


def assign_user(db, assignee, assigned):
    """Fulfill requirement(s) 31"""
    pass


def user_exists(db, email):
    """
    Checks whether a user is in the user database, given an email.
    :param db: db object that should already be connected to the databse.
    :param email: Email that coincides with the user that is being searched.
    :return: boolean on whether the user exists in the users table.
    """
    query = "SELECT * FROM users WHERE email=%s"
    cursor = db.cursor()
    cursor.execute(query % email)
    if cursor.fetchone():
        return True
    else:
        return False


def __get_supervisorid(db):
    """
    Gets the next available supervisor id.
    :param db: db object that should already be connected to the databse.
    :return: integer of the next available supervisor id
    """
    query = "SELECT MAX(supervisorID) FROM supervisors;"
    cursor = db.cursor()
    cursor.execute(query)
    max_id = -1
    try:
        # fetchone should return the single result as a tuple of 1 element..?
        max_id = int(cursor.fetchone()[0]) + 1
    except Exception:
        print("Error: cannot convert result to integer!")
    return max_id
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