"""Application launcher."""

import argparse
import records

from settings import CATEGORIES, DB_CONNEXION
from views import Display
from controller import Navigation


def parse_arguments():
    """Set the CLI argument for database installation."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--db_init", action="store_true",
                        help="Initializing and populating database")
    return parser.parse_args()


def main():
    """Start function of the app."""
    args = parse_arguments()

    if args.db_init is True:
        if len(CATEGORIES) > 5:
            print("Il y a plus de 5 catégories, veuillez en enlever dans settings.py")
        elif len(CATEGORIES) < 1:
            print("Veuillez sélectionner au moins une catégorie dans settings.py")
        else:
            setup()

    else:
        db_connection = records.Database(DB_CONNEXION)
        Navigation(db_connection).active()
        db_connection.db.close()


if __name__ == "__main__":
    main()
