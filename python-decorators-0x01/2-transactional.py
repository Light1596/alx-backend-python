import sqlite3
import functools


"""
Writing a decorator transactional(func) that ensures a function running a database operation
is wrapped inside a transaction. If the function raises an error, rollback; otherwise commit
the transaction

"""
def with_db_connection(func):

    @functools.wraps(func)
    def wrapper(* args, **kwargs):
        conn = None
        try:
            conn = sqlite3.connect('users.db')


            func(conn,*args, **kwargs)

            

        except sqlite3.Error as e:
            print(f"The error '{e}' was encountered")
            raise
        finally:
            if conn:
                conn.close()
                     
    return wrapper

def transactional(func):

    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):

        try:
            
            func(conn, *args, **kwargs)

            conn.commit()
            print("Change successful")
            
        except sqlite3.Error as e:
            print(f"error '{e}' was encountered")
            if conn:
                conn.rollback()
                
            raise
        
    return wrapper
                
            
@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))

@with_db_connection
def get_user_by_id(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()


# Update user's email with automatic transaction handling
update_user_email(user_id=1,new_email='Crawford_Cartwright@hotmail.com')

user = get_user_by_id(user_id=1)
print(user)