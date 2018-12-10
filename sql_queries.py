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
    create_db_query = (
        f"CREATE DATABASE IF NOT EXISTS {DB_NAME} DEFAULT CHARACTER SET utf8mb4;")

    TABLES = {}

    TABLES["Category"] = f"""
        CREATE TABLE IF NOT EXISTS {DB_NAME}.`Category` (
            `id` SMALLINT NOT NULL AUTO_INCREMENT,
            `name` VARCHAR(100) NULL,
            PRIMARY KEY (`id`))
        ENGINE = InnoDB;
        """

    TABLES["Store"] = f"""
        CREATE TABLE IF NOT EXISTS {DB_NAME}.`Store` (
            `id` SMALLINT NOT NULL AUTO_INCREMENT,
            `name` VARCHAR(255) NULL,
            PRIMARY KEY (`id`))
        ENGINE = InnoDB;
        """

    TABLES["Brand"] = f"""
        CREATE TABLE IF NOT EXISTS {DB_NAME}.`Brand` (
            `id` INT NOT NULL AUTO_INCREMENT,
            `name` VARCHAR(255) NULL,
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

# Insert data from API
def save_data_API(categories, brands, stores):
    """This fnction saves the data from API to database

    Arguments:
        categories {list} -- list of all categories
        brands {list} -- list of all brands as strings
        stores {list} -- list of all stores as strings
    """
    db_connection = mysql.connector.connect(user=DB_USER,
                                            password=DB_PASSWORD,
                                            host=DB_HOST,
                                            database=DB_NAME)

    cursor = db_connection.cursor()

    # queries
    categories_query = ("INSERT INTO Category (name) VALUES (%s)")
    brands_query = ("INSERT INTO Brand (name) VALUES (%s)")
    stores_query = ("INSERT INTO Store (name) VALUES (%s)")

    # Execution
    for category in categories:
        cursor.execute(categories_query, (category,))
    print("Categories saved !")
    for brand in brands:
        cursor.execute(brands_query, (brand,))
    print("Brands saved !")
    for store in stores:
        cursor.execute(stores_query, (store,))
    print("Stores saved !")

    db_connection.commit()
    cursor.close()
    db_connection.close()


def save_products(products):
    db_connection = mysql.connector.connect(user=DB_USER,
                                            password=DB_PASSWORD,
                                            host=DB_HOST,
                                            database=DB_NAME,
                                            charset="utf8mb4")
    
    cursor = db_connection.cursor()

    name_errors = 0
    query_errors = 0
    data_errors = 0
    print(f"Nombre de produits (avant l'enregistrement): {len(products)}")
    for product in products:
        try:
            product["nutrition_grade_fr"]
        except KeyError:
            product["nutrition_grade_fr"] = "n"

        try:
            product["product_name_fr"]
        except KeyError:
            name_errors += 1
            continue

        # Get number of categories
        category_field = ", ".join(["category_"+str(id)
                                    for (id, name) in product["categories"]])
        
        if len(product["categories"]) >= 1:
            category_0 = product["categories"][0][1]
            select_category_values = f"(SELECT id FROM Category WHERE name='{category_0}' LIMIT 1)"
            if len(product["categories"]) >= 2:
                category_1 = product["categories"][1][1]
                select_category_values += f", \n(SELECT id FROM Category WHERE name='{category_1}' LIMIT 1)"
                if len(product["categories"]) == 3:
                    category_2 = product["categories"][2][1]
                    select_category_values += f", \n(SELECT id FROM Category WHERE name='{category_2}' LIMIT 1)"
                    

        # # Get number of stores
        store_field = ", ".join(["store_"+str(id)
                                 for (id, name) in product["stores"]])

        if len(product["stores"]) >= 1:
            store_0 = product["stores"][0][1]
            select_store_values = f"(SELECT id FROM Store WHERE name='{store_0}' LIMIT 1)"
            if len(product["stores"]) == 2:
                store_1 = product["stores"][1][1]
                select_store_values += f", \n(SELECT id FROM Store WHERE name='{store_1}' LIMIT 1)"

        brand = product["brands"]
        select_brand_value = f"(SELECT id FROM Brand WHERE name='{brand}' LIMIT 1)"

        field_name = f"(name, description, url, nutri_score, brand, {store_field}, {category_field})"

        insertion_query = f"""INSERT INTO Product {field_name} 
                  VALUES ("{product["product_name_fr"]}", "{product["generic_name"]}", "{product["url"]}", "{product["nutrition_grade_fr"]}",
                  {select_brand_value},
                  {select_store_values},
                  {select_category_values});"""

        try:
            cursor.execute(insertion_query)

        except (KeyError, mysql.connector.errors.ProgrammingError):
            query_errors += 1
            print("query", query_errors)
            # print(insertion_query)
        except mysql.connector.errors.DataError:
            data_errors += 1
            print("data", data_errors)
            # print(insertion_query)
            
    print(name_errors)
    db_connection.commit()
    cursor.close()
    db_connection.close()


if __name__ == "__main__":
    create_database()
