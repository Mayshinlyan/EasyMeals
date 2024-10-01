import psycopg2
import psycopg2.extras
import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))


def get_db_string():

    database_string = "postgresql://{user}:{pw}@{host}:{port}/{dbname}"
    db_name = os.getenv("db_database")
    db_user = os.getenv("db_username")
    db_pw = os.getenv("db_pwd")
    db_host = os.getenv("db_hostname")
    db_port = os.getenv("db_port_id")

    return database_string.format(
        user=db_user, pw=db_pw, host=db_host, port=db_port, dbname=db_name
    )


def connect_db():
    db_string = get_db_string()
    try:
        conn = psycopg2.connect(db_string)
        print("Connection Successful")
    except psycopg2.OperationalError as err:
        err_msg = "DB Connection Error - Error: {}".format(err)
        print(err_msg)
        return False
    return conn


def create_table(sql_raw, params):
    """Create table"""
    return _execute_query(sql_raw, params, "create")


def insert(sql_raw, params):
    """Runs Insert query, returns result.
    Returned result is typically the newly created PRIMARY KEY value from the database.
    """
    return _execute_query(sql_raw, params, "insert")


def select_one(sql_raw, params):
    """Runs SELECT query that will return zero or 1 rows.  `params` is required."""
    return _execute_query(sql_raw, params, "sel_single")


def update(sql_raw, params):
    """Runs UPDATE query, returns result depending on update query executed."""
    return _execute_query(sql_raw, params, "update")


def select_multi(sql_raw, params=None):
    """Runs SELECT query that will return multiple.  `params` is optional."""
    return _execute_query(sql_raw, params, "sel_multi")


def _execute_query(sql_raw, params, qry_type):
    """Handles executing all types of queries based on the `qry_type` passed in.
    Returns False if there are errors during connection or execution.
        if results == False:
            print('Database error')
        else:
            print(results)
    You cannot use `if not results:` b/c 0 results is a false negative.
    """
    try:
        conn = connect_db()

    except psycopg2.ProgrammingError as err:
        print("Connection not configured properly.  Err: %s", err)
        return False

    if not conn:
        return False

    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    try:
        if qry_type == "create":
            cur.execute("DROP TABLE IF EXISTS patients")
            cur.execute(sql_raw)
        else:

            cur.execute(sql_raw, params)

        if qry_type == "sel_single":
            results = cur.fetchone()
        elif qry_type == "sel_multi":
            results = cur.fetchall()
        elif qry_type == "insert":
            results = None
            # results = cur.fetchone()
            conn.commit()
        elif qry_type == "update":
            # results = cur.fetchone()
            results = None
            conn.commit()
        elif qry_type == "create":
            # results = cur.fetchone()
            results = None
            conn.commit()
        else:
            raise Exception("Invalid query type defined.")

    except psycopg2.ProgrammingError as err:
        print("Database error via psycopg2.  %s", err)
        results = False
    except psycopg2.IntegrityError as err:
        print("PostgreSQL integrity error via psycopg2.  %s", err)
        results = False
    finally:
        conn.close()

    return results


def create_user_table():
    create_user_table_script = """ CREATE TABLE IF NOT EXISTS patients (
                                    id          SERIAL PRIMARY KEY,
                                    name        varchar(40) NOT NULL,
                                    email       varchar(40) NOT NULL UNIQUE,
                                    onboarded   BIT(1),
                                    favFood     varchar(100),
                                    dislikeFood varchar(100),
                                    breakfast   BIT(1),
                                    lunch       BIT(1),
                                    dinner      BIT(1),
                                    snack       BIT(1),
                                    NumOfDay    int
        )
        """
    create_table(create_user_table_script, "")


def onboard_user(insert_patients_value):

    insert_patients_script = "INSERT INTO patients (name, email, onboarded, favFood, dislikeFood, breakfast, lunch, dinner, snack, NumOfDay) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

    insert(insert_patients_script, insert_patients_value)


def get_user_info(email):
    script = "SELECT * FROM patients WHERE email=%s"
    result = select_one(script, (email,))
    return result


# create_user_table()

# onboard_user()

#   try:
#         with psycopg2.connect(
#             host=hostname, dbname=database, user=username, password=pwd, port=port_id
#         ) as conn:
#             with conn.cursor() as cur:

#                 cur.execute("DROP TABLE IF EXISTS patients")
#                 create_user_table = """ CREATE TABLE IF NOT EXISTS patients (
#                                             id          int PRIMARY KEY,
#                                             name        varchar(40) NOT NULL,
#                                             email       varchar(40) NOT NULL,
#                                             onboarded   BIT(1),
#                                             favFood     varchar(100),
#                                             dislikeFood varchar(100),
#                                             breakfast   BIT(1),
#                                             lunch       BIT(1),
#                                             dinner      BIT(1),
#                                             snack       BIT(1),
#                                             NumOfDay    int
#                 )
#                 """
#                 cur.execute(create_user_table)

#                 insert_patients_script = "INSERT INTO patients (id, name, email, onboarded, favFood, dislikeFood, breakfast, lunch, dinner, snack, NumOfDay) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
#                 insert_patients_value = (
#                     1,
#                     "May",
#                     "mayshinlyan29@gmail.com",
#                     "0",
#                     "chicken and avocado",
#                     "creamy stuff",
#                     "0",
#                     "0",
#                     "0",
#                     "0",
#                     3,
#                 )

#                 cur.execute(insert_patients_script, insert_patients_value)
#     except Exception as e:
#         print(e)
#     finally:
#         if conn is not None:
#             conn.close()
