import argparse

from settings import CATEGORIES
from get_data import save_data, create_database
from views import Display
from models import Category, Product


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
        view = Display()
        category_table = Category()
        product_table = Product()
        running = True
        options = None
        categories_selected = {"category_0": None,
                               "category_1": None, "category_2": None}
        sub_menu = 0

        while running == True:
            view.template_menu(options)
            choice = view.make_choice()

            if view.options == view.main_menu_options:
                if choice == 3:
                    print("A bientôt")
                    running = False
                elif choice == 1:
                    options = category_table.select_five_main_categories()
                    sub_menu += 1

            elif sub_menu == 1 or sub_menu == 2:
                print("sub_menu:", sub_menu)
                category_selected = options[int(choice)-1]
                category_id = category_table.select_id_by_name(category_selected)
                if sub_menu == 1:
                    categories_selected["category_0"] = category_id
                elif sub_menu == 2:
                    categories_selected["category_1"] = category_id
                print(categories_selected)
                options = category_table.select_sub_categories(
                    categories_selected, sub_menu)
                sub_menu += 1

            elif sub_menu == 3:
                print("sub_menu:", sub_menu)
                category_selected = options[int(choice)-1]
                category_id = category_table.select_id_by_name(
                    category_selected)
                categories_selected["category_2"] = category_id
                print(categories_selected)
                options = product_table.select_product_list_by_category(
                    categories_selected)


if __name__ == "__main__":
    main()
