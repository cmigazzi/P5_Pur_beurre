"""This module control the flow of the application."""

import random

from models import Category, Product, Brand, Substitution
from views import Display


class Navigation():
    """This class represents the app navigation tree.

    Arguments:
        db_connetcion {<class records.Database>} -- database connection

    Attributes:
        db {<class records.Database>} -- database connection
        view {<class views.Display>} -- manage the user interface
        category_table {<class models.Category>} --
                                    manage queries on category table
        brand_table {<class models.Brand>} -- manage queries on brand table
        product_table {<class models.Product>} --
                                    manage queries on product table
        substitution_table {<class models.Substitution>} --
                                    manage queries on substitution table
        current_pos {int} -- track where the user is in the navigation tree
        selections {dict} -- keep all the choices of the user
        active {func} -- active method

    """

    def __init__(self, db_connection):
        """Please see help(Navigation) for more details."""
        self.view = Display()

        self.db = db_connection
        self.category_table = Category(db_connection)
        self.product_table = Product(db_connection)
        self.brand_table = Brand(db_connection)
        self.substitution_table = Substitution(db_connection)
        self.current_pos = 0
        self.selections = {"category": None,
                           "sub_category": None,
                           "name": None,
                           "brand": None,
                           "brand_name": None,
                           "nutri_score": None,
                           "substitute": None,
                           "substitute_brand": None}
        self.active = self.main

    def main(self):
        """Control the main menu.

        Returns:
            func|False -- Call another method or return False to quit.

        """
        self.current_pos = 0
        self.view.template_menu(self.current_pos)
        choice = self.view.make_choice()

        if choice == 3:
            print("A bientôt")
            return False
        elif choice == 2:
            self.active = self.all_substitutions

        elif choice == 1:
            self.categories_options = \
                self.category_table.select_five_main_categories()
            self.active = self.categories

        else:
            print("veuillez entrer un nombre valide")

        return self.active()

    def categories(self):
        """Control the categories menu.

        Returns:
            func -- Call another method

        """
        self.current_pos = 1
        self.view.template_menu(self.current_pos, self.categories_options)
        choice = self.view.make_choice()

        if choice == 0:
            self.active = self.main
            return self.active()

        try:
            category_selected = self.categories_options[choice-1]
        except IndexError:
            print(
                "Aucun choix ne correspond à ce numéro,"
                "veuillez sélectionner un numéro valide")
        else:
            category_id = self.category_table.select_id_by_name(
                category_selected)

            self.selections["category"] = category_id
            self.sub_categories_options = \
                self.category_table.select_sub_categories(
                    self.selections)

            self.active = self.sub_categories

        return self.active()

    def sub_categories(self):
        """Control the subcategories menu.

        Returns:
            func -- Call another method

        """
        self.current_pos = 2
        self.view.template_menu(self.current_pos, self.sub_categories_options)
        choice = self.view.make_choice()

        if choice == 0:
            self.active = self.categories
            return self.active()

        try:
            category_selected = self.sub_categories_options[choice-1]
        except IndexError:
            print(
                "Aucun choix ne correspond à ce numéro,"
                "veuillez sélectionner un numéro valide")

        else:
            sub_category_id = self.category_table.select_id_by_name(
                category_selected)

            self.selections["sub_category"] = sub_category_id
            self.products_options = \
                self.product_table.select_product_list_by_category(
                    self.selections)
            self.active = self.products

        return self.active()

    def products(self):
        """Control the products menu.

        Returns:
            func -- Call another method

        """
        self.current_pos = 3
        self.view.template_menu(self.current_pos, self.products_options)
        choice = self.view.make_choice()

        if choice == 0:
            self.active = self.sub_categories
            return self.active()

        try:
            product_selected = self.products_options[choice-1]
        except IndexError:
            print(
                "Aucun choix ne correspond à ce numéro,"
                "veuillez sélectionner un numéro valide")
        else:
            self.selections["name"] = product_selected[0]
            self.selections["brand_name"] = product_selected[1]
            self.selections["brand"] = self.brand_table.select_id_by_name(
                product_selected[1])
            self.selections["nutri_score"] = \
                self.product_table.get_nutri_score_by_name(
                    self.selections)

            if self.selections["nutri_score"] == 'a':
                print("Cet aliment est déjà sain, c'est super ! Bon appétit")
            else:
                better_products = self.product_table.get_better_products(
                    self.selections)

                if len(better_products) == 0:
                    print("Aucun aliment n'est plus sain "
                          "dans la même catégorie !")
                else:
                    self.substitute = random.choice(better_products)
                    self.selections["substitute"] = self.substitute.name
                    self.selections["substitute_brand"] = self.substitute.brand
                    self.active = self.substitute_proposition

        return self.active()

    def substitute_proposition(self):
        """Control the substitute proposition menu.

        Returns:
            func -- Call another method

        """
        self.current_pos = 4
        self.view.substitute_proposition(self.selections, self.substitute)
        choice = self.view.make_choice()

        if choice == 1:
            try:
                self.substitution_table.insert_query(self.selections)
            except Exception as e:
                print("Erreur dans l'enregistrement")
                # print(e)
            else:
                print("Enregitrement effectué avec succès !")
        elif choice != 2:
            print(
                "Aucun choix ne correspond à ce numéro,"
                "veuillez sélectionner un numéro valide")

        self.selections = {k: None for k in self.selections.keys()}
        self.active = self.main

        return self.active()

    def all_substitutions(self):
        """Get and display all substitutions saved."""
        self.current_pos = 5
        results = self.substitution_table.get_all()
        self.view.substitutes(results)
        self.active = self.main

        return self.active()
