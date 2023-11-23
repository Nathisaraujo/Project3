import os
import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint
from tabulate import tabulate
from random import randint


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
    print("3. test\n")
    
    while True:
        user_option = input("Enter your answer here:").strip()
        if user_option == "1":
            print("Ok! Let's do it!\n")
            check_recipe()
        elif user_option == "2":
            add_recipe()
        elif user_option == "3":
            recipe_suggestion()
        else:
            print('Please, enter 1 or 2 to continue.')
            continue

def search_recipe_by_name(recipe_name):
     
    recipes = []
    all_rows = SHEET.worksheet("recipes").get_all_values()
    for row in all_rows:
        if recipe_name.lower() in row[1].lower(): 
            recipes.append(row)
    return recipes

def check_recipe():
    os.system('cls')

    print("Would you like a specific recipe or a suggestion? \n")
    print("1. View all recipes")
    print("2. Specific Recipe")

    while True:
        user_option = input("Enter your answer here:").strip()
        if user_option == "1":
            all_recipes = SHEET.worksheet("recipes").get_all_values()
            pprint(tabulate(all_recipes))

        elif user_option == "2":
            print("Ok! Enter the recipe name here and we're going to see if we have it!\n")
            recipe_name = input("Check Recipe:")
            found_recipes = search_recipe_by_name(recipe_name)

            headers = ["Type", "Name", "Ingredients", "How to make it", "Creator's Name", "Who's Favorite"]

            if found_recipes:
                print(f"Found {len(found_recipes)} matching recipes:")
                recipe_row = found_recipes[0]
                print("\nRecipe Details:")
                recipe_table = tabulate([recipe_row], headers=headers, tablefmt="pretty")
                print(recipe_table)          
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

    print("Would you like a savoury or a sweet recipe?\n")
    print("1. Savoury")
    print("2. Sweet")
    print("3. I don't know, give me a light!")
    print("4. Back to previous menu")
    print("Enter 'exit' to go to initial menu\n")

    while True:
        user_option = input("Enter your answer here:").strip()
        if user_option == "1":
            recipes = SHEET.worksheet("recipes").get_all_values()
            for row in recipes:
                if user_option in recipes:
                    print("working")
            # print("Ok! Our today suggestion is:\n")
            # recipes = SHEET.worksheet("recipes").row_values()
            # print(random.choice(recipes))
        elif user_option == "2":
            all_recipes = SHEET.worksheet("recipes").get_all_values()
            print("Ok! Today will have this for desert:\n")
            
            if len(all_recipes) > 1:
                
                random_index = randint(1, len(all_recipes)-1)  
                random_recipe = all_recipes[random_index - 1]
                

                headers = ["Type", "Name", "Ingredients", "How to make it", "Creator's Name", "Who's Favorite"]
                random_recipe_table = tabulate([random_recipe], headers=headers, tablefmt="pretty")
                print(random_recipe_table)
            #put random sweet recipe
        elif user_option == "3":
            print("Ok... but don't blame me if you don't like it...\n")
            #put random recipe
        elif user_option == "4":
            import os
            os.system('cls')
            check_recipe()
        elif user_option == "exit":
            import os
            os.system('cls')
            initial_page()
        else:
            print('Please, enter a valid option to continue.')
            print("Or you can enter 'exit' to go back to the initial menu.")
            continue

def add_recipe():
    import os
    os.system('cls')

    print("Ok! Then we'll need you to give us some information...")

    user_details = input("Name and Surname:")
    recipe_name = input("Name of the recipe:")
    ingredients_list = input("What are the ingredients?")
    recipe_preparation = input("How we prepare the recipe?")
    recipe_type = input("Is it savoury or sweet?") #IT HAS TO BE SAVOURY OR SWEET ONLY
    recipe_favorite = input("This recipe is who's favorite?")

    print(f"""
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
            break        
        elif user_option == "2": 
            #  print("Ok! What would you like to edit?\n")
            #  print("1. Name\n 2. Recipe name\n 3.Ingredients\n 4.Recipe type\n 5. Recipe favorite")
            #  edit_answer = input("Enter your answer here:").isaplha() #caracteres precisam ser alpha
            #  while True:
            #          if edit_answer == "1":
            #             print("ok")#colocar só pra editar um ponto
            #          else:
            #             continue 
            print("What would you like to edit? \n 1. Name and surname \n 2. recipe's name")
            edit_recipe = input("Enter your option here:")
            if edit_recipe == "1":
                print("it's working")
            elif edit_recipe == "2":
                print("option working")
             
            print("Ok! Thank you so much for your contribution!\n")
             #update worksheet
        elif user_option == "exit":
            import os
            os.system('cls')
            initial_page()
        else:
            print('Please, enter a valid option to continue.')
            print("Or you can enter 'exit' to go back to the initial menu.")
            continue
    
    data_list = (user_details, recipe_name, ingredients_list, recipe_preparation, recipe_type)
    recipes.append_row(data_list)
    print("updated completed.")

def main():
    """
    run all program functions
    """
    initial_page()

print("""
 

  _____               _ _                  
 |  ___|_ _ _ __ ___ (_) |_   _            
 | |_ / _` | '_ ` _ \| | | | | |           
 |  _| (_| | | | | | | | | |_| |           
 |_|  \__,_|_| |_| |_|_|_|\__, |           
                          |___/            
  _____                     _ _            
 |  ___|_ ___   _____  _ __(_) |_ ___  ___ 
 | |_ / _` \ \ / / _ \| '__| | __/ _ \/ __|
 |  _| (_| |\ V / (_) | |  | | ||  __/\__ \
 |_|  \__,_| \_/ \___/|_|  |_|\__\___||___/
                                           

 
 \n
 """)
main()