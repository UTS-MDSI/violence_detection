# I believe this script need to be in a Flask on our side (not client) to be more secure.
import psycopg2
import bcrypt

# Connecting to db

def validate_credentials(username, password):

    # Connecting to db
    conn = psycopg2.connect("host=localhost dbname=violence_detection user=admin password=admin")
    cur = conn.cursor()

    #Query and excecution
    query = """
            select c.name, c.pass, c.status
            from app.users as c
            where c.name = '{}'
            """.format(username)
    cur.execute(query)
    rs = cur.fetchone()

    #Close connections
    cur.close()
    conn.close()

    # Result
    if rs == None:
        msg = 'The user does not exist'
        return msg, False
    elif not bcrypt.checkpw(password.encode(), rs[1].tobytes()):
        msg = 'User and password do not match'
        return msg, False
    elif rs[2] == 0:
        msg = 'The current user does not have access'
        return msg, False
    else:
        msg = 'Access granted'
        return msg, True

def register_new(username, email, password):
    # Connecting to db
    conn = psycopg2.connect("host=localhost dbname=violence_detection user=admin password=admin")
    cur = conn.cursor()

    # Check if user exists
    query = """
            select c.name
            from app.users as c
            where c.name = '{}'
            """.format(username)
    cur.execute(query)
    rs = cur.fetchone()

    if rs != None:
        msg = 'The user already exists'
        return msg, False

    # Check email
    query = """
            select c.mail
            from app.users as c
            where c.mail = '{}'
            """.format(email)
    cur.execute(query)
    rs = cur.fetchone()

    if rs != None:
        msg = 'The email already exists'
        return msg, False
    
    # Register
    user_pass = (username, encript(password), 0, email)
    query = """INSERT into app.users(name, pass, status, mail) values(%s,%s,'%s', %s)"""
    cur.execute(query, user_pass)
    conn.commit()

    msg = 'Register succesfully'
    return msg, True

    cur.close()
    conn.close()

def retrieve_password():
    pass

def encript(password):
    """
    It encripts the given password
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed