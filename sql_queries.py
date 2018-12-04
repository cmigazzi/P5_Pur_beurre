################################################################################
#       This module contains all the MySQL queries for the application        #
###############################################################################

import mysql.connector

from settings import DB_USER, DB_PASSWORD, DB_HOST, DB_NAME


# Initialization queries
def create_database():
    """ 
        This function creates the databse schema 

        !!! DON'T FORGET to configure                       !!!
        !!! your username, password, host and database name !!!
        !!! in settings.py module                           !!!
    """
    db_connection = mysql.connector.connect(user=DB_USER,
                                            password=DB_PASSWORD,
                                                host=DB_HOST)
    
    cursor = db_connection.cursor()

    # queries
    create_db_query = (f"CREATE DATABASE IF NOT EXISTS {DB_NAME} DEFAULT CHARACTER SET utf8;")

    cursor.execute(create_db_query)

if __name__ == "__main__":
    create_database()

