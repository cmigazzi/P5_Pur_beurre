import mysql.connector
import records

import settings

# class Database():
#     def create(self):
#         db = records.Database(
#             f"mysql+mysqlconnector://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}")

#         db.query_file('database.sql')


class Table():
    """Represents a generic Table"""

    def __init__(self, db_connexion):
        """Defines database connection
        """
        self.db = db_connexion

    def insert_query(self, data):
        """Generic insert query for inserting data in single column

        Arguments:
            data {list} -- List of single data
        """

        t = self.db.transaction()

        for unique_data in data:
            # if len(unique_data) > 100:

            self.db.query(
                f"INSERT INTO {self.name} ({self.columns}) VALUES (:unique_data);", unique_data=unique_data)
        t.commit()

        self.db.close()

    def select_id_by_name(self, name):
        rows = self.db.query(
            f"SELECT `id` FROM {self.name} WHERE `name`=:name", name=name)

        id = [r.id for r in rows]
        return id[0]


class Product(Table):
    def __init__(self, db_connexion):
        Table.__init__(self, db_connexion)
        self.name = "Product"
        self.columns = ["name", "description", "url", "nutri_score",
                        "category", "sub_category", "store_0", "store_1", "brand"]

    @staticmethod
    def product_validator(product):

        valid_product = True
        # Check KeyError
        try:
            product["product_name_fr"]
            product["generic_name"]
            product["url"]
            product["categories"]
            product["brands"]
            product["stores"]
            product["nutrition_grade_fr"]
        except KeyError:
            valid_product = False

        # Check empty field and lenght of generic_name
        for key, value in product.items():
            if value == '':
                valid_product = False
                break
            if key == "generic_name":
                if len(value) > 255:
                    valid_product = False
        return valid_product

    def insert_query(self, products):
        t = self.db.transaction()

        # #error tracker
        print("Enregistrement des produits dans la base de données:")
        errors = 0
        for product in products:
            # Counter
            if product == products[-1]:
                print(products.index(product)+1, "/", len(products))
            else:
                print(products.index(product)+1, "/", len(products), end="\r")

            if Product(self.db).product_validator(product) == False:
                errors += 1
                print("erreurs: ", errors)
                continue

            product["name"] = product.pop("product_name_fr")
            product["description"] = product.pop("generic_name")
            product["nutri_score"] = product.pop("nutrition_grade_fr")

            product["brand"] = Brand(self.db).select_id_by_name(product.pop("brands"))

            categories_id = [Category(self.db).select_id_by_name(i)
                             for i in product["categories"]]
            del product["categories"]

            stores_id = [Store(self.db).select_id_by_name(i)
                         for i in product["stores"]]
            del product["stores"]

            product["category"] = categories_id[0]
            try:
                product["sub_category"] = categories_id[1]
            except IndexError:
                product["sub_category"] = None

            for n in range(len(stores_id)):
                field_name = "store_" + str(n)
                product[field_name] = stores_id[n]

            columns = ", ".join(product.keys())
            values = ", ".join([":"+str(i) for i in product.keys()])

            self.db.query(
                f"INSERT INTO {self.name} ({columns}) VALUES ({values});", **product)
        print(errors)
        t.commit()
        self.db.close()

    def select_product_list_by_category(self, categories_selected):

        query = (f"SELECT DISTINCT {self.name}.`name` AS `name`, b.`name` AS brand "
                 f"FROM eat_better.{self.name} "
                 "INNER JOIN eat_better.category AS c "
                 f"ON {self.name}.sub_category = c.id "
                 "INNER JOIN eat_better.brand AS b "
                 f"ON {self.name}.brand = b.id "
                 f"AND {self.name}.category = {categories_selected['category']} "
                 f"AND {self.name}.sub_category = {categories_selected['sub_category']} "
                 "AND c.`name` NOT LIKE 'en:%' OR 'fr:%';"
                 )
        print(query)
        rows = self.db.query(query)

        results = [(r.name, r.brand) for r in rows]

        return results

    def get_nutri_score_by_name(self, name_and_brand):

        field_query = {"name": name_and_brand[0], "brand": name_and_brand[1]}

        brand_id = Brand(self.db).select_id_by_name(field_query["brand"])

        field_query["brand"] = brand_id

        query = ("SELECT DISTINCT name, brand, nutri_score " 
                 "FROM eat_better.product "
                 "WHERE `name`=:name AND brand=:brand;")
        
        rows = self.db.query(query, **field_query)

        return rows[0]

    def select_product_by_name_and_brand(self, name_and_brand):

        field_query = {"name": name_and_brand[0], "brand": name_and_brand[1]}

        brand_id = Brand(self.db).select_id_by_name(field_query["brand"])

        field_query["brand"] = brand_id

        query = ("SELECT DISTINCT * FROM eat_better.product " 
                 "WHERE name=:name and brand=:brand;")

        rows = self.db.query(query, **field_query)

        return rows[0]

    def get_better_products(self, nutri_score):

        all_nutri_scores = ['a', 'b', 'c', 'd', 'e']
        nutri_score_wanted = tuple(n for n in all_nutri_scores if n < nutri_score)

        
        query = ("SELECT DISTINCT name, description, brand, store_0, store_1, url "
                 "FROM eat_better.product "
                 f"WHERE nutri_score IN {nutri_score_wanted} " 
                 "AND category=40 AND sub_category=74 "
                 "ORDER BY nutri_score "
                 "LIMIT 5;")

        rows = self.db.query(query)


class Category(Table):
    def __init__(self, db_connexion):
        Table.__init__(self, db_connexion)
        self.name = "Category"
        self.columns = "name"

    def select_five_main_categories(self):

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

    def select_sub_categories(self, categories_selected):

        query = ("SELECT DISTINCT category.`name`, category.id "
                 "FROM eat_better.product "
                 "INNER JOIN eat_better.category "
                 f"ON product.sub_category = category.id "
                 f"WHERE product.category={categories_selected['category']} "
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

    def __init__(self, db_connexion):
        Table.__init__(self, db_connexion)
        self.name = "Brand"
        self.columns = "name"


class Store(Table):

    def __init__(self, db_connexion):
        Table.__init__(self, db_connexion)
        self.name = "Store"
        self.columns = "name"


if __name__ == "__main__":
    # c = Category(settings.DB_CONNEXION).select_five_main_categories()
    print(settings.DB_CONNEXION)
    db_connexion = records.Database(settings.DB_CONNEXION)
    
    p = Product(db_connexion)
    test = p.get_nutri_score_by_name(("Minis Banana", "weetabix"))
    print(test)

    db_connexion.close
