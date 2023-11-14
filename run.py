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
    print("Would you like to check a recipe or add a new one?")
    print("Write add or check in the terminal, please.\n")

    user_option = input("Enter your answer here:")
    print(f"The data provided is {user_option}")

initial_page()