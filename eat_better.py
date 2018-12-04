import requests

from settings import CATEGORIES, SEARCH_API_URL, FIELD_NEEDED

def main():
    print("""
    ##################################################
    ######             EAT BETTER             ########
    # L'application pour une alimentation plus saine #
    ##################################################

    1 - Quel aliment souhaitez-vous remplacer ?
    2 - Retrouver mes aliments substitués.
    """)

def get_api_data():
    """This function requests the OpenFoodFact API to get data
    
    Returns:
        list -- list od dictionnary that represents a product
    """

    products = []

    for category in CATEGORIES:
        url = SEARCH_API_URL + f"?search_terms={category}&search_tag=category&page_size=250&json=1"
        json_response = requests.get(url).json()
        products_list = json_response["products"]

        for complete_product in products_list:
            clean_product = {k:v for k,v in complete_product.items() if k in FIELD_NEEDED}
            products.append(clean_product)

    print(products, len(products), sep="\n")

    return products




if __name__ == "__main__":
    get_api_data()