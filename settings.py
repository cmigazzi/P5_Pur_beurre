"""Set the application."""

# *******************************************************
#           DATABASE CONNECTION
# change the login data to your mysql configuration

DB_USER = "root"
DB_PASSWORD = "root"
DB_HOST = "localhost"
DB_PORT = "3306"
DB_NAME = "eat_better"

DB_CONNEXION = (f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}"
                f"@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4")


# *******************************************************
#           API REQUEST CONFIG
# Choose your categories, maximum 5
# Uncomment categories to get them
CATEGORIES = [
    # "Céréales et pommes de terre",
    "Fromages",
    "Biscuits et gâteaux",
    "Produits à tartiner sucrés",
    "Petit-déjeuners",
    "Desserts",
    # "Conserves"
]

SEARCH_API_URL = "https://fr.openfoodfacts.org/cgi/search.pl"

FIELD_NEEDED = [
    "product_name_fr",
    "categories",
    "generic_name",
    "stores",
    "brands",
    "url",
    "nutrition_grade_fr"
]
