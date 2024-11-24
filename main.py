import sys
import os

balance = -1
items_list = [] # Empty list to store the expense/income records with 'desc' and 'amt' keys

while True:
    # Handle 1: The file does not exist
    try:
        lines = []
        with open('./records.txt', 'r') as fh:
            lines = fh.readlines()
        
        # Handle 2: No lines in the file
        if not lines:
            sys.stderr.write("No lines in the file. Invalid format in records.txt.\n")
            print("Deleting the contents.")
            
            os.remove('./records.txt')
            sys.exit(1)
        
        # Handle 3: Cannot converted first line to int
        try:
            balance = int(lines[0])
        except ValueError:
            sys.stderr.write("First line cannot be interpreted as initial amount of money. Invalid format in records.txt.\n")
            print("Deleting the contents.")
            
            os.remove('./records.txt')
            sys.exit(2)
        
        for line in lines[1:]:
            # Handle 4: Cannot be split into a list of two str or the second str after splitting cannot be converted to int
            try:
                desc, amt = line.split(' ')
                amt = int(amt)
                items_list.append({'desc': desc, 'amt': amt})
            except ValueError:
                sys.stderr.write("Line cannot be interpreted as a record. Invalid format in records.txt.\n")
                print("Deleting the contents.")
                
                os.remove('./records.txt')
                sys.exit(3)
        
        print("Welcome back!")
        break
    except FileNotFoundError:
        print("Welcome! It looks like this is your first time using the program.")
        balance = 0
        break

while True:
    # Handle 5: User inputs a str that cannot be converted to int
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
        print("Add some expense or income records with description and amount:")
        print("desc1 amt1, desc2 amt2, desc3 amt3, ...")
        
        entries  = input().split(', ') # Take the input as a comma-separated list of desc and amt pairs
        
        for entry in entries:
            try:
                desc, amt = entry.split(' ') # Split each item into desc and amt
                amt = int(amt)
                items_list.append({'desc': desc, 'amt': amt}) # Add the desc and amt to the dict
                balance += amt # Update the balance
            except ValueError:
                # Handle 6: User inputs a str that does not follow the format
                if ' ' not in entry:
                    print("The format of a record should be like this: breakfast -50.")
                # Handle 7: The second str of a record, after splitting, cannot be converted to an int
                else:
                    print("Invalid value for money")
                print("Fail to add a record")
                break
    elif cmd == "view":
        print("Here's your expense and income records:")
        print(f"{"Id":<5} {"Description":<20} {"Amount":<10}")
        print("=" * 5 + " " + "=" * 20 + " " + "=" * 10)
        
        if not items_list: # If there are no records, display "NO RECORD" message
            print("-" * 14 + "NO RECORD" + "-" * 14)
        else: # else, display list of items
            for id, record in enumerate(items_list): # UNpack tuple from dict pairs
                print(f"{id + 1:<5} {record['desc']:<20} {record['amt']:<10}") # Display each record with an id, desc, and amt

        print("=" * 5 + " " + "=" * 20 + " " + "=" * 10)
        print(f"Now you have {balance} dollars.")
    elif cmd == "delete":
        print("Which record do you want to delete?")

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
                # Handle 8: The specified record does not exist
                else:
                    print("Invalid number! No record found with that number.\nTry again.\n")
                    continue
            # Handle 9: User inputs a str that cannot be converted to int
            except ValueError:
                print("Invalid format! Fail to delete a record.\nTry again.\n")
                continue
    elif cmd == "exit":
        break
    # Handle 10: User inputs invalid command
    else:
        print("Invalid command. Try again.")
        
    
with open('./records.txt', 'w') as fh:
    fh.write(f"{balance}\n")
    for record in items_list:
        fh.write(f"{record['desc']} {record['amt']}\n")
