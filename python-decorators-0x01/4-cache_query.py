# import sqlite3
# import functools
# import time

# query_cache = {}

# def with_db_connection(func):

#     @functools.wraps(func)
#     def wrapper(*args, **kwargs):
#         result = None
#         try:
#             conn = sqlite3.connect('users.db')

#             # Passing rhe connection to the function

#             result = func(conn, *args, **kwargs)

#         except sqlite3.Error as e:
#             print(f'{e}')

#         finally:
#             if conn:
#                 conn.close()
#             return result
#     return wrapper

# def cache_query(func):

#     @functools.wraps(func)
#     def wrapper(conn, query, *args, **kwargs):

        
#         result = func(conn, *args, **kwargs)

#         #Check for thr presence of this query in cache_query
#         if query in cache_query.keys():
#             return f"the results of {query} are {cache_query[query]}"
#         else:
#             print(f"Executing query...")
#             cache_query[query] = result
#             return f"The results of {query} are {result}"
            
        
#     return wrapper

# @with_db_connection
# @cache_query
# def fetch_users_with_cache(conn, query):
#     cursor=conn.cursor()
#     cursor.execute(query)
#     return cursor.fetchall()

# #### First call will cache the result
# users = fetch_users_with_cache(query="SELECT * FROM users")

# #### Second call will use the cached result
# users_again = fetch_users_with_cache(query="SELECT * FROM users")


import sqlite3
import functools
import time

# Global cache dictionary
query_cache = {}

def with_db_connection(func):
    """
    Decorator to manage database connection.
    Opens connection, passes to function, ensures it's closed.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = None
        result = None
        try:
            conn = sqlite3.connect('users.db')
            result = func(conn, *args, **kwargs)
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            raise
        finally:
            if conn:
                conn.close()
        return result
    return wrapper

def cache_query(func):
    """
    Decorator to cache the results of database queries.
    Caches based on the SQL query string and its parameters.
    """
    @functools.wraps(func)
    def wrapper(conn, query, params=None, *args, **kwargs):
        # Create a unique cache key that includes both the query and its parameters
        cache_key = (query, tuple(params) if params else ())

        if cache_key in query_cache:
            print(f"Cache hit! Returning cached result for query: '{query[:70]}...'")
            return query_cache[cache_key]
        else:
            print(f"Cache miss. Executing query: '{query[:70]}...'")
            # Execute the original function, passing all relevant arguments
            # This line ensures 'query' and 'params' are passed to 'fetch_users_with_cache'
            result = func(conn, query, params, *args, **kwargs)
            
            query_cache[cache_key] = result
            return result
            
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query, params=None):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

#### First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

#### Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")

print(query_cache.items())