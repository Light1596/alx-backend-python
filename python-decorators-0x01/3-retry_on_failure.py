import sqlite3
import functools
import time

def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):

        try:
            
            conn = sqlite3.connect('users.db')
            func(conn, *args, **kwargs)

        except sqlite3.Error as e:
            print(f"{e}")
        finally:
            if conn:
                conn.close()
    return wrapper


def retry_on_failure(retries=3, delay=1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper( *args, **kwargs):
            attempts = 0
            while attempts < retries:
                try:

                    return func(*args, **kwargs)

                except sqlite3.Error as e:
                    print(f"{e}/n Retrying ...")
                    if attempts < retries: 
                            time.sleep(1)
                            attempts += 1
            print(f"All {retries} have been exhausted for {func.__name__}.")
            
            
        return wrapper
    return decorator
 
@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()


#### attempt to fetch users with automatic retry on failure
users = fetch_users_with_retry()
print(users)