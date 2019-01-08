from models import Category, Product
from views import Display


class Navigation():

    def __init__(self, db_connection):
        self.view = Display()

        self.db = db_connection
        self.category_table = Category(db_connection)
        self.product_table = Product(db_connection)
        self.current_pos = 0
        self.selections = {"category": None,
                           "sub_category": None,
                           "name": None,
                           "brand": None,
                           "nutri_score": None}
        self.active = self.main

    def main(self):
        self.current_pos = 0
        self.view.template_menu(self.current_pos)
        choice = self.view.make_choice(self.current_pos)

        if choice == 3:
            print("A bientôt")
            return False
        elif choice == 2:
            print("under construction")

        elif choice == 1:
            self.categories_options = self.category_table.select_five_main_categories()
            self.active = self.categories

        else:
            print("veuillez entrer un nombre valide")

        return self.active()

    def categories(self):
        self.current_pos = 1
        self.view.template_menu(self.current_pos, self.categories_options)
        choice = self.view.make_choice(self.current_pos)

        if choice == 0:
            self.active = self.main
            return self.active()

        try:
            category_selected = self.categories_options[choice-1]
        except IndexError:
            print(
                "Aucun produit ne correspond à ce numéro, veuillez sélectionner un numéro valide")
        else:
            category_id = self.category_table.select_id_by_name(
                category_selected)

            self.selections["category"] = category_id
            self.sub_categories_options = self.category_table.select_sub_categories(
                self.selections)

            self.active = self.sub_categories

        return self.active()

    def sub_categories(self):
        self.current_pos = 2
        self.view.template_menu(self.current_pos, self.sub_categories_options)
        choice = self.view.make_choice(self.current_pos)

        if choice == 0:
            self.active = self.categories
            return self.active()

        try:
            category_selected = self.sub_categories_options[choice-1]
        except IndexError:
            print(
                "Aucun produit ne correspond à ce numéro, veuillez sélectionner un numéro valide")

        else:
            sub_category_id = self.category_table.select_id_by_name(
                category_selected)

            self.selections["sub_category"] = sub_category_id
            self.products_options = self.product_table.select_product_list_by_category(
                self.selections)
            self.active = self.products

        return self.active()

    def products(self):

        self.current_pos = 3
        self.view.template_menu(self.current_pos, self.products_options)
        choice = self.view.make_choice(self.current_pos)

        if choice == 0:
            self.active = self.sub_categories
            return self.active()

        try:
            product_selected = self.products_options[choice-1]
        except IndexError:
            print(
                "Aucun produit ne correspond à ce numéro, veuillez sélectionner un numéro valide")
        else:
            nutri_score = product_table.get_nutri_score_by_name(
                product_selected)

        return self.active()

    def substitute_proposition():
        pass
