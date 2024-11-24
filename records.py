import sys
import os

from errors import RecordsError

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the current script
FILE_PATH = os.path.join(BASE_DIR, "records.txt")

class Record:
    """Represent a financial record."""
    def __init__(self, cat : str, desc : str, amt : int):
        self._category = cat
        self._description = desc
        self._amount = amt
    
    @property
    def category(self):
        return self._category
    
    @property
    def description(self):
        return self._description
    
    @property
    def amount(self):
        return self._amount
    
class Records:
    """Manage a list of records and the initial amount of money."""
    def __init__(self):
        self._balance = 0
        self._item_list = []
        
        # Handle 1: The file does not exist
        try:
            with open(FILE_PATH, 'r') as fh:
                balance_line = fh.readline() # Read the first line for balance
                lines = fh.readlines() # Read the remaining lines for records
                
            # Handle 2: Check if the first line is empty
            if not balance_line.strip():  # Check for empty
                self.reset_records()
                raise RecordsError("The balance line is empty. Invalid format in records.txt.")
            
            # Handle 3: Cannot convert first line to int
            try:
                self._balance = int(balance_line)
            except ValueError:
                self.reset_records()
                raise RecordsError("First line cannot be interpreted as initial amount of money. Invalid format in records.txt.")
            
            for line in lines:
                # Handle 4: Handle possible empty lines in records
                if not line.strip():
                    self.reset_records()
                    raise RecordsError("Some record lines are empty. Invalid format in records.txt.")
                
                # Handle 5: Cannot be split into a list of two str or the second str after splitting cannot be converted to int
                try:
                    cat, desc, amt = line.split(' ')
                    amt = int(amt)
                    self._item_list.append({'cat': cat, 'desc': desc, 'amt': amt})
                except ValueError:
                    self.reset_records()
                    raise RecordsError("Line cannot be interpreted as a record. Invalid format in records.txt.")
            
            print("Welcome back!")
        except FileNotFoundError:
            print("Welcome! It looks like this is your first time using the program.")
        except RecordsError as e:
                    sys.stderr.write(f"{e}\n")
                    sys.exit(1)
    
    @property
    def balance(self):
        return self._balance
    
    @property
    def item_list(self):
        return self._item_list
    
    def initialize_balance(self):
        if self._balance == 0:
            while True:
                # Handle 6: User inputs a str that cannot be converted to int
                try:
                    self._balance = int(input("\nHow much money do you have? "))
                    break
                except ValueError:
                    print("Invalid value for money. Try again.")
        
    def reset_records(self):
        """Reset the records by deleting the file and returning an empty state."""
        print("Deleting the contents.") 
        self._balance = 0
        self._item_list = []   
        os.remove(FILE_PATH)
    
    def save(self):
        """Save the balance and items list to the records file."""
        with open(FILE_PATH, 'w') as fh:
            fh.write(f"{self._balance}\n")
            records = [f"{record['cat']} {record['desc']} {record['amt']}\n" for record in self._item_list]
            fh.writelines(records)
    
    def add(self, categories):
        """Add new expense or income records."""
        print("Add some expense or income records with category, description, and amount (separate by spaces):")
        print("cat1 desc1 amt1, cat2 desc2 amt2, cat3 desc3 amt3, ...")
        
        entries  = input().split(', ') # Take the input as a comma-separated list of desc and amt pairs
        
        for entry in entries:
            try:
                cat, desc, amt = entry.split(' ') # Split each item into desc and amt
                amt = int(amt)
                if not categories.is_category_valid(cat, categories.list_categories):
                    print(f"The specified category '{cat}' is not in the category list.")
                    print("You can check the category list by command 'view categories'.")
                    print("Skipping invalid record >>>\n")
                    continue
                self._item_list.append({'cat': cat, 'desc': desc, 'amt': amt}) # Add the cat, desc and amt to the dict and appended in items_list
                self._balance += amt # Update the balance
            except ValueError:
                # Handle 7: User inputs a str that does not follow the format
                print(f"\nInvalid format for record: {entry}")
                if ' ' not in entry:
                    print("The format of a record should be like this: food breakfast -50.")
                # Handle 8: The second str of a record, after splitting, cannot be converted to an int
                else:
                    print("Invalid value for money")
                print("Skipping invalid record >>>\n")
                continue # Skip invalid records and continue with valid entries

    def delete(self):
        """Delete a specific record by its ID."""
        print("Which record do you want to delete?")
        
        print('\n', end='')
        self.view()
        print('\n', end='')

        while True:
            try:
                id = int(input("Please select Id of item you want to delete(Press -1 to cancel deletion): ")) # Ask for the record id the user wants to delete
                
                if 1 <= id <= len(self._item_list): # Check if the id is valid
                    record = self._item_list.pop(id - 1) # Remove the selected record by index
                    self._balance -= record['amt'] # Update the balance
                    
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

    def view(self):
        """View all current records along with their details and total balance."""
        print("Here's your expense and income records:")
        print(f"{"Id":<5} {"Category":<20} {"Description":<20} {"Amount":<10}")
        print("=" * 5 + " " + "=" * 20 + " " + "=" * 20 + " " + "=" * 10)
        
        if not self._item_list: # If there are no records, display "NO RECORD" message
            print("-" * 24 + "NO  RECORD" + "-" * 24)
        else: # else, display list of items
            for id, record in enumerate(self._item_list):
                print(f"{id + 1:<5} {record['cat']:<20} {record['desc']:<20} {record['amt']:<10}") # Display each record with an id, cat, desc, and amt

        print("=" * 5 + " " + "=" * 20 + " " + "=" * 20 + " " + "=" * 10)
        print(f"Now you have {self._balance} dollars.")
    
    def find(self, category_name, categories):
        """Find and display records matching a given category and its subcategories."""
        subcategories = categories.find_subcategories(category_name, categories.list_categories)
        
        if not subcategories:
            print(f"No records found for category '{category_name}'.")
            return
        
        print(f"Records under category '{category_name}':")

        
        filtered_records = filter(lambda x: x['cat'] in subcategories, self._item_list)
        total_amt = 0
        
        print(f"{"Category":<20} {"Description":<20} {"Amount":<10}")
        print("=" * 20 + " " + "=" * 20 + " " + "=" * 10)
        
        if not self._item_list:
            print("-" * 14 + "NO RECORD" + "-" * 14)
        else:
            for record in filtered_records:
                print(f"{record['cat']:<20} {record['desc']:<20} {record['amt']:<10}")
                total_amt += record['amt']
            
        print("=" * 20 + " " + "=" * 20 + " " + "=" * 10)   
        print(f"The total amount above is: {total_amt}")