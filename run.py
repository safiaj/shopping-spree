"""
Taken from love sandwiches module -
imports the entire gspread library so I can access all functions/classses 
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

def insert_start_data():
    """
    Insert start data of '50' into the Google Sheet.
    """
    start_data = [50] * 4
    worksheet = SHEET.worksheet("start")
    next_available_col = len(worksheet.row_values(1)) + 1  # Find the next available column
    update_worksheet(start_data, "start", next_available_col)

def calculate_finish_data():
    """
    Calculate 'finish' data by subtracting sold data from the start.
    Start data is always set to 50 for current inventory.
    """
    start_row = [50] * 4  # Start data is always 50

    sold_sheet = SHEET.worksheet('sold')
    sold_data = sold_sheet.get_all_values()
    sold_row = [int(value) for value in sold_data[-1]]

    finish_data = [start - sold for start, sold in zip(start_row, sold_row)]

    # Find the index of the lowest 'finish' number
    lowest_finish_index = finish_data.index(min(finish_data))
    return finish_data, lowest_finish_index

def calculate_finish_data():
    """
    Calculate 'finish' data by subtracting sold data from the start.
    Start data is always set to 50 for current inventory.
    """
    start_row = [50] * 4  # Start data is always 50

    sold_sheet = SHEET.worksheet('sold')
    sold_data = sold_sheet.get_all_values()
    sold_row = [int(value) for value in sold_data[-1]]

    finish_data = [start - sold for start, sold in zip(start_row, sold_row)]

    # Find the index of the lowest 'finish' number
    lowest_finish_index = finish_data.index(min(finish_data))
    return finish_data, lowest_finish_index

def get_finish_data():
    """
    Get 'finish' data from the user which indicates
    how many items they sold per brand at the end
    of the day 
    """
    while True:
        print("\nEnter the number of designer items per brand that are left at the end of each day, in the following order: Prada, Louis Vuitton, Chanel, Gucci\n")
        print("The data entered should be four numbers, no bigger than 50 each, separated by commas.\n")
        print("Example: 23, 45, 15, 37")

        data_str = input("Please input data here: ")
    
        finish_data = data_str.split(",")

        if validate_data(finish_data):
            print("Input accepted!")
            break

    return finish_data