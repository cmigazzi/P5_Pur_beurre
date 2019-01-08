import argparse
import records

from settings import CATEGORIES, DB_CONNEXION
from get_data import save_data, create_database
from views import Display
from models import Category, Product
from navigation import Navigation


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--db_init", action="store_true",
                        help="Initializing and populating database")
    return parser.parse_args()


def main():
    args = parse_arguments()

    if args.db_init == True:
        if len(CATEGORIES) > 5:
            print("Il y a plus de 5 catégories, veuillez en enlever dans settings.py")
        elif len(CATEGORIES) < 1:
            print("Veuillez sélectionner au moins une catégorie dans settings.py")
        else:
            print("Création de la base de données...")
            create_database()
            print("Base de données crée ! Chargement des données d'Open Food Facts...")
            save_data()
            print("Installation terminée, vous pouvez utiliser l'application !")

    else:
        # Initialisation
        db_connexion = records.Database(DB_CONNEXION) 
      
        Navigation(db_connexion).active()

        db_connexion.db.close()


if __name__ == "__main__":
    main()
