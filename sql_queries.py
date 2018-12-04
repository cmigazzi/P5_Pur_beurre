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

    TABLES = {}

    TABLES["Category"] = f""" 
        CREATE TABLE IF NOT EXISTS {DB_NAME}.`Category` (
            `id` SMALLINT NOT NULL AUTO_INCREMENT,
            `name` VARCHAR(100) NULL,
            `tag` VARCHAR(100) NULL,
            PRIMARY KEY (`id`))
        ENGINE = InnoDB;
        """

    TABLES["Store"] = f"""
        CREATE TABLE IF NOT EXISTS {DB_NAME}.`Store` (
            `id` SMALLINT NOT NULL AUTO_INCREMENT,
            `name` VARCHAR(45) NULL,
            `tag` VARCHAR(45) NULL,
            PRIMARY KEY (`id`))
        ENGINE = InnoDB;
        """

    TABLES["Brand"] = f"""
        CREATE TABLE IF NOT EXISTS {DB_NAME}.`Brand` (
            `id` INT NOT NULL AUTO_INCREMENT,
            `name` VARCHAR(45) NULL,
            PRIMARY KEY (`id`))
        ENGINE = InnoDB;
        """

    TABLES["Product"] = f"""
        CREATE TABLE IF NOT EXISTS {DB_NAME}.`Product` (
            `id` INT NOT NULL AUTO_INCREMENT,
            `name` VARCHAR(150) NOT NULL,
            `description` TINYTEXT NULL,
            `url` VARCHAR(255) NOT NULL,
            `nutri_score` VARCHAR(1) NULL,
            `category_0` SMALLINT NOT NULL,
            `category_1` SMALLINT NULL,
            `category_2` SMALLINT NULL,
            `store_0` SMALLINT NOT NULL,
            `store_1` SMALLINT NULL,
            `brand` INT NULL,
            PRIMARY KEY (`id`),
            UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
            INDEX `fk_category_1_idx` 
                (`category_0` ASC, `category_1` ASC, `category_2` ASC) VISIBLE,
            INDEX `fk_category_1_idx1` (`category_1` ASC) VISIBLE,
            INDEX `fk_category_2_idx` (`category_2` ASC) VISIBLE,
            INDEX `fk_store_0_idx` (`store_0` ASC) VISIBLE,
            INDEX `fk_store_1_idx` (`store_1` ASC) VISIBLE,
            INDEX `fk_brand_idx` (`brand` ASC) VISIBLE,
            CONSTRAINT `fk_category_0`
                FOREIGN KEY (`category_0`)
                REFERENCES {DB_NAME}.`Category` (`id`)
                ON DELETE NO ACTION
                ON UPDATE NO ACTION,
            CONSTRAINT `fk_category_1`
                FOREIGN KEY (`category_1`)
                REFERENCES {DB_NAME}.`Category` (`id`)
                ON DELETE NO ACTION
                ON UPDATE NO ACTION,
            CONSTRAINT `fk_category_2`
                FOREIGN KEY (`category_2`)
                REFERENCES {DB_NAME}.`Category` (`id`)
                ON DELETE NO ACTION
                ON UPDATE NO ACTION,
            CONSTRAINT `fk_store_0`
                FOREIGN KEY (`store_0`)
                REFERENCES {DB_NAME}.`Store` (`id`)
                ON DELETE NO ACTION
                ON UPDATE NO ACTION,
            CONSTRAINT `fk_store_1`
                FOREIGN KEY (`store_1`)
                REFERENCES {DB_NAME}.`Store` (`id`)
                ON DELETE NO ACTION
                ON UPDATE NO ACTION,
            CONSTRAINT `fk_brand`
                FOREIGN KEY (`brand`)
                REFERENCES {DB_NAME}.`Brand` (`id`)
                ON DELETE NO ACTION
                ON UPDATE NO ACTION)
            ENGINE = InnoDB;
        """

    TABLES["Substitution"] = f"""
        CREATE TABLE IF NOT EXISTS {DB_NAME}.`Substitution` (
            `id` SMALLINT NOT NULL,
            `original` INT NULL,
            `substitute` INT NULL,
            PRIMARY KEY (`id`),
            INDEX `fk_substitution_idx` (`original` ASC) VISIBLE,
            INDEX `fk_substitute_idx` (`substitute` ASC) VISIBLE,
            CONSTRAINT `fk_original`
                FOREIGN KEY (`original`)
                REFERENCES {DB_NAME}.`Product` (`id`)
                ON DELETE NO ACTION
                ON UPDATE NO ACTION,
            CONSTRAINT `fk_substitute`
                FOREIGN KEY (`substitute`)
                REFERENCES {DB_NAME}.`Product` (`id`)
                ON DELETE NO ACTION
                ON UPDATE NO ACTION)
            ENGINE = InnoDB;
    """

    # queries execution
    cursor.execute(create_db_query)

    for description in TABLES.values():
        cursor.execute(description)
    
    cursor.close()
    db_connection.close()
        

if __name__ == "__main__":
    create_database()

