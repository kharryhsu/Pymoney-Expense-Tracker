import sys
import os

FILE_PATH = './records.txt'

def reset_records():
    print("Deleting the contents.")    
    os.remove(FILE_PATH)
    return 0, []

def initialize():
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
                desc, amt = line.split(' ')
                amt = int(amt)
                items_list.append({'desc': desc, 'amt': amt})
            except ValueError:
                sys.stderr.write("Line cannot be interpreted as a record. Invalid format in records.txt.\n")
                return reset_records()
        
        print("Welcome back!")
    except FileNotFoundError:
        print("Welcome! It looks like this is your first time using the program.")
        return balance, items_list
    
    return balance, items_list

def save(balance, items_list):
    with open(FILE_PATH, 'w') as fh:
        fh.write(f"{balance}\n")
        records = [f"{record['desc']} {record['amt']}\n" for record in items_list]
        fh.writelines(records)
            
def add(balance, items_list):
    print("Add some expense or income records with description and amount:")
    print("desc1 amt1, desc2 amt2, desc3 amt3, ...")
    
    entries  = input().split(', ') # Take the input as a comma-separated list of desc and amt pairs
    
    for entry in entries:
        try:
            desc, amt = entry.split(' ') # Split each item into desc and amt
            amt = int(amt)
            items_list.append({'desc': desc, 'amt': amt}) # Add the desc and amt to the dict and appended in items_list
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
    print("Here's your expense and income records:")
    print(f"{"Id":<5} {"Description":<20} {"Amount":<10}")
    print("=" * 5 + " " + "=" * 20 + " " + "=" * 10)
    
    if not items_list: # If there are no records, display "NO RECORD" message
        print("-" * 14 + "NO RECORD" + "-" * 14)
    else: # else, display list of items
        for id, record in enumerate(items_list):
            print(f"{id + 1:<5} {record['desc']:<20} {record['amt']:<10}") # Display each record with an id, desc, and amt

    print("=" * 5 + " " + "=" * 20 + " " + "=" * 10)
    print(f"Now you have {balance} dollars.")
    
def delete(balance, items_list):
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
                
                print(f"Record with description '{record['desc']}' and amount {record['amt']} has been successfully deleted.")
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
    cmd = input("\nWhat do you want to do (add / view / delete / exit)? ")
    
    if cmd == "add":
        balance, items_list = add(balance, items_list)
    elif cmd == "view":
        view(balance, items_list)
    elif cmd == "delete":
        balance, items_list = delete(balance, items_list)
    elif cmd == "exit":
        save(balance, items_list)
        break
    # Handle 11: User inputs invalid command
    else:
        sys.stderr.write('Invalid command. Try again.\n')