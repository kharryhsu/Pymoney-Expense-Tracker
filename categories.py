class Categories:
    
    """Maintain the category list and provide methods for managing categories."""
    def __init__(self):
        """Initialize and return the predefined category hierarchy."""
        self._categories = ['expense', ['food', ['meal', 'snack', 'drink'], 'transportation', ['bus', 'railway']], 'income', ['salary', 'bonus']]
    
    @property
    def list_categories(self):
        return self._categories
    
    def view_categories(self, categories, level=0):
        """Recursively display the category hierarchy."""
        if categories == None:
            return
        
        if type(categories) == list:
            for child in categories:
                self.view_categories(child, level + 1)
        else:
            print(f'{" " * (level - 1) + "- "}{categories}')

    def is_category_valid(self, category_name, categories):
        """Check if a category exists in the hierarchy."""
        if type(categories) == list:
            for item in categories:
                if item == category_name:
                    return True
                if type(item) == list and self.is_category_valid(category_name, item):
                    return True
        return False
    
    def find_subcategories(self, category_name, categories):
        def find_subcategories_gen(category, categories, found=False):
            if type(categories) == list:
                for index, child in enumerate(categories):
                    # Recursively process each child, updating the "found" flag as needed
                    yield from find_subcategories_gen(category, child, found)
                    
                    # If the current child matches the target category
                    if child == category and index + 1 < len(categories) and type(categories[index + 1]) == list:
                        # Recursively process subcategories with the "found" flag set to True
                        yield from find_subcategories_gen(category, categories[index + 1], True)
            else:
                # Yield the target category or any subcategories if "found" is True
                if categories == category or found:
                    yield categories

        # Return a list of all subcategories found
        return [i for i in find_subcategories_gen(category_name, categories)]