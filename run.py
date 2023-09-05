
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


# def update_sales_worksheet(data):
#   """
#   Update sales worksheet, add new row from data provided
#   """
#   print("Updating sales worksheet...\n")
#   sales_worksheet = SHEET.worksheet("sales")
#   sales_worksheet.append_row(data)
#   print("Sales worksheet updated successfully.\n")

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

def update_worksheet(data, worksheet):
  """
  Receives int list to be inserted into worksheet "worksheet"
  Updates relevant worksheet from data provided
  """
  print(f"Updating {worksheet} worksheet...\n")
  worksheet_to_update = SHEET.worksheet(worksheet)
  worksheet_to_update.append_row(data)
  print(f"{worksheet.capitalize()} worksheet updated successfully.\n")
  
def get_last_five_entries_sales():
  sales = SHEET.worksheet("sales")
  columns = []
  for i in range(1,7):
    column = sales.col_values(i)
    columns.append(column[-5:])
  return columns
    
def calculate_stock_data(data):
  """
  Calculate the average stock for each item type, and add 10%
  """
  print("Calculating stock data...\n")
  new_stock_data = []
  
  for column in data:
    new_stock_data.append(round((sum([int(num) for num in column])/5) * 1.1))
  
  return new_stock_data

def main():
  """
  Run all program functions
  """
  data = get_sales_data()
  sales_data = [int(num) for num in data]
  update_worksheet(sales_data, "sales")
  surplus_data = calculate_surplus_data(sales_data)
  update_worksheet(surplus_data, "surplus")
  data = get_last_five_entries_sales()
  stock_data = calculate_stock_data(data)
  update_worksheet(stock_data, "stock")

print("Welcome to Love Sandwichs data automation\n")
main()
