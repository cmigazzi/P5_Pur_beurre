################################################################################
#           This module contains all the functions to get data from            #
#                            OpenFoodFacts API                                 #
################################################################################

import requests

from settings import CATEGORIES, SEARCH_API_URL, FIELD_NEEDED
from sql_queries import create_database, save_data_API, save_products


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
                category for category in enumerate(filter_categories)]

            filter_stores = stores[:2]
            product["stores"] = [store for store in enumerate(filter_stores)]

            product["brands"] = brands[0]

            all_categories += filter_categories
            all_stores += filter_stores
            all_brands.append(product["brands"])

            products.append(product)

    clean_categories = clean_duplicate(all_categories)
    clean_brands = clean_duplicate(all_brands)
    clean_stores = clean_duplicate(all_stores)

    save_data_API(clean_categories, clean_brands, clean_stores)
    save_products(products)
    


def clean_tag(elmt_with_commas):
    """This function transforms a string of elements separated by commas into a list 

    Arguments:
        elmt_with_commas {string with commas} -- elements separated by commas

    Returns:
        [list] -- elements in a list
    """
    elmt_list = elmt_with_commas.split(",")
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