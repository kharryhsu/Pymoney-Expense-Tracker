balance = int(input("how much money do you have? ")) # receive input as integer

print("Add an expense or income record with description and amount:") 
print("desc1 amt1, desc2 amt2, desc3 amt3, ...")

items_list = input().split(', ') # split input with comma
items_list = [tuple(item.split(' ')) for item in items_list] # iterate item in items_list and split item with blank and convert to tuple

print("Here's your expense ans income records:")

for desc, amt in items_list: # iterate description and amount in items_list
    print(f"{desc} {amt}")
    balance += int(amt) # add amount of each of items into the balance
    
print(f"Now you have {balance} dollars.")