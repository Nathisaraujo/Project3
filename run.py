import os
import gspread
from google.oauth2.service_account import Credentials
from random import randint
from prettytable import PrettyTable

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('family_favorites')

recipes = SHEET.worksheet('recipes')

def initial_page():
    """

    Ask what the user wants to do

    """
    os.system('clear')

    print("\nWhat would you like to do? \n")
    print("1. Check a recipe")
    print("2. Add a new one\n")
    
    while True:
        user_option = input("Enter your answer here:").strip()
        if user_option == "1":
            print("Ok! Let's check what we have here!\n")
            check_recipe()
        elif user_option == "2":
            print("HMMMM! New recipe coming!\n")
            add_recipe()
        else:
            print('Please, enter 1 or 2 to continue.')
            continue

def search_recipe_by_name(recipe_name):    
    recipes = []
    all_rows = SHEET.worksheet("recipes").get_all_values()
    for row in all_rows:
        if recipe_name.lower() in row[0].lower(): 
            recipes.append(row)
    return recipes

def check_recipe():
    os.system('clear')

    print("Would you like a specific recipe or a suggestion? \n")
    print("1. View all recipes")
    print("2. Suggestion Recipe")
    print("3. Specific Recipe\n")
    print("Enter EXIT to go back to main menu.")

    while True:
        user_option = input("Enter your answer here:").strip().lower()
        if user_option == "1":
            headers = ["Name", "Ingredients", "How to make it", "Creator's Name", "Who's Favorite"]

            all_recipes = SHEET.worksheet("recipes").get_all_values()

            tables = PrettyTable()
            tables.field_names = headers
            tables.max_width = 30
            tables.align = "l"

            for row in all_recipes:
                tables.add_row(row)
            print(tables)

            print("1. Main menu")
            print("2. Exit program")
            user_option = input("Enter here your option:").strip().lower()
            while True:
                if user_option == "1":
                    main()
                elif user_option == "2":
                    exit_program()
        elif user_option == "2":
            recipe_suggestion()
        elif user_option == "3":
            print("Ok! Enter the recipe name here and we're going to see if we have it!\n")
            recipe_name = input("Check Recipe:")
            found_recipes = search_recipe_by_name(recipe_name)

            headers = ["Name", "Ingredients", "How to make it", "Creator's Name", "Who's Favorite"]

            if found_recipes:
                print(f"Found {len(found_recipes)} matching recipes:")
                recipe_row = found_recipes[0]
                print("\nRecipe Details:")

                tables = PrettyTable()
                tables.field_names = headers
                tables.max_width = 30
                tables.align = "l"

                for row in found_recipes:
                    tables.add_row(row)
                print(tables)

                print("1. Main menu")
                print("2. Exit program")
                user_option = input("Enter here your option:").strip().lower()
                while True:
                    if user_option == "1":
                        main()
                    elif user_option == "2":
                        exit_program()       
            else:
                print("No recipes found with that name.")
        elif user_option == "exit":
            os.system('clear')
            main()
        else:
            print('Please, enter 1 or 2 to continue.')
            print("Or you can enter 'exit' to go back to the initial menu.")
            continue

def recipe_suggestion():
    os.system('clear')

    print("Ok! I think you you'll like this one:\n")
    all_recipes = SHEET.worksheet("recipes").get_all_values()         
        
    if len(all_recipes) > 1:
        headers = ["Name", "Ingredients", "How to make it", "Creator's Name", "Who's Favorite"]
        random_index = randint(1, len(all_recipes)-1)  
        random_recipe = all_recipes[random_index - 1]
                
        tables = PrettyTable()
        tables.field_names = headers
        tables.max_width = 30
        tables.align = "l"

        tables.add_row(random_recipe)
        print(tables)

        print("Enter what you want to do next:")
        print("NEW - another recommendation.")
        print("MENU - go back to main menu.")
        print("EXIT - exit the program.")

        while True:
            user_option = input("Enter your answer here:").strip().lower()
            if user_option == "new":
                os.system('clear')
                recipe_suggestion()
            elif user_option == "menu":
                
                os.system('clear')
                main()
            elif user_option == "exit":
                exit_program()
            else:
                print('Please, enter a valid option to continue.')
                continue


def editing():
    print("""
        What would you like to edit?\n 
        1. First name\n 
        2. Recipe\n 
        3. Ingredients\n
        4. Preparation\n 
        5. Recipe favorite\n""")
    edit_recipe = input("Enter your option here:")
    print("You can enter EXIT to go back to main menu")
    if edit_recipe == "1":
        print(f'First name: {user_details}')
        global name_update
        name_update = input("New name:")
        print(f"""
                Name: {name_update}
                Recipe name: {recipe_name}
                Ingredients List: {ingredients_list}
                Recipe Preparation: {recipe_preparation}
                Recipe Favorite: {recipe_favorite}
                """)

        print("\nPlease, make sure you added all information right.")
        print("1. Confirm")
        print("2. Edit")

        while True:
            user_option = input("Enter your answer here:").strip().lower()
                    
            if user_option == "confirm":
                print("Ok! Thank you so much for your contribution!\n Updating...")
                time.sleep(0.05)
                data_list = (name_update, recipe_name, ingredients_list, recipe_preparation, recipe_favorite)
                recipes.append_row(data_list)
                print("Update completed.")

                print("1. Main menu")
                print("2. Exit program")
                user_option = input("Enter here your option:").strip().lower()
                while True:
                    if user_option == "1":
                        main()
                    elif user_option == "2":
                        exit_program()
            elif user_option == "edit":
                editing()
            elif user_option == "exit":
                main()
            else:
                print('Please, enter a valid option to continue.')
                print("Or you can enter 'exit' to go back to the initial menu.")
    elif edit_recipe == "2":
        print(f'Recipe: {recipe_name}')
        global recipe_update
        recipe_update = input("New recipe name:")
        print(f"""
                Name: {name_update}
                Recipe name: {recipe_update}
                Ingredients List: {ingredients_list}
                Recipe Preparation: {recipe_preparation}
                Recipe Favorite: {recipe_favorite}
                """)

        print("\nPlease, make sure you added all information right.")
        print("Confirm")
        print("Edit")

        while True:
            user_option = input("Enter your answer here:").strip().lower()
                    
            if user_option == "confirm":
                print("Ok! Thank you so much for your contribution!\n Updating...")
                time.sleep(0.05)
                data_list = (name_update, recipe_update, ingredients_list, recipe_preparation, recipe_favorite)
                recipes.append_row(data_list)
                print("Update completed.")

                print("1. Main menu")
                print("2. Exit program")
                user_option = input("Enter here your option:").strip().lower()
                while True:
                    if user_option == "1":
                        main()
                    elif user_option == "2":
                        exit_program()
            elif user_option == "edit":
                editing()
            elif user_option == "exit":
                main()
            else:
                print('Please, enter a valid option to continue.')
                print("Or you can enter 'exit' to go back to the initial menu.")
    elif edit_recipe == "3":
        print(f'Ingredients List: {ingredients_list}')
        global ingredients_update
        ingredients_update = input("New ingredients list:")
        print(f"""
                Name: {name_update}
                Recipe name: {recipe_update}
                Ingredients List: {ingredients_update}
                Recipe Preparation: {recipe_preparation}
                Recipe Favorite: {recipe_favorite}
                """)

        print("\nPlease, make sure you added all information right.")
        print("Confirm")
        print("Edit")

        while True:
            user_option = input("Enter your answer here:").strip().lower()
                    
            if user_option == "confirm":
                print("Ok! Thank you so much for your contribution!\n Updating...")
                time.sleep(0.05)
                data_list = (name_update, recipe_update, ingredients_update, recipe_preparation, recipe_favorite)
                recipes.append_row(data_list)
                print("Update completed.")
                print("1. Main menu")
                print("2. Exit program")
                user_option = input("Enter here your option:").strip().lower()
                while True:
                    if user_option == "1":
                        main()
                    elif user_option == "2":
                        exit_program()
            elif user_option == "edit":
                editing()
            elif user_option == "exit":
                main()
            else:
                print('Please, enter a valid option to continue.')
                print("Or you can enter 'exit' to go back to the initial menu.")
    elif edit_recipe == "4":
        print(f'Recipe preparation: {recipe_preparation}')
        global preparation_update
        preparation_update = input("New recipe preparation:")
        print(f"""
                Name: {name_update}
                Recipe name: {recipe_update}
                Ingredients List: {ingredients_update}
                Recipe Preparation: {preparation_update}
                Recipe Favorite: {recipe_favorite}
                """)

        print("\nPlease, make sure you added all information right.")
        print("Confirm")
        print("Edit")

        while True:
            user_option = input("Enter your answer here:").strip().lower()
                    
            if user_option == "confirm":
                print("Ok! Thank you so much for your contribution!\n Updating...")
                time.sleep(0.05)
                data_list = (name_update, recipe_update, ingredients_update, preparation_update, recipe_favorite)
                recipes.append_row(data_list)
                print("Update completed.")
                print("1. Main menu")
                print("2. Exit program")
                user_option = input("Enter here your option:").strip().lower()
                while True:
                    if user_option == "1":
                        main()
                    elif user_option == "2":
                        exit_program()
            elif user_option == "edit":
                editing()
            elif user_option == "exit":
                main()
            else:
                print('Please, enter a valid option to continue.')
                print("Or you can enter 'exit' to go back to the initial menu.")
    elif edit_recipe == "5":
        print(f'Favorite by: {recipe_favorite}')
        global favorite_update
        favorite_update = input("Now favorite by:")
        print(f"""
                Name: {name_update}
                Recipe name: {recipe_update}
                Ingredients List: {ingredients_update}
                Recipe Preparation: {preparation_update}
                Recipe Favorite: {favorite_update}
                """)

        print("\nPlease, make sure you added all information right.")
        print("Confirm")
        print("Edit")

        while True:
            user_option = input("Enter your answer here:").strip().lower()
                    
            if user_option == "confirm":
                print("Ok! Thank you so much for your contribution!\n Updating...")
                time.sleep(0.05)
                data_list = (name_update, recipe_update, ingredients_update, preparation_update, favorite_update)
                recipes.append_row(data_list)
                print("1. Main menu")
                print("2. Exit program")
                user_option = input("Enter here your option:").strip().lower()
                while True:
                    if user_option == "1":
                        main()
                    elif user_option == "2":
                        exit_program()
                print("Update completed.")
            elif user_option == "edit":
                editing()
            elif user_option == "exit":
                main()
            else:
                print('Please, enter a valid option to continue.')
                print("Or you can enter 'exit' to go back to the initial menu.")

def add_recipe():   
    os.system('clear')

    print("Ok! Then we'll need you to give us some information...")

    global user_details
    user_details = input("First name:")
    global recipe_name 
    recipe_name = input("Name of the recipe:")
    global ingredients_list
    ingredients_list = input("What are the ingredients?")
    global recipe_preparation
    recipe_preparation = input("How we prepare the recipe?")
    global recipe_favorite
    recipe_favorite = input("This recipe is who's favorite?")

    print(f"""
        Your name: {user_details}
        Recipe name: {recipe_name}
        Ingredients List: {ingredients_list}
        Recipe Preparation: {recipe_preparation}
        Recipe Favorite: {recipe_favorite}
        """)
     
    print("Please, make sure you added all information right.\n")
    print("1. Confirm")
    print("2. Edit")
    print("You can enter EXIT to go back to main menu")

    while True:
        user_option = input("Enter your answer here:").strip().lower()
        if user_option == "1": 
            data_list = (user_details, recipe_name, ingredients_list, recipe_preparation, recipe_favorite)
            recipes.append_row(data_list)
            print("Recipe added.")

            print("1. Main menu")
            print("2. Exit program")
            user_option = input("Enter here your option:").strip().lower()
            while True:
                if user_option == "1":
                    main()
                elif user_option == "2":
                    exit_program()        
        elif user_option == "2":
            editing()
        elif user_option == "exit":
            os.system('clear')
            main()
        else:
            print('Please, enter a valid option to continue.')
            print("Or you can enter EXIT to go back to the initial menu.")

def exit_program():
    print("Exiting the program...")
    sys.exit(0)

def main():
    """
    run all program functions

    """
    print(" WELCOME TO\n")
    print("  _____               _ _                  ")
    print(" |  ___|_ _ _ __ ___ (_) |_   _            ")
    print(" | |_ / _` | '_ ` _ \| | | | | |           ")
    print(" |  _| (_| | | | | | | | | |_| |           ")
    print(" |_|  \__,_|_| |_| |_|_|_|\__, |           ")
    print("                          |___/            ")
    print("  _____                     _ _            ")
    print(" |  ___|_ ___   _____  _ __(_) |_ ___  ___ ")
    print(" | |_ / _` \ \ / / _ \| '__| | __/ _ \/ __|")
    print(" |  _| (_| |\ V / (_) | |  | | ||  __/\__ \\")
    print(" |_|  \__,_| \_/ \___/|_|  |_|\__\___||___/")

    print("""\nThis a heartfelt family recipe book where
    we can share are favorite recipes!
    This is a gift to our future generation who will
    be able to prepare the most special recipes.\n
    """)
    input("Press Enter to continue...")
    initial_page()
                                           
main()