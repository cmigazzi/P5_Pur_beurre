import mysql.connector
import records

import settings

# class Database():
#     def create(self):
#         db = records.Database(
#             f"mysql+mysqlconnector://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}")
        
#         db.query_file('database.sql', fetchall=True)


class Table():
    """Represents a generic Table"""

    def __init__(self):
        """Defines database connection
        """
        self.db = records.Database(
            f"mysql+mysqlconnector://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:3306/{settings.DB_NAME}?charset=utf8mb4")

    def insert_query(self, data):
        """Generic insert query for inserting data in single column

        Arguments:
            data {list} -- List of single data
        """

        t = self.db.transaction()

        for unique_data in data:
            self.db.query(
                f"INSERT INTO {self.name} ({self.columns}) VALUES (:unique_data);", unique_data=unique_data)
        t.commit()

    def select_id_by_name(self, name):
        rows = self.db.query(
            f"SELECT `id` FROM {self.name} WHERE `name`=:name", name=name)

        id = [r.id for r in rows]
        return id[0]


class Product(Table):
    def __init__(self):
        Table.__init__(self)
        self.name = "Product"
        self.columns = ["name", "description", "url", "nutri_score",
                        "category_0", "category_1", "category_2", "store_0", "store_1", "brand"]

    def insert_query(self, products):
        # t = self.db.transaction()
        err = 0
        for product in products:
            product["name"] = product.pop("product_name_fr")
            product["description"] = product.pop("generic_name")
            try:
                product["nutri_score"] = product.pop("nutrition_grade_fr")
            except KeyError:
                err += 1
                continue

            product["brand"] = Brand().select_id_by_name(product.pop("brands"))

            categories_id = [Category().select_id_by_name(i)
                             for i in product["categories"]]
            del product["categories"]
            stores_id = [Store().select_id_by_name(i)
                         for i in product["stores"]]
            del product["stores"]

            for n in range(len(categories_id)):
                field_name = "category_" + str(n)
                product[field_name] = categories_id[n]

            for n in range(len(stores_id)):
                field_name = "store_" + str(n)
                product[field_name] = stores_id[n]

            columns = ", ".join(product.keys())
            values = ", ".join([":"+str(i) for i in product.keys()])

            self.db.query(
                f"INSERT INTO {self.name} ({columns}) VALUES ({values});", **product)
        print(err)


class Category(Table):
    def __init__(self):
        Table.__init__(self)
        self.name = "Category"
        self.columns = "name"


class Brand(Table):
    def __init__(self):
        Table.__init__(self)
        self.name = "Brand"
        self.columns = "name"


class Store(Table):
    def __init__(self):
        Table.__init__(self)
        self.name = "Store"
        self.columns = "name"


if __name__ == "__main__":
    # cat_data = ['poissons', 'viandes', 'frites']
    products = [{'stores': ['Intermarché', 'Leader Price'], 'generic_name': 'Crème glacée Caramel, sauce caramel (9%) et des Pépites aux amandes (9%)', 'url': 'https://fr.openfoodfacts.org/produit/8718114712277/ben-jerry-s-fairly-nuts', 'brands': "Ben & Jerry's", 'nutrition_grade_fr':
                 'd', 'product_name_fr': "Ben & Jerry's - Fairly Nuts", 'categories': ['Desserts', ' Surgelés']}, {'url': 'https://fr.openfoodfacts.org/produit/3013520080398/sorbet-framboise-plein-fruit-carte-d-or', 'generic_name': 'sorbet plein fruit framboise avec des morceaux de framboise (1,4%)', 'stores': ['Carrefour', 'Super U'], 'product_name_fr': 'Sorbet framboise plein fruit', 'categories': ['Desserts', ' Surgelés', ' Desserts glacés'], 'brands': "Carte d'or", 'nutrition_grade_fr': 'c'}]
    # Category().insert_query(cat_data)
    # Brand().insert_query(cat_data)
    # Store().insert_query(cat_data)
    p = Product().insert_query(products)
    print(p)
