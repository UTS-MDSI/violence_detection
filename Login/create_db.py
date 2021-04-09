# Improvements
# Avoid SQL Injection
# Put it in a Flask?

import psycopg2
import bcrypt

# Connecting to db
conn = psycopg2.connect("host=localhost dbname=violence_detection user=admin password=admin")

# Creating cursor to create schema and user table
cur = conn.cursor()
cur.execute("CREATE SCHEMA IF NOT EXISTS app")
cur.execute("""CREATE TABLE IF NOT EXISTS 
            app.users (name varchar PRIMARY KEY, pass bytea, status int, mail varchar);
            """)

# Creating some user - passwords
user_pass = [('javiera', 'delacarreragarcia', 1, 'anamaria.jaimerivera@student.uts.edu.au'),
            ('ana', 'jaimerivera', 1, 'javiera.delacarreragarcia@student.uts.edu.au'),
            ('felipe', 'monroymorales', 0, 'felipe.m02@gmail.com')]

def encript(password):
    """
    It encripts the given password
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed

# Creating some users
user_pass = [(cred[0], encript(cred[1]), cred[2], cred[3]) for cred in user_pass]
query = """INSERT into app.users(name, pass, status, mail) values(%s,%s,'%s', %s)"""
cur.executemany(query, user_pass)

# Commiting
conn.commit()

cur.close()
conn.close()

#print(bcrypt.hashpw("18721872".encode(), hashed) ==  hashed)
