"""Install of the Database and populate it."""

import records

from settings import DB_CONNEXION, CATEGORIES
from get_data import Api, ProductFromApiToDatabase, DataFromApiToDatabase
from database import (SchemaCreator, CategoryCreator,
                      StoreCreator, BrandCreator,
                      ProductCreator, SubstitutionCreator)


def setup():
    """Install of the Database and populate it."""
    print("Création de la base de données...")
    SchemaCreator().create()
    db_connection = records.Database(DB_CONNEXION)
    CategoryCreator(db_connection).create()
    StoreCreator(db_connection).create()
    BrandCreator(db_connection).create()
    ProductCreator(db_connection).create()
    SubstitutionCreator(db_connection).create()
    print("Base de données crée ! Chargement des données d'Open Food Facts...")

    api_response = Api().call()
    categories = DataFromApiToDatabase(db_connection, "Category")
    stores = DataFromApiToDatabase(db_connection, "Store")
    brands = DataFromApiToDatabase(db_connection, "Brand")
    products = DataFromApiToDatabase(db_connection, "Product")

    for category in CATEGORIES:
        for product in api_response:
            product = ProductFromApiToDatabase(
                product, category, db_connection)
            if product.validate() is False:
                continue
            product.clean()

            categories + product.categories
            stores + product.stores
            brands.append(product.brand)
            products.append(product.fields)

    categories.clean_duplicate()
    stores.clean_duplicate()
    brands.clean_duplicate()

    categories.save()
    stores.save()
    brands.save()
    products.save()

    db_connection.close()

    print("Installation terminée, vous pouvez utiliser l'application !")
