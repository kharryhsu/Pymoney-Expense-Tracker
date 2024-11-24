import sys
import os

FILE_PATH = './records.txt'

def initialize_categories():
    """Initialize and return the predefined category hierarchy."""
    return ['expense', ['food', ['meal', 'snack', 'drink'], 'transportation', ['bus', 'railway']], 'income', ['salary', 'bonus']]

def view_categories(categories, level=0):
    """Recursively display the category hierarchy."""
    if categories == None:
        return
    
    if type(categories) == list:
        for child in categories:
            view_categories(child, level + 1)
    else:
        print(f'{" " * (level - 1) + "- "}{categories}')
        
def is_category_valid(category_name, categories):
    """Check if a category exists in the hierarchy."""
    if type(categories) == list:
        for item in categories:
            if item == category_name:
                return True
            if type(item) == list and is_category_valid(category_name, item):
                return True
    return False

def flatten(L):
    """Flatten a nested list into a single list."""
    if type(L) == list:
        result = []
        
        for item in L:
            result.extend(flatten(item))
        return result
    return [L]

def find_subcategories(category_name, categories):
    """Find subcategories for a given category."""
    if type(categories) == list:
        for item in categories:
            if item == category_name:
                idx = categories.index(item)
                subcategories = categories[idx + 1] if idx + 1 < len(categories) and type(categories[idx + 1]) == list else []
                return [category_name] + flatten(subcategories)
            
            if type(item) == list:
                result = find_subcategories(category_name, item)
                if result:
                    return result
    return []

def find(category_name, items_list, categories):
    """Find and display records matching a given category and its subcategories."""
    subcategories = find_subcategories(category_name, categories)
    
    if not subcategories:
        print(f"No records found for category '{category_name}'.")
        return
    
    print(f"Records under category '{category_name}':")
    
    filtered_records = filter(lambda x: x['cat'] in subcategories, items_list)
    total_amt = 0
    
    for record in filtered_records:
        print(f"{record['cat']:<20} {record['desc']:<20} {record['amt']:<10}")
        total_amt += record['amt']
        
    print(f"The total amount above is: {total_amt}")

def reset_records():
    """Reset the records by deleting the file and returning an empty state."""
    print("Deleting the contents.")    
    os.remove(FILE_PATH)
    return 0, []

def initialize():
    """Initialize balance and items list by reading from the records file."""
    balance = 0
    items_list = []
    lines = []
    
    # Handle 1: The file does not exist
    try:
        with open(FILE_PATH, 'r') as fh:
            balance_line = fh.readline() # Read the first line for balance
            lines = fh.readlines() # Read the remaining lines for records
            
        # Handle 2: Check if the first line is empty
        if not balance_line.strip():  # Check for empty
            sys.stderr.write("The balance line is empty. Invalid format in records.txt.\n")
            return reset_records()
        
        # Handle 3: Cannot convert first line to int
        try:
            balance = int(balance_line)
        except ValueError:
            sys.stderr.write("First line cannot be interpreted as initial amount of money. Invalid format in records.txt.\n")
            return reset_records()
        
        for line in lines:
            # Handle 4: Handle possible empty lines in records
            if not line.strip():
                sys.stderr.write("Some record lines are empty. Invalid format in records.txt.\n")
                return reset_records()
            
            # Handle 5: Cannot be split into a list of two str or the second str after splitting cannot be converted to int
            try:
                cat, desc, amt = line.split(' ')
                amt = int(amt)
                items_list.append({'cat': cat, 'desc': desc, 'amt': amt})
            except ValueError:
                sys.stderr.write("Line cannot be interpreted as a record. Invalid format in records.txt.\n")
                return reset_records()
        
        print("Welcome back!")
    except FileNotFoundError:
        print("Welcome! It looks like this is your first time using the program.")
        return balance, items_list
    
    return balance, items_list

def save(balance, items_list):
    """Save the balance and items list to the records file."""
    with open(FILE_PATH, 'w') as fh:
        fh.write(f"{balance}\n")
        records = [f"{record['cat']} {record['desc']} {record['amt']}\n" for record in items_list]
        fh.writelines(records)
            
def add(balance, items_list, categories):
    """Add new expense or income records."""
    print("Add some expense or income records with category, description, and amount (separate by spaces):")
    print("cat1 desc1 amt1, cat2 desc2 amt2, cat3 desc3 amt3, ...")
    
    entries  = input().split(', ') # Take the input as a comma-separated list of desc and amt pairs
    
    for entry in entries:
        try:
            cat, desc, amt = entry.split(' ') # Split each item into desc and amt
            amt = int(amt)
            if not is_category_valid(cat, categories):
                print(f"The specified category '{cat}' is not in the category list.")
                print("You can check the category list by command 'view categories'.")
                print("Skipping invalid record >>>\n")
                continue
            items_list.append({'cat': cat, 'desc': desc, 'amt': amt}) # Add the cat, desc and amt to the dict and appended in items_list
            balance += amt # Update the balance
        except ValueError:
            # Handle 7: User inputs a str that does not follow the format
            print(f"\nInvalid format for record: {entry}")
            if ' ' not in entry:
                print("The format of a record should be like this: breakfast -50.")
            # Handle 8: The second str of a record, after splitting, cannot be converted to an int
            else:
                print("Invalid value for money")
            print("Skipping invalid record >>>\n")
            continue # Skip invalid records and continue with valid entries
    
    return balance, items_list

def view(balance, items_list):
    """View all current records along with their details and total balance."""
    print("Here's your expense and income records:")
    print(f"{"Id":<5} {"Category":<20} {"Description":<20} {"Amount":<10}")
    print("=" * 5 + " " + "=" * 20 + " " + "=" * 20 + " " + "=" * 10)
    
    if not items_list: # If there are no records, display "NO RECORD" message
        print("-" * 14 + "NO RECORD" + "-" * 14)
    else: # else, display list of items
        for id, record in enumerate(items_list):
            print(f"{id + 1:<5} {record['cat']:<20} {record['desc']:<20} {record['amt']:<10}") # Display each record with an id, cat, desc, and amt

    print("=" * 5 + " " + "=" * 20 + " " + "=" * 20 + " " + "=" * 10)
    print(f"Now you have {balance} dollars.")
    
def delete(balance, items_list):
    """Delete a specific record by its ID."""
    print("Which record do you want to delete?")
    
    print('\n', end='')
    view(balance, items_list)
    print('\n', end='')

    while True:
        try:
            id = int(input("Please select Id of item you want to delete(Press -1 to cancel deletion): ")) # Ask for the record id the user wants to delete
            
            if 1 <= id <= len(items_list): # Check if the id is valid
                record = items_list.pop(id - 1) # Remove the selected record by index
                balance -= record['amt'] # Update the balance
                
                print(f"Record with category '{record['cat']}', description '{record['desc']}' and amount {record['amt']} has been successfully deleted.")
                break
            elif id == -1: # If the user enters -1, cancel the deletion
                print("Cancel deletion")
                break
            # Handle 9: The specified record does not exist
            else:
                print("Invalid number! No record found with that number.\nTry again.\n")
                continue
        # Handle 10: User inputs a str that cannot be converted to int
        except ValueError:
            print("Invalid format! Fail to delete a record.\nTry again.\n")
            continue
    
    return balance, items_list

balance, items_list = initialize()
categories = initialize_categories()

while True:
    # Handle 6: User inputs a str that cannot be converted to int
    try:
        if balance == 0:
            balance = int(input("\nHow much money do you have? ")) # Ask the user for their initial balance and store it as an integer
    except ValueError:
        print("Invalid value for money. Try again.")
        continue
    break

while True:
    cmd = input("\nWhat do you want to do (add / view / delete / view categories / find / exit)? ")
    
    if cmd == "add":
        balance, items_list = add(balance, items_list, categories)
    elif cmd == "view":
        view(balance, items_list)
    elif cmd == "delete":
        balance, items_list = delete(balance, items_list)
    elif cmd == "view categories":
        view_categories(categories)
    elif cmd == "find":
        category_name = input("Which category do you want to find? ")
        find(category_name, items_list, categories)
    elif cmd == "exit":
        save(balance, items_list)
        break
    # Handle 11: User inputs invalid command
    else:
        sys.stderr.write('Invalid command. Try again.\n')