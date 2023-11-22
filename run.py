import os
import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint
from tabulate import tabulate
from random import random

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
            print("Ok! Let's do it!\n")
            check_recipe()
        elif user_option == "2":
            add_recipe()
        else:
            print('Please, enter 1 or 2 to continue.')
            continue

class Recipe:
     def __init__(self, recipe_name, ingredients_list, recipe_preparation, recipe_type, recipe_favorite):
         self.recipe_name = recipe_name
         self.ingredients_list = ingredients_list
         self.recipe_preparation = recipe_preparation
         self.recipe_type = recipe_type
         self.recipe_favorite = recipe_favorite



def check_recipe():
    os.system('cls')

    print("Would you like a specific recipe or a suggestion? \n")
    print("1. View all recipes")
    print("2. Suggestion")

    while True:
        user_option = input("Enter your answer here:").strip()
        if user_option == "1":
            # print("Ok! Enter the recipe name here and we're going to see if we have it!\n")
            # input("Check recipe:")
            all_recipes = SHEET.worksheet("recipes").get_all_values()
            pprint(tabulate(all_recipes))

        elif user_option == "2":
            # recipe_suggestion()
            recipe_name = recipes.col_values(1).get_all_values()
            print(recipe_name)

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
            print("Ok! Today will have this for desert:\n")
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

     user_details = input("Name and Surname:").isalpha() #isaplha not working

     """
     while True:
        if not user_details.isalpha():
            continue
        else:
            print('its finally working;;;')            
        
     """
     recipe_name = input("Name of the recipe:")
     ingredients_list = input("What are the ingredients?")
     recipe_preparation = input("How we prepare the recipe?")
     recipe_type = input("Is it savoury or sweet?") #IT HAS TO BE SAVOURY OR SWEET ONLY
     recipe_favorite = input("This recipe is who's favorite?").isalpha()

     print(f"""
         Recipe name: {recipe_name}
         Ingredients List: {ingredients_list}
         Recipe Preparation: {recipe_preparation}
         Recipe Type: {recipe_type}
         Recipe Favorite: {recipe_favorite}
            """)
     
     print("Please, make sure you added all information right.\n")
     print("1. Edit")
     print("2. Confirm")

     while True:
         user_option = input("Enter your answer here:").strip()
         if user_option == "1": #confirming for now
            print("option 1 working")
            break
            #  print("Ok! What would you like to edit?\n")
            #  print("1. Name\n 2. Recipe name\n 3.Ingredients\n 4.Recipe type\n 5. Recipe favorite")
            #  edit_answer = input("Enter your answer here:").isaplha() #caracteres precisam ser alpha
            #  while True:
            #          if edit_answer == "1":
            #             print("ok")#colocar só pra editar um ponto
            #          else:
            #             continue         
         elif user_option == "2": #editing for now
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

    #check the information
    #confirmar a adição da receita
    #agradecer e menu inicial

# update_worksheet()

def main():
    """
    run all program functions
    """
    initial_page()

print("Welcome to family favorites")
main()