# OC - Project 5 - Eat Better by Pur Beurre

# How to start ?

Before using the applictaion, you need to clone this repository, create and activate a virtual environnement, install database schema and get data from Open Food Facts API.

To do that, make sure that Python3, venv and MySql are installed and follow theses steps:

- clone the repo:
    `git clone https://github.com/cmigazzi/P5_Pur_beurre.git`

- install and activate virtual environnement:
    python3 -m venv eat_better_venv

    - for Linux and MacOS user:
        source eat_better_venv\bin\activate
    
    - for Windows user:
        eat_better_venv\Scripts\activate

- install required libs:
    pip install -r requirements.txt

- install database schema and get datas:
    python3 eat_better.py --init-db

This may takes few minutes, so let's take a coffee
    

