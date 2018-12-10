import argparse

from settings import CATEGORIES
from sql_queries import create_database
from get_data import save_data

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--db_init", action="store_true", help="Initializing and populating database")
    return parser.parse_args()

def main():
    args = parse_arguments()

    if args.db_init == True:
        if len(CATEGORIES) > 5:
            print("Il y a plus de 5 catégories, veuillez en enlever dans settings.py")
        elif len(CATEGORIES) < 1:
            print("Veuillez sélectionner au moins une catégorie dans settings.py")
        else:   
            print("Creating Database...")
            create_database()
            print("Database created ! Loading data...")
            save_data()
            print("Everything is ready, you can use the app !")

    else:            
        print("""
        ##################################################
        ######             EAT BETTER             ########
        # L'application pour une alimentation plus saine #
        ##################################################

        1 - Quel aliment souhaitez-vous remplacer ?
        2 - Retrouver mes aliments substitués.
        """)            

if __name__ == "__main__":
    main()
