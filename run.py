# import gspread to update worksheet
import re # importation tool to search for patterns in strings
import gspread
from google.oauth2.service_account import Credentials
import os  # import to clear screen
from random import randint  # import to choose random data in the worksheet
import time  # import to time.sleep
import sys  # import to exit program
from prettytable import PrettyTable  # import table style

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

#  functions to call colors
#  I got this part of the code at geeksforgeeks.org - see readme


def prRed(skk): print("\033[91m {}\033[00m" .format(skk))


def prYellow(skk): print("\033[93m {}\033[00m" .format(skk))


def prPurple(skk): print("\033[95m {}\033[00m" .format(skk))


def prCyan(skk): print("\033[96m {}\033[00m" .format(skk))


def prGreen(skk): print("\033[92m {}\033[00m" .format(skk))


# Validation functions for recipe fields
def validate_alphabetic(value):
    return bool(re.match("^[A-Za-z ]+$", value))


def validate_recipe_steps(value):
    return len(value.split()) > 2


# ensures that user inputs are not empty or invalid
def validate_input(prompt, allow_empty=False, validation_fn=None, error_message="Invalid input"):
    while True:
        user_input = input(prompt).strip()
        if user_input or allow_empty:
            if validation_fn is None or validation_fn(user_input):
                return user_input
            else:
                prRed(error_message)
        else:
            prRed("Input cannot be empty. Please try again.")


def initial_page():
    """
    Initial page
    Ask what the user would like to do - check or add a recipe.
    """
    clear_console()
    print("\nWhat would you like to do? \n")
    print("1. Check a recipe")
    print("2. Add a new one")
    print("3. Exit the program\n")

    #  All code using 'while/if/elif/else' structure was inspired 
    #  in my colleague 'Pasta la vista' project - see readme

    while True:
        user_option = validate_input("Enter your answer here:\n").strip()
        if user_option == "1":
            prPurple("Ok! Let's check what we have here...\n")
            time.sleep(1.5)
            check_recipe()
        elif user_option == "2":
            prPurple("HMMMM! New recipe coming!\n")
            time.sleep(1.5)
            add_recipe()
        elif user_option == "3":
            prPurple("Ok... bye bye!\n")
            exit_program()
        else:
            prRed('Please, enter a valid option to continue.')
            continue


def check_recipe():
    """
    - Option so the user can check the recipe.
    - It takes the user to the option they choose, respectively.
    - The user can also choose to exit the program or go back to
    the main page.
    """
    clear_console()

    print("How would you like to find a recipe?\n")
    print("1. View all recipes")
    print("2. Give me a suggestion")
    print("3. Check recipe by name")
    print("4. Go back to main page.")

    while True:
        user_option = validate_input("\nEnter your answer here:\n").strip().lower()
        if user_option == "1":
            all_recipes()
        elif user_option == "2":
            recipe_suggestion()
        elif user_option == "3":
            recipe_by_name()
        elif user_option == "4":
            os.system('clear')
            main()
        elif user_option == "exit":
            exit_program()
        else:
            prRed('Please, enter a valid option to continue.')
            prRed("Or you can enter 'exit' to end the program.")
            continue


def all_recipes():
    """
    - Return all recipes from the worksheet to
    the user.
    - It gets the headers and align with all
    rows.
    """
    clear_console()
    headers = [
        "Name",
        "Ingredients",
        "How to make it",
        "Creator's Name",
        "Who's Favorite"
    ]

    all_recipes = SHEET.worksheet("recipes").get_all_values()

    tables = PrettyTable()
    tables.field_names = headers
    tables.max_width = 7 #  ChatGPT suggestion - see readme
    tables.align = "l"

    for row in all_recipes:
        tables.add_row(row)
    print(tables)
    next_move()


def search_recipe_by_name(recipe_name):
    """
    When the user choose to look for a recipe
    by the name:
    - Searches the first column of the panel
    to see if the name the user entered exists.
    """
    recipes = []
    all_rows = SHEET.worksheet("recipes").get_all_values()
    for row in all_rows:
        if recipe_name.lower() in row[0].lower():
            recipes.append(row)
    return recipes


def recipe_by_name():
    """
    - This is the option to look for a recipe by name.
    - The user writes what he wants and the program
    sees if the recipe exists in the spreadsheet.
    - If a recipe is found, return the respective row.
    - If no recipe is found, it gives him the option
    to choose again.
    """
    clear_console()
    prPurple("""Ok! Enter the recipe name here
    and we're going to see if we have it!\n""")
    recipe_name = validate_input("Check Recipe:\n", validation_fn=validate_alphabetic, error_message="Recipe name can only contain letters and spaces.")
    found_recipes = search_recipe_by_name(recipe_name)

    headers = [
        "Name",
        "Ingredients",
        "How to make it",
        "Creator's Name",
        "Who's Favorite"
    ]

    if found_recipes:
        print(f"Found {len(found_recipes)} matching recipes:")
        prCyan("\nRecipe Details:")
        tables = PrettyTable()
        tables.field_names = headers
        tables.max_width = 7
        tables.align = "l"

        for row in found_recipes:
            tables.add_row(row)
        print(tables)

        next_move()
    else:
        prRed("No recipes found with that name.")
        print("Please, choose again.")
        time.sleep(1.5)
        check_recipe()


def recipe_suggestion():
    """
    - In this option, the user chooses to
    receive a random recipe suggestion.
    - It returns a single row with a random
    suggestion from the spreadsheet recipe book.
    - If the user is not happy with the recipe
    given, he can opt to get other random recipe.
    """
    clear_console()

    prPurple("Ok! I think you'll like this one:\n")
    time.sleep(0.8)
    all_recipes = SHEET.worksheet("recipes").get_all_values()
    if len(all_recipes) > 1:
        headers = [
            "Name",
            "Ingredients",
            "How to make it",
            "Creator's Name",
            "Who's Favorite"
        ]
        random_index = randint(1, len(all_recipes)-1)
        random_recipe = all_recipes[random_index - 1]
        tables = PrettyTable()
        tables.field_names = headers
        tables.max_width = 7
        tables.align = "l"

        tables.add_row(random_recipe)
        print(tables)

        print("\nWhat to do next?")
        print("1. Another recommendation.")
        print("2. Go back to main menu.")
        print("3. Exit the program.\n")

        while True:
            user_option = validate_input("Enter your answer here:\n").strip().lower()
            if user_option == "1":
                os.system('clear')
                recipe_suggestion()
            elif user_option == "2":
                os.system('clear')
                main()
            elif user_option == "3":
                exit_program()
            else:
                prRed('Please, enter a valid option to continue.')
                continue


def add_recipe():
    """
    - This option allows the user to add a
    new recipe.
    - The user will be asked to fill some information
    that is uploaded to the spreadsheet in a new row.
    - If it has some type mistakes, the user can choose
    to edit it.
    """
    clear_console()

    prPurple("Ok! Then we'll need you to give us some information...\n")
    time.sleep(1.0)

    global user_details
    global recipe_name
    global ingredients_list
    global recipe_preparation
    global recipe_favorite

    recipe_name = validate_input("Name of the recipe:\n", validation_fn=validate_alphabetic, error_message="Recipe name can only contain letters and spaces.")
    ingredients_list = validate_input("What are the ingredients?\n", validation_fn=validate_recipe_steps, error_message="Recipe preparation should be at least a few words.")
    recipe_preparation = validate_input("How we prepare the recipe?\n", validation_fn=validate_recipe_steps, error_message="Recipe preparation should be at least a few words.")
    user_details = validate_input("Your first name:\n", validation_fn=validate_alphabetic, error_message="Name can only contain alphabetic characters and spaces.")
    recipe_favorite = validate_input("Who in our family likes this recipe the most?\n", validation_fn=validate_alphabetic, error_message="Name can only contain alphabetic characters and spaces.")

    print(f"""
        Recipe name: {recipe_name}
        Ingredients List: {ingredients_list}
        Recipe Preparation: {recipe_preparation}
        Your name: {user_details}
        Recipe Favorite: {recipe_favorite}
        """)
    print("Please, make sure you added all information right.\n")
    print("1. Confirm")
    print("2. Edit")
    print("3. Cancel and go to main page\n")

    while True:
        user_option = validate_input("Enter your answer here:\n").strip().lower()
        if user_option == "1":
            confirm_recipe()
        elif user_option == "2":
            edit_recipe()
        elif user_option == "3":
            clear_console()
            main()
        elif user_option == "exit":
            exit_program()
        else:
            prRed('Please, enter a valid option to continue.')
            prRed("Or you can enter EXIT to go back to the initial menu.")


def edit_recipe():
    """
    - This is the option to edit the information
    given by the user when adding a new recipe.
    - The user can edit all options and the new info
    will be updated when the user enter 'confirm'
    """
    clear_console()

    global user_details
    global recipe_name
    global ingredients_list
    global recipe_preparation
    global recipe_favorite

    print("Which information would you like to edit?\n")
    print("1. Recipe name")
    print("2. Ingredients list")
    print("3. Recipe preparation")
    print("4. First name")
    print("5. Recipe favorite")
    print("6. Cancel and go to the main page\n")

    #  This part of the code was suggested by ChatGPT
    #  in order to fix a bug and also shorten the code
    #  Please, see the readme for more information

    edit_option = validate_input("Enter your option here:\n")
    if edit_option == "1":
        recipe_name = validate_input(f'Recipe name ({recipe_name}):\n') or recipe_name
    elif edit_option == "2":
        ingredients_list = validate_input(f'Ingredients list ({ingredients_list}):\n')\
                            or ingredients_list
    elif edit_option == "3":
        recipe_preparation = validate_input(f'Recipe preparation ({recipe_preparation}):\n')\
                            or recipe_preparation
    elif edit_option == "4":
        user_details = validate_input(f'First name ({user_details}):\n') or user_details
    elif edit_option == "5":
        recipe_favorite = validate_input(f'Recipe favorite ({recipe_favorite}):\n')\
                            or recipe_favorite
    elif edit_option == "6":
        main()
    else:
        prRed('Please, enter a valid option to continue.')

    print(f"""
        Recipe name: {recipe_name}
        Ingredients List: {ingredients_list}
        Recipe Preparation: {recipe_preparation}
        Your name: {user_details}
        Recipe Favorite: {recipe_favorite}
        """)
    prRed("\nPlease, make sure you added all information right.")
    print("\n1. Confirm")
    print("2. Edit")
    print("3. Cancel and go to main page\n")

    while True:
        user_option = validate_input("Enter your answer here:\n").lower()
        if user_option == "1":
            confirm_recipe()
        elif user_option == "2":
            edit_recipe()
        elif user_option == "3":
            clear_console()
            main()
        elif user_option == "exit":
            exit_program()
        else:
            prRed('Please, enter a valid option to continue.')
            prRed("Or you can enter 'exit' to go back to the initial menu.")


def confirm_recipe():
    """
    Here the new recipe added is uploaded
    to the spreadsheet when the user enter
    'confirm' in the console.
    """
    clear_console()
    prGreen("Thank you! Just one second and we're done!\n")
    global user_details
    global recipe_name
    global ingredients_list
    global recipe_preparation
    global recipe_favorite
    data = [recipe_name, ingredients_list, recipe_preparation, user_details, recipe_favorite]

    #  To add a recipe in the spreadsheet,
    #  I inspired myself in my colleague "Kennel Mate"
    #  project - see readme

    try:
        SHEET.worksheet("recipes").append_row(data)
        prYellow("Loading your information...")
        time.sleep(1.0)
        prGreen('All done! Recipe saved!\n')
        time.sleep(2)
        clear_console()
        next_move()
    except Exception as e:
        prRed(f"An error occurred: {e}")
        print("Please, try again later.")
        time.sleep(2)
        clear_console()
        next_move()


def next_move():
    """
    This option appears after an option is
    chosen by the user so he can choose to go back
    to the main page (to do something else) or
    exit the program if he's finished.
    """
    prCyan("\nWhat to do next?")
    print("1. Search recipe.")
    print("2. Go back to main menu.")
    print("3. Exit the program.\n")

    while True:
        user_option = validate_input("Enter your answer here:\n").lower()
        if user_option == "1":
            check_recipe()
        elif user_option == "2":
            clear_console()
            main()
        elif user_option == "3":
            exit_program()
        else:
            prRed('Please, enter a valid option to continue.')


def clear_console():
    """
    It clears the console.
    This part I took from Geeks for Geeks website
    and ChatGPT to solve the bug - see readme
    """
    os.system('clear' if os.name == 'posix' else 'cls')


def exit_program():
    """
    It exits the program when requested by the user.
    This code was taken from freecodecamp.org - see readme
    """
    clear_console()
    prGreen("Thanks for using the family favorites recipe book! Goodbye!")
    time.sleep(2)
    prRed("Exiting the program...")
    time.sleep(1.0)
    sys.exit(0)


def main():
    """
    This is the main page. It explains to the
    user what 'Family Favorites' is about and
    start the program.
    """
    clear_console()
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
        |  _| (_| |\ V / (_) | |  | | ||  __/\__ \\
        |_|  \__,_| \_/ \___/|_|  |_|\__\___||___/
        """)
    prYellow("""\n
                     Welcome to
                 Family Favorites
     This is a heartfelt family recipe book where
          we can share our favorite recipes!
    This is a gift to our future generation who will
       be able to prepare the most special dishes.\n""")
    input("Press Enter to continue...\n")
    initial_page()


main()
