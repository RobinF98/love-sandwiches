import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
  "https://www.googleapis.com/auth/spreadsheets",
  "https://www.googleapis.com/auth/drive.file",
  "https://www.googleapis.com/auth/drive",
]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("love_sandwiches")


def get_sales_data():
  """
  Get sales figures input from the user
  Run a while loop to repeat input request until valid data is inputted
  Data must be in the form 6 comma-separated ints
  """
  while True:
    print("Please enter sales data from the last market.")
    print("Data should be six numbers, separated by commas.")
    print("Example: 12,34,55,36,22,23\n")

    data_str = input("Enter your data here: ")
    
    sales_data = data_str.split(',')
    
    if validate_data(sales_data):
      print("Data is valid as per my extensive validation testing (～￣▽￣)～")
      break
  return sales_data

def validate_data(values):
  """
  Inside the try, parses all strings as integers - Raises ValueError if strings
  cannot be converted or if there aren't exactly 6 values
  """
  try:
    [int(value) for value in values]
    if len(values) != 6:
      raise ValueError(
        f"Exactly 6 values required, you provided {len(values)}"
      )
  except ValueError as e:
    print(f"Invalid data: {e}, please try again\n")
    return False
  
  return True


def update_sales_worksheet(data):
  """
  Update sales worksheet, add new row from data provided
  """
  print("Updating sales worksheet...\n")
  sales_worksheet = SHEET.worksheet("sales")
  sales_worksheet.append_row(data)
  print("Sales worksheet updated successfully.\n")

def calculate_surplus_data(sales_row):
  """
  Compare sales with stock and calculate the difference for each item type
  - Positive surplus indicates waste
  - Negative surplus indicates extra made when stock was sold out
  """
  
  print("Calculating surplus data...\n")
  stock  = SHEET.worksheet("stock").get_all_values()
  stock_row = stock[-1]
  surplus_row = [int(x)-y for x,y in zip(stock_row, sales_row)]
  return surplus_row

def update_surplus_worksheet(data):
  """
  Update surplus worksheet from data calculated
  """
  print("Updating surplus worksheet...\n")
  surplus_worksheet = SHEET.worksheet("surplus")
  surplus_worksheet.append_row(data)
  print("Surplus worksheet updated successfully.\n")
  
def main():
  """
  Run all program functions
  """
  data = get_sales_data()
  sales_data = [int(num) for num in data]
  update_sales_worksheet(sales_data)
  surplus_data = calculate_surplus_data(sales_data)
  update_surplus_worksheet(surplus_data)
  

print("Welcome to Love Sandwichs data automation\n")
main()