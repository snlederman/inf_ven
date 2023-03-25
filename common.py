import logging
import json
import pymysql


logging.basicConfig(filename='common.log',
                    format='%(asctime)s-%(levelname)s-FILE:%(filename)s-FUNC:%(funcName)s-LINE:%(lineno)d-%(message)s',
                    level=logging.INFO)


def configuration(conf_file):
    """Opens the configuration file."""
    with open(conf_file, "r") as jsonfile:
        conf = json.load(jsonfile)
        return conf


CONF_FILE = 'conf.json'
HOST = configuration(CONF_FILE)['HOST']
USER = configuration(CONF_FILE)['MYSQL_USER']
PASSWORD = configuration(CONF_FILE)['MYSQL_PASSWORD']


def connection():
    """gets a user and a password to MySQL Server and returns a pymysql.connection.connection attribute."""
    connect = pymysql.connect(host=HOST,
                              user=USER,
                              password=PASSWORD,
                              cursorclass=pymysql.cursors.DictCursor)
    return connect


def database_connection(database):
    connect = pymysql.connect(host=HOST,
                              user=USER,
                              password=PASSWORD,
                              database=database)
    return connect


def sql_query(obj, query):
    """Receives a string with sql query and returns it result using pymysql module."""
    if obj == 'database':
        con = connection()
    else:
        con = database_connection('plazas')
    with con.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()
        return result


def get_categories_links():
    categories_link_list_query = f"SELECT url FROM category;"
    categories_link = sql_query(categories_link_list_query)
    return list(map(lambda x: x[0], categories_link))


def filling_table(database, table, variables, *data):
    """Gets name of a database, name of a table, string of variables and a list of data and adds it to the table """
    con = create_connection()
    with con.cursor() as cursor:
        select_database = f"USE {database}"
        cursor.execute(select_database)
        variables = variables.replace("'", "")
        values = len(data) * '%s, '
        values = values.rstrip(", ")
        fill_table = f"REPLACE INTO {table} {variables} VALUES ({values})"
        cursor.execute(fill_table, [*data])
        con.commit()
