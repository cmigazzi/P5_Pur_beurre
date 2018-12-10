############
# SETTINGS #
############

# DATABASE CONNECTION 
# change the login data to your mysql configuration

DB_USER = "root"
DB_PASSWORD = "root"
DB_HOST = "localhost"
DB_NAME = "eat_better"

# API REQUEST CONFIG
# Choose your categories, maximum 5
CATEGORIES = [
#    "Snacks sucrés",
#    "Produits laitiers",
    "Plats préparés",
#    "Biscuits et gâteaux",
#    "Produits à tartiner",
    "Petit-déjeuners",
    "Desserts",
#    "Epicerie",
    "Surgelés",
    "Viandes"
]

SEARCH_API_URL = "https://fr.openfoodfacts.org/cgi/search.pl"
CATEGORIES_API_URL = "https://fr.openfoodfacts.org/category/"

FIELD_NEEDED = [
    "product_name_fr",
    "categories",
    "generic_name",
    "stores",
    "brands",
    "url",
    "nutrition_grade_fr"
]