################################################################################
#           This module contains all the views of the program                  #
################################################################################


class Display():
    def __init__(self):
        print("##################################################",
              "######             EAT BETTER             ########",
              "# L'application pour une alimentation plus saine #",
              "##################################################",
              "\n",
              sep="\n")
        self.main_menu_options = [
            "Quel aliment souhaitez-vous remplacer ?", "Retrouver mes aliments substitués.", "Quitter"]

    def template_menu(self, sub_menu, options=None):
        if options == None:
            self.options = self.main_menu_options
        else:
            self.options = options

        if sub_menu == 0:
            # main menu
            print("Faites votre choix à l'aide des numéros")
        elif sub_menu == 1:
            # select category
            print("\nSélectionner la catégorie (taper 0 pour revenir au menu principal):")
        elif sub_menu == 2:
            # select sub category
            print(
                "\nSélectionner la sous-catégorie (taper 0 pour revenir à la liste des catégories):")
        elif sub_menu == 3:
            # select product
            print(
                "\nSélectionner l'aliment (taper 0 pour revenir à la liste des sous-catégories):")

        for (number, option) in enumerate(self.options):
            if isinstance(option, tuple):
                print(f"{number+1} - '{option[0]}' de la marque '{option[1]}'")
            else:
                print(f"{number+1} - {option}")
        if sub_menu != 0:
            print("0 - Retour")

    def make_choice(self, sub_menu):
        make_choice = True
        while make_choice == True:

            try:
                choice = int(input("Saisissez un numéro: \n"))
            except ValueError:
                print("Pour faire votre choix, veuillez saisir un nombre valide")
                continue
            return choice


