import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint



SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]


CREDS = Credentials.from_service_account_file('creds.json')
SCOPE_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPE_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

def get_sales_data():
    """
    Get sales figure input from the user
    """
    while True:
        print("please enter sales data from the last market.")
        print("Data should be six numbers, separated by commas.")
        print("Example:10,20,30,40,50,60\n")

        data_str = input("Enter your data here:")
    
        sales_data = data_str.split(",")

        if validate_data(sales_data):
            print("Data is valid")
            break

    return sales_data    




def validate_data(values):
    """Inside the try,converts all strings to integers rasises 
    value error if strings can not be converted into it, or if there are't exactly 
    6 values
    """
    try:
        if len(values) != 6:
            raise ValueError (
                f"Exactly 6 values required, you provided{len(values)}"
            )
    except ValueError as e:
        print(f"invalid data: {e}, please try again.\n")
        return False

    return True   
    


'''def update_sales_worksheet(data):
    """ 
update sales worksheet, add row with the list data provided.
    """
    print("updating sales worksheet...\n")
    sales_worksheet = SHEET.worksheet("sales")
    sales_worksheet.append_row(data)
    print("sales worksheet updated successfully.\n")



def update_surplus_worksheet(data):
    """
    update surplus worksheet, add row with the list data provided.
    """
    print("updating surplus worksheet...\n")
    surplus_worksheet = SHEET.worksheet("surplus")
    surplus_worksheet.append_row(data)
    print("surplus worksheet updated successfully.\n")
'''

def update_worksheet(data, worksheet):
    """ 
    Recieve a list of integers to inserted into a worksheet 
    update the relevant with the data provided
    """
    print("updating {worksheet} sales worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated successfully..\n")


def calculate_surplus_data(sales_row):
    """
    compare sales with stock and calculate the surplus for each item type.
    -positive surplus indicates waste
    - Negative surplus indicates  extra made stock was sold out.
    """

    print("calculating surplus data...\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]
    
    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock )- sales
        surplus_data.append(surplus)

    return surplus_data

def get_last_5_entries_sales():
    """calculate columns of data from sales worksheet, collecting the last 5 entries
       for each sandwiches and returns the data as a list of lists.
    """
    sales =  SHEET.worksheet("sales")
    column = sales.col_values()
       
    columns = []
     
    for ind in range(1, 7):
        column = sales.col_values(ind)
        columns.append(column[-5:])

        return columns





def main():
    """ 
    Run all programs
    """

data = get_sales_data()
sales_data = [int(num) for num in data]
update_worksheet(sales_data, "sales")
new_surplus_data = calculate_surplus_data(sales_data)
update_worksheet(new_surplus_data, "surplus")



print("Welcome to Love Sandwiches Data Automation")
main()

sales_columns = get_last_5_entries_sales()