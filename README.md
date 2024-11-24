# Pymoney-Expense-Tracker

This program is a simple financial records management tool made by python that allows users to track expenses and incomes. Users can add, view, delete, and search for records by category, manage their budget, and view a predefined category hierarchy.

## Features

- **Add Records**: Add expense or income records with category, description, and amount.
- **View Records**: Display all current records along with their details and the total balance.
- **Delete Records**: Remove specific records by their ID.
- **View Categories**: Display a predefined hierarchical list of categories (e.g., `expense -> food -> meal`).
- **Find Records by Category**: Search for records under a specific category or its subcategories.
- **Error Handling**: Handles various invalid inputs gracefully, such as file errors, invalid formats, and more.
- **Persistent Storage**: Records are saved to a file (`records.txt`) and loaded upon restart.

## Commands

- `add`: Add new records. Input format: `cat1 desc1 amt1, cat2 desc2 amt2, ...`
- `view`: View all records and the current balance.
- `delete`: Remove a specific record by entering its ID.
- `view categories`: Display the predefined category hierarchy.
- `find`: Search for records under a specific category or its subcategories.
- `exit`: Save all records to `records.txt` and exit the program.

## File Format (`records.txt`)

- **First Line**: Stores the initial balance (integer).
- **Subsequent Lines**: Each line represents a record in the format:

## Example Workflow

1. Start the program and initialize the balance.
2. Add records such as `food breakfast -50, salary job 2000`.
3. View all records to check the balance and details.
4. Delete a specific record by ID.
5. Use `view categories` to check available categories.
6. Use `find` to filter records by category.
7. Exit the program to save all changes.

## Future Enhancements

- Allow dynamic addition and removal of categories.
- Add export functionality to generate reports.
- Implement a graphical user interface (GUI).
