"""Contains all the functions to get data from OpenFoodFacts API."""


import requests
import mysql.connector
import records

from settings import (DB_USER, DB_PASSWORD, DB_HOST, CATEGORIES,
                      SEARCH_API_URL, FIELD_NEEDED, DB_CONNEXION)
from models import Category, Brand, Product, Store


def create_database():
    """Create the databse schema.

    !!! DON'T FORGET to configure                       !!!
    !!! your username, password, host and database name !!!
    !!! in settings.py module                           !!!
    """
    db_connection = mysql.connector.connect(user=DB_USER,
                                            password=DB_PASSWORD,
                                            host=DB_HOST)

    cursor = db_connection.cursor()

    f = open("database.sql", "r")
    query = " ".join(f.readlines())
    iterator = cursor.execute(query, multi=True)
    for i in iterator:
        i

    cursor.close()
    f.close()
    db_connection.close()


def get_api_data(category):
    """Request the OpenFoodFact API to get data.

    Returns:
        list -- list of dictionnary that represents a product

    """
    products = []

    url = SEARCH_API_URL + \
        f"?search_terms={category}&search_tag=category&sort_by=unique_scans_n&page_size=250&json=1"
    json_response = requests.get(url).json()
    products_list = json_response["products"]

    for complete_product in products_list:
        clean_product = {
            k: v for k, v in complete_product.items() if k in FIELD_NEEDED}
        products.append(clean_product)

    return products


def save_data():
    """Save the data requested to database."""
    products = []
    all_categories = []
    all_stores = []
    all_brands = []
    errors = 0

    for category in CATEGORIES:
        print(f"Chargement des produits de type {category}")
        products_in_category = get_api_data(category)

        for product in products_in_category:

            if product_validator(product) is False:
                errors += 1
                continue
            else:

                try:
                    categories = clean_tag(product["categories"], 100)
                    stores = clean_tag(product["stores"], 45)
                    brands = clean_tag(product["brands"], 45)
                    category_index = categories.index(category)
                except KeyError:
                    errors += 1
                    continue
                except ValueError:
                    errors += 1
                    continue

            filter_categories = categories[category_index:category_index+2]
            product["categories"] = [
                category for category in filter_categories]

            filter_stores = stores[:2]
            product["stores"] = [store for store in filter_stores]

            product["brands"] = brands[0]

            all_categories += filter_categories
            all_stores += filter_stores
            all_brands.append(product["brands"])

            products.append(product)

    print(f"{errors} éléments n'ont pas pu être importés car ils sont incomplets.")

    clean_categories = clean_duplicate(all_categories)
    clean_brands = clean_duplicate(all_brands)
    clean_stores = clean_duplicate(all_stores)

    db_connection = records.Database(DB_CONNEXION)

    Category(db_connection).insert_query(clean_categories)
    Brand(db_connection).insert_query(clean_brands)
    Store(db_connection).insert_query(clean_stores)
    Product(db_connection).insert_query(products)

    db_connection.close()


def product_validator(product):
    """Check if a product is valid."""
    valid_product = True
    # Check KeyError
    try:
        product["product_name_fr"]
        product["generic_name"]
        product["url"]
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


def clean_tag(elmt_with_commas, max_lenght):
    """Transform a string of elements separated by commas into a list.

    Arguments:
        elmt_with_commas {string with commas} -- elements separated by commas

    Returns:
        [list] -- elements in a list

    """
    elmt_list = elmt_with_commas.split(",")
    elmt_list = [e.strip() for e in elmt_list if len(e) < max_lenght]
    return elmt_list


def clean_duplicate(list_of_tags):
    """Delete duplicates elements in a list.

    Arguments:
        list_of_tags {list} -- list with duplicates

    Returns:
        list -- list without duplicates

    """
    clean_list = list(set(list_of_tags))
    return clean_list


if __name__ == "__main__":
    save_data()
