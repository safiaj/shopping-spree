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

def validate_data(values):
    """
   In the try block, all string values are attempted to be converted into integers. 
   If any strings cannot be converted into integers, or if there are not exactly 4 values, 
   a ValueError is raised. Additionally, if any converted value is greater than 50, 
   a ValueError is also raised.
    """
    try:
        int_values = [int(value) for value in values]
        if len(values) != 4:
            raise ValueError(
                f"Incorrect input, please input 4 figures, you provided {len(values)}"
            )
        if any(value > 50 for value in int_values):
            raise ValueError(
                "Values must be no bigger than 50"
            )
    except ValueError as e:
        print(f"Invalid input: {e}, please try again.\n")
        return False

    return True 

def update_worksheet(data, worksheet_name, start_col):
    """
    This function gets a list of integers to be inserted into the worksheet, and 
    updates the worksheet with this data provided.
    """
    print(f"\nUpdating {worksheet_name} worksheet...\n")
    worksheet = SHEET.worksheet(worksheet_name)
    for i, value in enumerate(data, start=2):  # Start from the second row
        worksheet.update_cell(i, start_col, value)
    print(f"{worksheet_name} worksheet updated successfully\n")

def add_new_brand_to_inventory():
    """
    Allow the user to add a new brand to the inventory.
    """
    print("\nInstructions for adding new inventory:")
    print("Enter the brand name and initial stock quantity for the new brand.")
    print("The quantities should be integers, no bigger than 50, separated by commas.")
    print("Example: Miu Miu, 10, 20, 15, 30")

    while True:
        inventory_str = input("\nEnter brand name and initial stock quantities here: ")
        inventory_data = inventory_str.split(",")

        if len(inventory_data) != 5:
            print("Invalid input format. Please enter the brand name followed by four stock quantities separated by commas.")
            continue

        brand_name = inventory_data[0].strip()
        quantities = [value.strip() for value in inventory_data[1:]]

        if validate_inventory_data(quantities):
            print("Input accepted!")
            break

    # Add the new brand name to all relevant sheets
    add_brand_to_sheets(brand_name, quantities)

    print("\nNew inventory added successfully.")

def validate_inventory_data(values):
    """
    Validate the entered inventory data.
    """
    try:
        int_values = [int(value) for value in values]
        if len(values) != 4:
            raise ValueError(
                f"Exactly 4 stock quantities required, you provided {len(values)}"
            )
        if any(value > 50 for value in int_values):
            raise ValueError(
                "Values must be no bigger than 50"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False

    return True

def add_brand_to_sheets(brand_name, quantities):
    """
    Add the brand name to all relevant sheets.
    """
    sheet_names = ["start", "sold", "finish"]
    for sheet_name in sheet_names:
        worksheet = SHEET.worksheet(sheet_name)
        next_available_col = len(worksheet.row_values(1)) + 1
        worksheet.update_cell(1, next_available_col, brand_name)
        if sheet_name == "start":
            update_worksheet(quantities, sheet_name, next_available_col)


def calculate_sold_data(finish_row):
    """
    Compare finish with start and calculate the sold for each brand/item type.
    Start data is always set to 50.
    """
    start_row = [50] * 4  # Start data is always 50

    sold_data = []
    for start, finish in zip(start_row, finish_row):
        sold = start - int(finish)
        sold_data.append(sold)

    return sold_data

def fetch_lowest_finish_location(lowest_finish_index):
    """
    Fetch the cell location of the lowest 'finish' number.
    The cell location is based on the row index and column index (1-indexed).
    """
    # Works as the 'finish' worksheet has headers in the first row
    row_index = lowest_finish_index + 2  # Adjust for 0-based index and header row
    column_index = 1  # 'finish' numbers are in the first column
    return f"A{row_index}"  # Return cell data 

def fetch_corresponding_data(lowest_finish_index):
    """
    Fetch the data from the corresponding first row of the 'finish' worksheet
    based on the index of the lowest 'finish' number.
    """
    # Get the 'finish' worksheet
    finish_worksheet = SHEET.worksheet("finish")
    # Fetch the data from the first row
    first_row_data = finish_worksheet.row_values(1)
    # Return the corresponding data based on the index of the lowest 'finish' number
    return first_row_data[lowest_finish_index]

def print_menu():
    """
    Print the menu options for the user.
    """
    print('\nMenu - Sales Data Management System:\n')
    print('Please select what you would like to do by entering a number '
          'between 1 and 3\n')

    menu_options = {
        '1': 'Update end of day sales data',
        '2': 'Add new brand to inventory',
        '3': 'Exit'
    }

    for key in menu_options.keys():
        print(key, '--', menu_options[key])

def main():
    """
    Run all functions to coordinate the process.
    """
    print("Welcome to the Deisgner Brands Sales Data Management System.\n")
    
    while True:
        print_menu()
        option = input('\nEnter your option here: ')

        if option == '1':
            # Update end of sales data
            insert_start_data()
            finish_data = get_finish_data()
            sold_data = calculate_sold_data(finish_data)
            next_available_col_finish = len(SHEET.worksheet("finish").row_values(1)) + 1
            next_available_col_sold = len(SHEET.worksheet("sold").row_values(1)) + 1
            update_worksheet(finish_data, "finish", next_available_col_finish)
            update_worksheet(sold_data, "sold", next_available_col_sold)
            finish_data, lowest_finish_index = calculate_finish_data()
            corresponding_data = fetch_corresponding_data(lowest_finish_index)
            print(f"\nThe following brand: {corresponding_data.upper()}, has sold the most items today with only {finish_data[lowest_finish_index]} items left over!\n")
        elif option == '2':
            # Add new brand to inventory
            add_new_brand_to_inventory()
        elif option == '3':
            # Exit the program
            print('\nThank You, Goodbye!\n')
            break
        else:
            print('Invalid option')

if __name__ == '__main__':
    main()
