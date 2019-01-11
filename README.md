# OC - Project 5 - Eat Better by Pur Beurre

# How to start ?

Before using the applictaion, you need to clone this repository, create and activate a virtual environnement, install database schema and get data from Open Food Facts API.

To do that, make sure that Python3, venv, git and MySql are installed and follow theses steps in your prompt in target folder:

- clone the repo: `git clone https://github.com/cmigazzi/P5_Pur_beurre.git`

- create virtual environnement (venv): `python3 -m venv eat_better_venv`

- active the virtual environment:

    - for Linux and MacOS user, activate venv: `source eat_better_venv\bin\activate`
    
    - for Windows user, activate venv: `eat_better_venv\Scripts\activate`

- install required libs: `pip install -r requirements.txt`

- If not exist, create a new mysql user with creation privileges

- Go to settings.py to enter your mysql username, password, host, port and db_name at lines 7-11

- install database schema and get datas: `python eat_better.py --init-db`
This may takes few minutes, so let's take a coffee

- If everything goes right, you can launch the application: `python eat_better.py`

## Select a product you want to replace

On main menu, enter 1.
To select a product, you have first to select a category and a subcategory with numeric characters.
When you've found the product, the application displays a substitute. 
If you want, you can save the substitution for later.

## Retrive a substitution

On main menu, enter 2 and the application displays the list of all substitution
    

