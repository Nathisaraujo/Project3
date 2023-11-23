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
    os.system('cls')

    print("Would you like a specific recipe or a suggestion? \n")
    print("1. View all recipes")
    print("2. Suggestion Recipe")
    print("3. Specific Recipe\n")
    print("Enter EXIT to go back to main menu.")

    while True:
        user_option = input("Enter your answer here:").strip()
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
            else:
                print("No recipes found with that name.")
        elif user_option == "exit":
            os.system('cls')
            initial_page()
        else:
            print('Please, enter 1 or 2 to continue.')
            print("Or you can enter 'exit' to go back to the initial menu.")
            continue

def recipe_suggestion():
    import os
    os.system('cls')

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

    print("Are you happy with this one or should we recommend another one?")
    print("Enter [new] for another recommendation")
    print("Enter EXIT to go back to main menu.")

    while True:
        user_option = input("Enter your answer here:")
        if user_option == "new":
            import os
            os.system('cls')
            recipe_suggestion()
        elif user_option == "exit":
            import os
            os.system('cls')
            initial_page()
        else:
            print('Please, enter a valid option to continue.')
            continue

def update_table():
    data_list = (user_details, recipe_name, ingredients_list, recipe_preparation, recipe_type)
    recipes.append_row(data_list)
    print("updated completed.")

def editing():
                print("What would you like to edit? \n 1. Name and surname \n 2. recipe's name\n 3.Ingredients\n 4.Recipe type\n 5. Recipe favorite")
                edit_recipe = input("Enter your option here:")
                if edit_recipe == "1":
                    print('Recipe name: {recipe_name}')
                    new_update = input("New recipe name:")
                    # update_cell = SHEET.worksheet("recipes").update('B2', "{new_update}")
                    print(f"""
                        Recipe name: {new_update}
                        Ingredients List: {ingredients_list}
                        Recipe Preparation: {recipe_preparation}
                        Recipe Type: {recipe_type}
                        Recipe Favorite: {recipe_favorite}
                        """)

                    print("Please, make sure you added all information right.\n")
                    print("1. Confirm")
                    print("2. Edit")

                    user_option = input("Enter your answer here:").strip()
                    
                    if user_option == "1":
                        print("thank you")
                        data_list = (new_update, recipe_name, ingredients_list, recipe_preparation, recipe_type)
                        recipes.append_row(data_list)
                        print("updated completed.")
                    elif user_option == "2":
                        editing()
                    else:
                        print('Please, enter a valid option to continue.')
                        print("Or you can enter 'exit' to go back to the initial menu.")
                        # continue
                elif edit_recipe == "2":
                    print("option working")
                elif edit_recipe == "3":
                    print("option working")
                elif edit_recipe == "4":
                    print("option working")
                elif edit_recipe == "5":
                    print("option working")
                
                    print("Ok! Thank you so much for your contribution!\n")

def add_recipe():
    import os
    os.system('cls')

    print("Ok! Then we'll need you to give us some information...")

    global user_details
    user_details = input("Name and Surname:")
    global recipe_name 
    recipe_name = input("Name of the recipe:")
    global ingredients_list
    ingredients_list = input("What are the ingredients?")
    global recipe_preparation
    recipe_preparation = input("How we prepare the recipe?")
    global recipe_type #IT HAS TO BE SAVOURY OR SWEET ONLY
    recipe_type = input("Is it savoury or sweet?")
    global recipe_favorite
    recipe_favorite = input("This recipe is who's favorite?")

    print(f"""
        Your name: {user_details}
        Recipe name: {recipe_name}
        Ingredients List: {ingredients_list}
        Recipe Preparation: {recipe_preparation}
        Recipe Type: {recipe_type}
        Recipe Favorite: {recipe_favorite}
        """)
     
    print("Please, make sure you added all information right.\n")
    print("1. Confirm")
    print("2. Edit")

    while True:
        user_option = input("Enter your answer here:").strip()
        if user_option == "1": 
            update_table()        
        elif user_option == "2":
            editing()
        elif user_option == "exit":
            import os
            os.system('cls')
            initial_page()
        else:
            print('Please, enter a valid option to continue.')
            print("Or you can enter 'exit' to go back to the initial menu.")
                    # continue

def main():
    """
    run all program functions
    """
    initial_page()

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
                                           
main()