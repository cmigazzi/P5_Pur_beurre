"""This module manage all the MySQL queries."""


import mysql.connector
import records

import settings

# class Database():
#     def create(self):
#         db = records.Database(
#             f"mysql+mysqlconnector://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:3306/")

#         db.query_file('database.sql')


class Table():
    """Represent a generic Table.

    Arguments:
        db_connexion {<class records.Database>} -- Records Object that provides database connection

    """

    def __init__(self, db_connexion):
        """Please see help(Table) for more details."""
        self.db = db_connexion

    def insert_query(self, data):
        """Insert query for inserting data in single column.

        Arguments:
            data {list} -- List of single data
        """
        t = self.db.transaction()

        for unique_data in data:

            self.db.query(
                f"INSERT INTO {self.name} ({self.columns}) VALUES (:unique_data);",
                unique_data=unique_data)
        t.commit()

    def select_id_by_name(self, name):
        """Return id of the name pass in parameter.

        Arguments:
            name {str} -- name to select

        Returns:
            str -- id of the name

        """
        rows = self.db.query(
            f"SELECT `id` FROM {self.name} WHERE `name`=:name", name=name)

        id = [r.id for r in rows]
        return id[0]


class Product(Table):
    """Represent the Product table.

    Inherit from Table class.

    Arguments:
        db_connexion {<class records.Database>} -- Records Object that provides database connection

    Attributes:
        name [str] -- Name of the table
        columns [list] -- All the columns of the table

    """

    def __init__(self, db_connexion):
        """Please see help(Product) for more details."""
        Table.__init__(self, db_connexion)
        self.name = "Product"
        self.columns = ["name", "description", "url", "nutri_score",
                        "category", "sub_category", "store_0", "store_1", "brand"]

    def insert_query(self, products):
        """Insert product in Product table.

        Override Table method

        Arguments:
            products {list} -- dictionnaries of product properties

        """
        t = self.db.transaction()

        print("Enregistrement des produits dans la base de données:")
        for product in products:
            # Counter
            if product == products[-1]:
                print(products.index(product)+1, "/", len(products))
            else:
                print(products.index(product)+1, "/", len(products), end="\r")

            product["brand"] = Brand(self.db).select_id_by_name(
                product["brand"])

            product["category"] = Category(self.db).select_id_by_name(product["category"])

            if product["sub_category"] is not None:
                product["sub_category"] = Category(self.db).select_id_by_name(product["sub_category"])

            product["store_0"] = Store(self.db).select_id_by_name(product["store_0"])

            try:
                product["store_1"]
            except KeyError:
                pass
            else:
                product["store_1"] = Store(self.db).select_id_by_name(product["store_1"])

            columns = ", ".join(product.keys())
            values = ", ".join([":"+str(i) for i in product.keys()])

            self.db.query(
                f"INSERT INTO {self.name} ({columns}) VALUES ({values});", **product)

        t.commit()
        self.db.close()

    def select_product_list_by_category(self, selections):
        """Select products in a single categoy.

        Arguments:
            selections {dict} -- Selections of the user with keys 'category' and 'sub_category'

        Returns:
            [list] -- dictionnaires of the row results

        """
        query = (f"SELECT DISTINCT {self.name}.`name` AS `name`, b.`name` AS brand "
                 f"FROM eat_better.{self.name} "
                 "INNER JOIN eat_better.category AS c "
                 f"ON {self.name}.sub_category = c.id "
                 "INNER JOIN eat_better.brand AS b "
                 f"ON {self.name}.brand = b.id "
                 f"AND {self.name}.category = {selections['category']} "
                 f"AND {self.name}.sub_category = {selections['sub_category']} "
                 "AND c.`name` NOT LIKE 'en:%' OR 'fr:%';"
                 )
        print(query)
        rows = self.db.query(query)

        results = [(r.name, r.brand) for r in rows]

        return results

    def get_nutri_score_by_name(self, selections):
        """Select nutri_score of a product.

        Arguments:
            selections {dict} -- Selections of the user with keys 'name' and 'brand'.

        Returns:
            str -- the nutri_score of the product.

        """
        query = ("SELECT DISTINCT nutri_score "
                 "FROM eat_better.product "
                 "WHERE `name`=:name AND brand=:brand;")

        rows = self.db.query(query, **selections)

        return rows[0].nutri_score

    def get_better_products(self, selections):
        """Select maximum 5 better products.

        Arguments:
            selections {dict} -- Selections of the user with keys 'nutri_score'

        Returns:
           list -- dictionnaries with query result

        """
        all_nutri_scores = ['a', 'b', 'c', 'd', 'e']
        nutri_score_wanted = tuple(
            n for n in all_nutri_scores if n < selections["nutri_score"])

        query = ("SELECT DISTINCT product.name AS name, description, "
                 "b.name AS brand_name, b.id AS brand, s0.name AS store_0, s1.name AS store_1, url "
                 "FROM eat_better.product "
                 "INNER JOIN eat_better.brand AS b "
                 "ON product.brand = b.id "
                 "INNER JOIN eat_better.store AS s0 "
                 "ON product.store_0 = s0.id "
                 "INNER JOIN eat_better.store AS s1 "
                 "ON product.store_1 = s1.id "
                 f"WHERE nutri_score IN {nutri_score_wanted} "
                 "AND category=:category AND sub_category=:sub_category "
                 "ORDER BY nutri_score "
                 "LIMIT 5;")

        rows = self.db.query(query, **selections)

        return rows.all()


class Category(Table):
    """Represent the Category table.

    Inherit from Table class and extend insert_query and select_id_by_name methods.

    Arguments:
        db_connexion {<class records.Database>} -- Records Object that provides database connection

    Attributes:
        name [str] -- Name of the table
        columns [list] -- All the columns of the table

    """

    def __init__(self, db_connexion):
        """Please see help(Category) for more details."""
        Table.__init__(self, db_connexion)
        self.name = "Category"
        self.columns = "name"

    def select_five_main_categories(self):
        """Select the main categories.

        Returns:
            list -- names of the categories

        """
        query = (f"SELECT DISTINCT {self.name}.`name` "
                 "FROM eat_better.product "
                 f"INNER JOIN eat_better.{self.name} "
                 f"ON product.category = {self.name}.id "
                 f"WHERE {self.name}.`name` NOT LIKE 'en:%' OR 'fr:%' "
                 f"GROUP BY {self.name}.`name` "
                 "ORDER BY count(*) DESC "
                 "LIMIT 5;")
        # print(query)
        rows = self.db.query(query)

        results = [r.name for r in rows]

        return results

    def select_sub_categories(self, selections):
        """Select maximum 20 sub categories.

        Arguments:
            selections {dict} -- Selections of the user with keys 'ncategory'.

        Returns:
            list -- names of the sub-categories

        """
        query = ("SELECT DISTINCT category.`name`, category.id "
                 "FROM eat_better.product "
                 "INNER JOIN eat_better.category "
                 f"ON product.sub_category = category.id "
                 f"WHERE product.category={selections['category']} "
                 "AND category.`name` NOT LIKE 'en:%' OR 'fr:%' "
                 "GROUP BY category.`name` "
                 "HAVING COUNT(*) >= 5 "
                 "ORDER BY count(*) DESC "
                 "LIMIT 20;")
        # print(query)
        rows = self.db.query(query)

        results = [r.name for r in rows]

        return results


class Brand(Table):
    """Represent the Brand table.

    Inherit from Table class and extend insert_query and select_id_by_name methods.

    Arguments:
        db_connexion {<class records.Database>} -- Records Object that provides database connection

    Attributes:
        name [str] -- Name of the table
        columns [list] -- All the columns of the table

    """

    def __init__(self, db_connexion):
        """Please see help(Brand) for more details."""
        Table.__init__(self, db_connexion)
        self.name = "Brand"
        self.columns = "name"


class Store(Table):
    """Represent the Store table.

    Inherit from Table class and extend insert_query and select_id_by_name methods.

    Arguments:
        db_connexion {<class records.Database>} -- Records Object that provides database connection

    Attributes:
        name [str] -- Name of the table
        columns [list] -- All the columns of the table

    """

    def __init__(self, db_connexion):
        """Please see help(Store) for more details."""
        Table.__init__(self, db_connexion)
        self.name = "Store"
        self.columns = "name"


class Substitution(Table):"""Represent the Substitution table.

    Inherit from Table class and extend insert_query and select_id_by_name methods.

    Arguments:
        db_connexion {<class records.Database>} -- Records Object that provides database connection

    Attributes:
        name [str] -- Name of the table
        columns [list] -- All the columns of the table

    """

    def __init__(self, db_connexion):
        """Please see help(Store) for more details."""
        Table.__init__(self, db_connexion)
        self.name = "Substitution"
        self.columns = ["original", "substitute"]

    def save_substitution(self, selections):
        """Save the substitution.
        
        Arguments:
            selections {dict} -- original and substitute products properties.
        """

        t = self.db.transaction()
        query = (f"INSERT INTO {self.name} (original, substitute) VALUES "
                 "((SELECT id FROM Product WHERE name=:name AND brand=:brand LIMIT 1), "
                 "(SELECT id FROM Product WHERE name=:substitute AND brand=:substitute_brand LIMIT 1));")

        self.db.query(query, **selections)
        t.commit()

    def get_all(self):

        query = ("SELECT o.name AS original, ob.name AS original_brand, s.name AS substitute, "
                 "sb.name AS substitute_brand, s.url AS url "
                 "FROM eat_better.substitution "
                 "INNER JOIN eat_better.product AS o "
                 "ON substitution.original = o.id "
                 "INNER JOIN eat_better.product AS s "
                 "ON substitution.substitute = s.id "
                 "INNER JOIN eat_better.brand AS ob "
                 "ON o.brand = ob.id "
                 "INNER JOIN eat_better.brand AS sb "
                 "ON s.brand = sb.id;")

        rows = self.db.query(query)

        return rows.all()


if __name__ == "__main__":
    pass
