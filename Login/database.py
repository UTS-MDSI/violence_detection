import psycopg2
import bcrypt

# Connecting to db
conn = psycopg2.connect("host=localhost dbname=violence_detection user=admin password=admin")

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

def register_new(username, password):
    pass


def retrieve_password():
    pass