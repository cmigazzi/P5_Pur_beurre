"""This module contains all the views of the program."""


class Display():
    """Represent the User Interface."""

    def __init__(self):
        """Print intro."""
        print("##################################################",
              "######             EAT BETTER             ########",
              "# L'application pour une alimentation plus saine #",
              "##################################################",
              "\n",
              sep="\n")
        self.main_menu_options = [
            "Quel aliment souhaitez-vous remplacer ?", "Retrouver mes aliments substitués.", "Quitter"]

    def template_menu(self, menu_tree, options=None):
        """Display list.

        Arguments:
            menu_tree {int} -- place in navigation tree

        Keyword Arguments:
            options {list} -- list of options to display (default: {None})
        """
        if options is None:
            self.options = self.main_menu_options
        else:
            self.options = options

        if menu_tree == 0:
            # main menu
            print("Faites votre choix à l'aide des numéros")
        elif menu_tree == 1:
            # select category
            print("\nSélectionner la catégorie (taper 0 pour revenir au menu principal):")
        elif menu_tree == 2:
            # select sub category
            print(
                "\nSélectionner la sous-catégorie (taper 0 pour revenir à la liste des catégories):")
        elif menu_tree == 3:
            # select product
            print(
                "\nSélectionner l'aliment (taper 0 pour revenir à la liste des sous-catégories):")

        for (number, option) in enumerate(self.options):
            if isinstance(option, tuple):
                print(f"{number+1} - '{option[0]}' de la marque '{option[1]}'")
            else:
                print(f"{number+1} - {option}")
        if menu_tree != 0:
            print("0 - Retour")

    def substitute_proposition(self, selections, substitute):
        """Display the substitute proposition.

        Arguments:
            selections {dict} -- selections made by the user
            substitute {list} -- substitute product property

        """
        print(f"\nNous vous proposons de remplacer le produit {selections['name']} de la marque {selections['brand_name']} par: \n",
              f"{ substitute.name } de la marque { substitute.brand_name}. \n",
              f"Description: {substitute.description}",
              f"Vous pourrez le trouver chez {substitute.store_0} ou {substitute.store_1}.\n",
              "Pour plus d'informations sur le produit, cliquez ici:",
              f"{substitute.url}\n",
              "Souhaitez-vous enregistrer cette substitution de produit ?",
              "1 - Oui",
              "2 - Non (retour au menu principal)",
              sep="\n")

    def substitutes(self, substitutions):
        """Display all the substitutions saved.

        Arguments:
            substitutions {list} -- substitutions
        """
        for products in substitutions:
            print(f"Le produit {products.original} de la marque {products.original_brand}",
                  "a été substitué par: ",
                  f"{products.substitute} de la marque {products.substitute_brand}",
                  f"Pour plus de détails: {products.url}",
                  sep="\n")

    def make_choice(self):
        """Validate and save choice of the user."""
        make_choice = True
        while make_choice is True:

            try:
                choice = int(input("Saisissez un numéro: \n"))
            except ValueError:
                print("Pour faire votre choix, veuillez saisir un nombre valide")
                continue
            return choice
