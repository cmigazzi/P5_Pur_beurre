################################################################################
#           This module contains all the functions to get data from            #
#                            OpenFoodFacts API                                 #
################################################################################

import requests
import mysql.connector

from settings import DB_USER, DB_PASSWORD, DB_HOST, CATEGORIES, SEARCH_API_URL, FIELD_NEEDED
from models import Category, Brand, Product, Store

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

    f = open("database.sql", "r")
    query = " ".join(f.readlines())
    iterator = cursor.execute(query, multi=True)
    for i in iterator:
        i
        
    cursor.close()
    f.close()
    db_connection.close()

def get_api_data(category):
    """This function requests the OpenFoodFact API to get data

    Returns:
        list -- list of dictionnary that represents a product
    """
    products = []

    url = SEARCH_API_URL + \
        f"?search_terms={category}&search_tag=category&page_size=250&json=1"
    json_response = requests.get(url).json()
    products_list = json_response["products"]

    for complete_product in products_list:
        clean_product = {
            k: v for k, v in complete_product.items() if k in FIELD_NEEDED}
        products.append(clean_product)

    return products


def save_data():
    """This function save the data from OFF API to database"""

    products = []
    all_categories = []
    all_stores = []
    all_brands = []

    for category in CATEGORIES:
        print(f"Loading products of {category}")
        products_in_category = get_api_data(category)

        for product in products_in_category:
            categories = clean_tag(product["categories"])
            stores = clean_tag(product["stores"])
            brands = clean_tag(product["brands"])

            try:
                category_index = categories.index(category)
            except ValueError:
                category_index = 0

            filter_categories = categories[category_index:category_index+3]
            product["categories"] = [
                category for category in filter_categories]

            filter_stores = stores[:2]
            product["stores"] = [store for store in filter_stores]

            product["brands"] = brands[0]

            all_categories += filter_categories
            all_stores += filter_stores
            all_brands.append(product["brands"])

            products.append(product)

    clean_categories = clean_duplicate(all_categories)
    clean_brands = clean_duplicate(all_brands)
    clean_stores = clean_duplicate(all_stores)

    Category().insert_query(clean_categories)
    Brand().insert_query(clean_brands)
    Store().insert_query(clean_stores)
    Product().insert_query(products)
    
    

def clean_tag(elmt_with_commas):
    """This function transforms a string of elements separated by commas into a list 

    Arguments:
        elmt_with_commas {string with commas} -- elements separated by commas

    Returns:
        [list] -- elements in a list
    """
    elmt_list = elmt_with_commas.split(",")
    elmt_list = [e.strip() for e in elmt_list]
    return elmt_list


def clean_duplicate(list_of_tags):
    """This function delete duplicates elements in a list

    Arguments:
        list_of_tags {list} -- list with duplicates

    Returns:
        list -- list without duplicates
    """
    clean_list = list(set(list_of_tags))
    return clean_list

if __name__ == "__main__":
    save_data()