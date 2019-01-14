"""Contains the Schema class that creates schema and tables."""

import records

from settings import DB_NAME, DB_CONNEXION, DB_HOST, DB_USER, DB_PASSWORD


class SchemaCreator():
    """Represent the Database to install."""

    def __init__(self):
        """Get the DB_NAME to create the database."""
        self.db_name = DB_NAME

    def create(self):
        """Create schema."""
        db = records.Database(
            f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:3306/")
        db.query(
            f"CREATE SCHEMA IF NOT EXISTS `{self.db_name}` "
            "DEFAULT CHARACTER SET utf8mb4;")
        db.close()


class TableCreator():
    """Represent the creator of the tables.

    Arguments:
        db_connection {<class records.Database>} -- database connection Object
    """

    def __init__(self, db_connection):
        """Please see help(TableCreator) for more details."""
        self.db = db_connection
        self.db_name = DB_NAME

    def create(self):
        """Create generic method."""
        self.db.query(self.query)


class CategoryCreator(TableCreator):
    """Represent the Category table creator.

    Inherit of TableCreator
    Arguments:
        db_connection {<class records.Database>} -- database connection Object
    """

    def __init__(self, db_connection):
        """Set create query as attribute."""
        super().__init__(db_connection)
        self.query = ("CREATE TABLE IF NOT EXISTS "
                      f"`{self.db_name}`.`Category` ("
                      "`id` SMALLINT NOT NULL AUTO_INCREMENT,"
                      "`name` VARCHAR(100) NOT NULL,"
                      "PRIMARY KEY (`id`))"
                      "ENGINE = InnoDB;")


class StoreCreator(TableCreator):
    """Represent the Store table creator.

    Inherit of TableCreator
    Arguments:
        db_connection {<class records.Database>} -- database connection Object
    """

    def __init__(self, db_connection):
        """Set create query as attribute."""
        super().__init__(db_connection)
        self.query = (f"CREATE TABLE IF NOT EXISTS `{self.db_name}`.`Store` ("
                      "`id` SMALLINT NOT NULL AUTO_INCREMENT,"
                      "`name` VARCHAR(45) NOT NULL,"
                      "PRIMARY KEY (`id`))"
                      "ENGINE = InnoDB;")


class BrandCreator(TableCreator):
    """Represent the Brand table creator.

    Inherit of TableCreator
    Arguments:
        db_connection {<class records.Database>} -- database connection Object
    """

    def __init__(self, db_connection):
        """Set create query as attribute."""
        super().__init__(db_connection)
        self.query = (f"CREATE TABLE IF NOT EXISTS `{self.db_name}`.`Brand` ("
                      "`id` SMALLINT NOT NULL AUTO_INCREMENT, "
                      "`name` VARCHAR(45) NOT NULL,"
                      "PRIMARY KEY (`id`)) "
                      "ENGINE = InnoDB;")


class ProductCreator(TableCreator):
    """Represent the Product table creator.

    Inherit of TableCreator
    Arguments:
        db_connection {<class records.Database>} -- database connection Object
    """

    def __init__(self, db_connection):
        """Set create query as attribute."""
        super().__init__(db_connection)
        self.query = ("CREATE TABLE IF NOT EXISTS "
                      f"`{self.db_name}`.`Product` ("
                      "`id` INT NOT NULL AUTO_INCREMENT, "
                      "`name` VARCHAR(150) NOT NULL, "
                      "`description` TINYTEXT NULL, "
                      "`url` VARCHAR(255) NOT NULL, "
                      "`nutri_score` VARCHAR(1) NULL, "
                      "`category` SMALLINT NOT NULL, "
                      "`sub_category` SMALLINT NULL, "
                      "`store_0` SMALLINT NOT NULL, "
                      "`store_1` SMALLINT NULL, "
                      "`brand` SMALLINT NULL, "
                      "PRIMARY KEY (`id`), "
                      "UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE, "
                      "INDEX `fk_category_idx` (`category` ASC) VISIBLE, "
                      "INDEX `fk_sub_category_idx1` "
                      "(`sub_category` ASC) VISIBLE, "
                      "INDEX `fk_store_0_idx` (`store_0` ASC) VISIBLE, "
                      "INDEX `fk_store_1_idx` (`store_1` ASC) VISIBLE, "
                      "INDEX `fk_brand_idx` (`brand` ASC) VISIBLE, "
                      "CONSTRAINT `fk_category` "
                      "FOREIGN KEY (`category`) "
                      f"REFERENCES `{self.db_name}`.`Category` (`id`) "
                      "ON DELETE NO ACTION "
                      "ON UPDATE NO ACTION, "
                      "CONSTRAINT `fk_sub_category` "
                      "FOREIGN KEY (`sub_category`) "
                      f"REFERENCES `{self.db_name}`.`Category` (`id`) "
                      "ON DELETE NO ACTION "
                      "ON UPDATE NO ACTION, "
                      "CONSTRAINT `fk_store_0` "
                      "FOREIGN KEY (`store_0`) "
                      f"REFERENCES `{self.db_name}`.`Store` (`id`) "
                      "ON DELETE NO ACTION "
                      "ON UPDATE NO ACTION, "
                      "CONSTRAINT `fk_store_1` "
                      "FOREIGN KEY (`store_1`) "
                      f"REFERENCES `{self.db_name}`.`Store` (`id`) "
                      "ON DELETE NO ACTION "
                      "ON UPDATE NO ACTION, "
                      "CONSTRAINT `fk_brand` "
                      "FOREIGN KEY (`brand`) "
                      f"REFERENCES `{self.db_name}`.`Brand` (`id`) "
                      "ON DELETE NO ACTION "
                      "ON UPDATE NO ACTION) "
                      "ENGINE = InnoDB;")


class SubstitutionCreator(TableCreator):
    """Represent the Substitution table creator.

    Inherit of TableCreator
    Arguments:
        db_connection {<class records.Database>} -- database connection Object
    """

    def __init__(self, db_connection):
        """Set create query as attribute."""
        super().__init__(db_connection)
        self.query = ("CREATE TABLE IF NOT EXISTS "
                      f"`{self.db_name}`.`Substitution` ("
                      "`id` SMALLINT NOT NULL AUTO_INCREMENT, "
                      "`original` INT NOT NULL, "
                      "`substitute` INT NOT NULL, "
                      "PRIMARY KEY (`id`), "
                      "INDEX `fk_substitution_idx` (`original` ASC) VISIBLE, "
                      "INDEX `fk_substitute_idx` (`substitute` ASC) VISIBLE, "
                      "CONSTRAINT `fk_original` "
                      "FOREIGN KEY (`original`) "
                      f"REFERENCES `{self.db_name}`.`Product` (`id`) "
                      "ON DELETE NO ACTION "
                      "ON UPDATE NO ACTION, "
                      "CONSTRAINT `fk_substitute` "
                      " FOREIGN KEY (`substitute`) "
                      f"REFERENCES `{self.db_name}`.`Product` (`id`) "
                      "ON DELETE NO ACTION "
                      " ON UPDATE NO ACTION) "
                      "ENGINE = InnoDB;")


if __name__ == "__main__":
    db = records.Database(DB_CONNEXION)
    c = ProductCreator(db)
    print(c)
    print(c.db_name)
    print(c.query)
