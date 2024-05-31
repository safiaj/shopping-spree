"""
Taken from love sandwiches module -
imports the entire gspread library so we can access all functions/classses 
within it and google auth imports the credentials class 
which is part of the service account function from google auth libary
""" 
import gspread
from google.oauth2.service_account import Credentials 

"""
Lists the APIs the program should to access for the
program to run 
"""
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('shopping-spree')


def get_finish_data():
    """
    Get 'finish' data from the user which indicates
    how many bags were sold by the brand at the end
    of the day 
    """
    print("Please enter the number of bags sold at the end of each day.\n")
    print("The data entered should be four numbers, no bigger than 50 each, separated by commas.\n")
    print("Example: 23, 45, 15, 37"\n)

    data_str = input("Enter your data here: ")
    print(f"The data provided is {data_str}")

get_finish_data()

