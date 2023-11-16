import os
import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('family_favorites')

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

def user_option():
    """
    add option
    """
    while True:
        try:
            if user_option == "1":
                user_details = input("Name and Surname:")
                recipe_name = input("Name of the recipe:")
                ingredients_list = input("What are the ingredients?")
                preparation_step = input("How we prepare the recipe?")
                food_type = input("Is it savoury or sweet?")
                whos_favorite = input("This recipe is who's favorite?")
                #update the worksheet and then initial menu again
                break
            elif user_option == "2":
                give_idea = input("How would you like it? \n 1. Savoury \n 2. Sweet")
                #give a random recipe
                break
        except VauleError as e:
            print("Invalid option")
    


initial_page()