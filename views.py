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
        self. options = None

    def template_menu(self, options):
        if options == None:
            self.options = self.main_menu_options
        else:
            self.options = options
        for (number, option) in enumerate(self.options):
            if isinstance(option, tuple):
                print(f"{number} - '{option[0]}' de la marque '{option[1]}'")
            else:
                print(f"{number+1} - {option}")

    def make_choice(self):
        make_choice = True
        while make_choice == True:
            try:
                choice = int(
                    input("Faites votre choix à l'aide des numéros:\n"))
            except ValueError:
                print("Pour faire votre choix, veuillez saisir un nombre valide")
                continue
            return choice
