import functools
import sqlite3
from datetime import datetime

# DATABASE SETUP

def create_database(db_name='users.db'):
    """
    Creates an SQLite3 database and the required tables if they do not exist.
    """
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        # Create the users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
               email TEXT UNIQUE NOT NULL
            )
         ''')

         # Create the logs table
        cursor.execute('''
              CREATE TABLE IF NOT EXISTS logs (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  timestamp TEXT NOT NULL,
                  function_name TEXT NOT NULL,
                  query_type TEXT,
                  message TEXT
              )
         ''')

        conn.commit()
        print(f"Database '{db_name}' and tables 'users' and 'logs' created.")
    except sqlite3.Error as e:
         print(f"Database error: {e}")
    finally:
         if conn:
             conn.close()


# def log_database_query(func):
#      @functools.wraps(func)
#      def wrapper(*args, **kwargs):
#          function_name = func.__name__
#          timestamp = datetime.now().isoformat()
#          query_type = "READ"  # You might make this dynamic later

#          try:
#              conn = sqlite3.connect("users.db")
#              cursor = conn.cursor()

#              result = func(*args, **kwargs)

#              message = f"Function '{function_name}' executed successfully."

#              cursor.execute(
#                  "INSERT INTO users (name, email) VALUES (?,?)",
#                  ('Light', 'lightsituma@gmail.com')
#              )
#              cursor.execute(
#                  "INSERT INTO logs (timestamp,function_name, query_type, message) VALUES (?, ?, ?, ?)",
#                  (timestamp,function_name, query_type, message)
#              )

#              conn.commit()
#              return result
#          except sqlite3.Error as e:
#              error_message = f"Function '{function_name}' encountered a database error: {e}"
#              print(error_message)
#          finally:
#              if conn:
#                  conn.close()
#      return wrapper

#@log_database_query
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# Create the database and tables
#create_database()

# Fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")
logout = fetch_all_users(query="SELECT * from logs")
print(users, logout)
