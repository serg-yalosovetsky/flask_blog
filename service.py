import sqlite3
from init_db import hash_, INSERT_POSTS, INSERT_USERS

UPDATE_POST = 'UPDATE posts SET title=?, content=? WHERE id==?'


            
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def create_user(name, passw, email):
    conn = get_db_connection()
    conn.execute(INSERT_USERS, (name, hash_(passw), email) )
    conn.commit()
    conn.close()
    
   
def get_user(email):
    conn = get_db_connection()
    result = conn.execute(f'SELECT * FROM users where email = ? order by id desc',
                        (email,)).fetchone()
    conn.close()
    return result    
    
def check_pass(email, passw):
    conn = get_db_connection()
    result = conn.execute(f'SELECT * FROM users where email = ? and password = ?',
                        (email, hash_(passw))).fetchone()
    conn.close()
    return result
    
    
def update_posts(title, content, id):
    conn = get_db_connection()
    conn.execute(UPDATE_POST, (title, content, id) )
    conn.commit()
    conn.close()
    
def delete_post(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?',
                    (id,)  )
    conn.commit()
    conn.close()
    
def create_post(title, content, user_id):
    conn = get_db_connection()
    conn.execute(INSERT_POSTS, (title, content, user_id) )
    conn.commit()
    conn.close()
    

    
def select_all(table):
    conn = get_db_connection()
    result = conn.execute(f'SELECT * FROM {table}').fetchall()
    conn.close()
    return result
    
def select_one(table, id):
    conn = get_db_connection()
    result = conn.execute(f'SELECT * FROM {table} where id = ?',
                        (id,)).fetchone()
    conn.close()
    return result
    
