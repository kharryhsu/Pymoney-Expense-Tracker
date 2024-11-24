balance = int(input("How much money do you have? ")) # Ask the user for their initial balance and store it as an integer

items_dict = {} # Empty dict to store the expense/income records, format{key = description, and value = amount}

while True:
    cmd = input("What do you want to do (add / view / delete / exit)? ")
    
    if cmd == "add":
        print("Add some expense or income records with description and amount:")
        print("desc1 amt1, desc2 amt2, desc3 amt3, ...")
        
        items_list = input().split(', ') # Take the input as a comma-separated list of desc and amt pairs
        
        for item in items_list:
            desc, amt = item.split(' ') # Split each item into desc and amt
            items_dict[desc] = int(amt) # Add the desc and amt to the dict
            balance += int(amt) # Update the balance
    elif cmd == "view":
        print("Here's your expense and income records:")
        print(f"{"Id":<5} {"Description":<20} {"Amount":<10}")
        print("=" * 5 + " " + "=" * 20 + " " + "=" * 10)
        
        if len(items_dict) < 1: # If there are no records, display "NO RECORD" message
            print("-" * 14 + "NO RECORD" + "-" * 14)
        else: # else, display list of items
            for id, (desc, amt) in enumerate(items_dict.items()): # UNpack tuple from dict pairs
                print(f"{id + 1:<5} {desc:<20} {amt:<10}") # Display each record with an id, desc, and amt

        print("=" * 5 + " " + "=" * 20 + " " + "=" * 10)
        print(f"Now you have {balance} dollars.")
    elif cmd == "delete":
        print("Which record do you want to delete?")

        while True:
            id = int(input("Please select Id of item you want to delete(Press -1 to cancel deletion): ")) # Ask for the record id the user wants to delete
            
            if 1 <= id <= len(items_dict): # Check if the id is valid
                desc = list(items_dict.keys())[id - 1] # Find the description of the item to delete by using the ID
                amt = items_dict[desc] # Get the amt associated with the desc
                items_dict.pop(desc) # Remove the record from the dict
                balance -= amt # Update the balance
                
                print(f"Record with description '{desc}' and amount {amt} has been successfully deleted.")
                
                break
            elif id == -1: # If the user enters -1, cancel the deletion
                print("Cancel deletion")
                
                break
            else: # If the user enters an invalid number
                print("Invalid number! No record found with that number.")
        
    elif cmd == "exit":
        break
