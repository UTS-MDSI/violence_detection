# I believe this script need to be in a Flask on our side (not client) to be more secure.
import psycopg2
import bcrypt
import secrets
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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


def check_email(email):
    # Connecting to db
    conn = psycopg2.connect("host=localhost dbname=violence_detection user=admin password=admin")
    cur = conn.cursor()

    #Query and excecution
    query = """
            select c.mail
            from app.users as c
            where c.mail= '{}'
            """.format(email)
    cur.execute(query)
    rs = cur.fetchone()

    #Close connections
    cur.close()
    conn.close()

    if rs is None:
        return False
    else:
        return True

def encript(password):
    """
    It encripts the given password
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed

def reset_password(email):
    # Set new password
    password = secrets.token_urlsafe(13)
    encripted = encript(password)

    # Connecting to db
    conn = psycopg2.connect("host=localhost dbname=violence_detection user=admin password=admin")
    cur = conn.cursor()
    print(password)

    #Query and execution
    query = """
            UPDATE app.users
            SET pass = %s
            WHERE mail = %s
            """

    cur.execute(query, (encripted, email))
    conn.commit()

    #Close connections
    cur.close()
    conn.close()

    return password

def send_password(email, password):
    msg = MIMEMultipart()
    message = f"Your new password is: {password}"
    
    # setup the parameters of the message
    password = "7$&T*pAZd5v8g*"
    msg['From'] = "violence.detection.app@gmail.com"
    msg['Subject'] = "Password reset"

    # add in the message body
    msg.attach(MIMEText(message, 'plain'))

    #create server
    server = smtplib.SMTP('smtp.gmail.com: 587')

    server.starttls()

    # Login Credentials for sending the mail
    server.login(msg['From'], password)

    # send the message via the server.
    server.sendmail(msg['From'], [email], msg.as_string())

    server.quit()
    print('Succesfully email send')

def retrieve_password(email):
    # Check that email exists
    if not check_email(email):
        print("No match")
        return None

    # Reset password and save it as a new variable
    password = reset_password(email)

    # Send password
    send_password(email, password)