import argparse

from settings import CATEGORIES
from get_data import save_data, create_database
from views import Display
from models import Category, Product


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--db_init", action="store_true", help="Initializing and populating database")
    return parser.parse_args()

def main_menu():
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
        view = Display()
        category_table = Category()
        product_table = Product()
        running = True
        options = None
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
                options = category_table.select_sub_categories(category_selected, sub_menu)
                sub_menu += 1

            elif sub_menu == 3:
                category_selected = options[int(choice)-1]
                category_id = category_table.select_id_by_name(category_selected)
                options = product_table.select_product_list_by_category(category_id)



        # main_menu_view()

        # main_menu_state = True
        # while main_menu_state == True:
        #     try:
        #         choice = int(input("Faites votre choix à l'aide des numéros:\n"))
        #     except ValueError:
        #         print("Pour faire votre choix, veuillez saisir un nombre")
        #         continue
        #     if choice == 1:
        #         print("categories")
        #         category_menu()
        #     elif choice == 2:
        #         print("élements déjà substitués")
        #     elif choice == 3:
        #         main_menu_state = False
        #     else:
        #         print(f"Aucune option ne correspond à {choice}")
        #         continue
            
# def category_menu():
#     category_menu_view()
#     category_menu_state = True
#     while category_menu_state == True:
#         try:
#             choice = int(input("Faites votre choix à l'aide des numéros:\n"))
#         except ValueError:
#             print("Pour faire votre choix, veuillez saisir un nombre")
#             continue
#         if choice == 1:
#             print("C1")
#         elif choice == 2:
#             print("C2")
#         elif choice == 3:
#             category_menu_state = False
#         else:
#             print(f"Aucune option ne correspond à {choice}")
#             continue

     
if __name__ == "__main__":
    main_menu()
