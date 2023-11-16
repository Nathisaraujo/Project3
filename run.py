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

def check_recipe():
    os.system('cls')

    print("Would you like a specific recipe or a suggestion? \n")
    print("1. Specific")
    print("2. Suggestion")

    while True:
        user_option = input("Enter your answer here:").strip()
        if user_option == "1":
            print("Ok! Enter the recipe name here and we're going to see if we have it!\n")
            input("Check recipe:")
        elif user_option == "2":
            recipe_suggestion()
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
            print("Ok! Our today suggestion is:\n")
            #put random savoury recipe
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
initial_page()