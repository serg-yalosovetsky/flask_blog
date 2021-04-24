import sqlite3
import hashlib

connection = sqlite3.connect('database.db')
INSERT_USERS = "INSERT INTO users (name, password, email) VALUES (?, ?, ?)"
INSERT_POSTS = "INSERT INTO posts (title, content, user_id) VALUES (?, ?, ?)"

with open('schema.sql') as f:
    connection.executescript(f.read())
    
cur = connection.cursor()

def hash_(s):
    return hashlib.sha256(s.encode('utf-8')).hexdigest()

cur.execute(INSERT_USERS, ('Ivan', hash_('passwordIvan'), 'Ivan@gmail.com'))
cur.execute(INSERT_USERS, ('qwe', hash_('qwe'), 'qwe'))

cur.execute(INSERT_USERS, ('Petya', hash_('passwordPetya'), 'Petya@gmail.com'))

cur.execute(INSERT_USERS, ('Sasha', hash_('passwordSasha'), 'Sasha@gmail.com'))

cur.execute(INSERT_POSTS, ('First Post', 'Content for the first post', 3))

cur.execute(INSERT_POSTS, ('Second Post', 'Content for the second post', 2))

connection.commit()
connection.close()

