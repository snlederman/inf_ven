import sys
import logging
# ____internal modules____
from common import sql_query

logging.basicConfig(filename='database.log',
                    format='%(asctime)s-%(levelname)s-FILE:%(filename)s-FUNC:%(funcName)s-LINE:%(lineno)d-%(message)s',
                    level=logging.INFO)


def create_database(name):
    query = f'CREATE DATABASE {name}'
    sql_query('database', query)


def create_table(name, *args):
    """Gets a name of a database, name of a new table and a list of arguments
    containing a sql code to implement on the new table"""
    content = str(args).replace("'", "")
    sql_query('table', f'CREATE TABLE {name} {content}')


def main(database):
    """
    Main function of the module, creates the foundation of the database using the MySQL Server
    """
    create_database(database)

    category_table = 'id INT AUTO_INCREMENT PRIMARY KEY', 'category VARCHAR(45)',
    create_table('categories', *category_table)

    subcategory_table = 'id INT AUTO_INCREMENT PRIMARY KEY', 'subcategory VARCHAR(45)'
    create_table('subcategories', *subcategory_table)

    products_table = 'id INT AUTO_INCREMENT PRIMARY KEY', 'name VARCHAR(200)', 'price FLOAT', \
                     'id_categories INT', 'id_subcategories INT', \
                     'FOREIGN KEY (id_categories) REFERENCES categories(id)', \
                     'FOREIGN KEY (id_subcategories) REFERENCES subcategories(id)'
    create_table('products', *products_table)


if __name__ == '__main__':
    main(sys.argv[1])
