import sys
    
from records import Records
from categories import Categories

records = Records()
categories = Categories()

records.initialize_balance()

while True:
    cmd = input("\nWhat do you want to do (add / view / delete / view categories / find / exit)? ")
    
    if cmd == "add":
        records.add(categories)
    elif cmd == "view":
        records.view()
    elif cmd == "delete":
        records.delete()
    elif cmd == "view categories":
        categories.view_categories(categories.list_categories)
    elif cmd == "find":
        category_name = input("Which category do you want to find? ")
        records.find(category_name, categories)
    elif cmd == "exit":
        records.save()
        break
    # Handle 11: User inputs invalid command
    else:
        sys.stderr.write('Invalid command. Try again.\n')