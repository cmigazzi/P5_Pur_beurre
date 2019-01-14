"""Contains all the functions to get data from OpenFoodFacts API."""


import requests
import mysql.connector
import records

from settings import CATEGORIES, SEARCH_API_URL, FIELD_NEEDED, DB_CONNEXION
from models import Category, Brand, Product, Store


class Api():
    """Represent the API caller."""

    def call(self):
        """Request the OpenFoodFact API to get data.

        Returns:
            list -- list of dictionnary that represents a product

        """
        clean_products = []

        for category in CATEGORIES:
            print(f"Chargement des produits de type {category}")
            api_url = SEARCH_API_URL + \
                (f"?search_terms={category}"
                 "&search_tag=category&sort_by=unique_scans_n"
                 "&page_size=1000&json=1")
            json_response = requests.get(api_url).json()
            products = json_response["products"]

            for product in products:
                clean_product = {
                    k: v for k, v in product.items()
                    if k in FIELD_NEEDED and v != ''}
                clean_products.append(clean_product)

        return clean_products


class DataFromApiToDatabase():
    """Represent data batch from api call to database.

    Arguments:
        db_connection {<class records.Database>} -- database connection object
        table {str} -- name of the target table

    """

    def __init__(self, db_connection, table):
        """Please see help(DataFromApiToDatabase) for more details."""
        self.elements = []
        self.db = db_connection
        self.table = table

    def __add__(self, element):
        """Add elements to self.elements.

        Arguments:
            element {list} -- new data
        """
        self.elements += element

    def __str__(self):
        """Print the list of the elements."""
        return str(self.elements)

    def append(self, element):
        """Append a single string in self.elements.

        Arguments:
            element {str} -- new data

        """
        self.elements.append(element)

    def clean_duplicate(self):
        """Delete duplicates in self.elements."""
        self.elements = list(set(self.elements))
        self.elements = [e for e in self.elements if e != '']

    def save(self):
        """Save data in target table."""
        if self.table == "Category":
            Category(self.db).insert_query(self.elements)
        elif self.table == "Brand":
            Brand(self.db).insert_query(self.elements)
        elif self.table == "Store":
            Store(self.db).insert_query(self.elements)
        elif self.table == "Product":
            Product(self.db).insert_query(self.elements)


class ProductFromApiToDatabase():
    """Represent a product from api call to database saving.

    Arguments:
        product {list} -- dictionnaries of products property
        category {str} -- main category of the product
        db_connection {<class records.Database>} -- database connection

    """

    def __init__(self, product, category, db_connection):
        """Please see help(ProductFromApiToDatabase) for more details."""
        self.db = db_connection
        self.fields = product
        self.category = category
        self.categories = None
        self.stores = None
        self.brand = None
        self.category_index = None
        self.errors = 0

    def __str__(self):
        """Print product dict."""
        return f"{self.fields}"

    @staticmethod
    def clean_tag(elmt_with_commas, max_lenght):
        """Transform a string of elements separated by commas into a list.

        Arguments:
            elmt_with_commas {string with commas} --
                                elements separated by commas

        Returns:
            [list] -- elements in a list

        """
        elmt_list = elmt_with_commas.split(",")
        elmt_list = [e.strip() for e in elmt_list if len(e) < max_lenght]
        return elmt_list

    def validate(self):
        """Check if a product is valid."""
        # Check KeyError
        try:
            self.fields["product_name_fr"]
            self.fields["generic_name"]
            self.fields["url"]
            self.fields["nutrition_grade_fr"]
            self.fields["categories"]
            self.fields["stores"]
            self.fields["brands"]
        except KeyError:
            return False

        # Check empty field and lenght of generic_name
        for key, value in self.fields.items():
            if value == '':
                return False
                break
            if key == "generic_name":
                if len(value) > 255:
                    return False

        try:
            self.categories = ProductFromApiToDatabase.clean_tag(
                self.fields["categories"], 100)
            self.stores = ProductFromApiToDatabase.clean_tag(
                self.fields["stores"], 45)
            self.brands = ProductFromApiToDatabase.clean_tag(
                self.fields["brands"], 45)
            self.category_index = self.categories.index(self.category)
        except KeyError:
            return False
        except ValueError:
            return False
        except AttributeError:
            self.errors += 1
            print(self.errors)
            return False

    def clean(self):
        """Clean and format product property to be saved."""
        # clean categories
        filter_categories = \
            self.categories[self.category_index: self.category_index+2]
        self.categories = [
            category for category in filter_categories if category != '']
        del self.fields["categories"]
        self.fields["category"] = self.categories[0]

        try:
            self.fields["sub_category"] = self.categories[1]
        except IndexError:
            self.fields["sub_category"] = None

        # clean stores
        filter_stores = self.stores[:2]
        self.stores = [store for store in filter_stores]
        del self.fields["stores"]

        for n in range(len(self.stores)):
            field_name = "store_" + str(n)
            self.fields[field_name] = self.stores[n]

        # clean brand
        self.brand = self.brands[0]
        self.fields["brand"] = self.brand
        del self.fields["brands"]

        # clean others fields
        self.fields["name"] = self.fields.pop("product_name_fr")
        self.fields["description"] = self.fields.pop("generic_name")
        self.fields["nutri_score"] = self.fields.pop("nutrition_grade_fr")


if __name__ == "__main__":
    pass
