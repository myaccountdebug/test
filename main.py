from db.sqlite import init_database, insert_fruits, get_all_fruits, delete_fruit, clear_all_fruits

def get_fruit_names():
    """Get fruit names from user input."""
    fruit_names = []
    print("\n=== Fruit Input ===")
    while True:
        fruit = input("Enter a fruit name (or type 'exit' to stop): ").strip()
        if fruit.lower() == 'exit':
            break
        if fruit and fruit.isalpha(): 
            fruit_names.append(fruit)
        else:
            print("Invalid input. Please enter only alphabetic characters.")
    return fruit_names


def display_menu():
    """Display the main menu."""
    print("\n=== Fruit Management System ===")
    print("1. Add fruits")
    print("2. View all fruits")
    print("3. Delete a fruit")
    print("4. Clear all fruits")
    print("5. Exit")
    return input("Choose an option (1-5): ").strip()


def add_fruits():
    """Add fruits to the database."""
    fruits = get_fruit_names()
    if fruits:
        results = insert_fruits(fruits)
        print("\n--- Insertion Results ---")
        for fruit, success in results:
            status = "✓ Added" if success else "✗ Already exists"
            print(f"{fruit}: {status}")
    else:
        print("No fruits entered.")


def view_all_fruits():
    """View all fruits in the database."""
    fruits = get_all_fruits()
    if fruits:
        print("\n--- All Fruits ---")
        for fruit_id, name, created_at in fruits:
            print(f"ID: {fruit_id}, Name: {name}, Created: {created_at}")
    else:
        print("No fruits in the database.")


def delete_single_fruit():
    """Delete a fruit from the database."""
    fruit_name = input("Enter the fruit name to delete: ").strip()
    if fruit_name and fruit_name.isalpha():
        success = delete_fruit(fruit_name)
        if success:
            print(f"✓ {fruit_name} deleted successfully.")
        else:
            print(f"✗ {fruit_name} not found in the database.")
    else:
        print("Invalid input.")


def main():
    """Main application loop."""
    init_database()
    print("Welcome to the Fruit Management System!")
    
    while True:
        choice = display_menu()
        
        if choice == '1':
            add_fruits()
        elif choice == '2':
            view_all_fruits()
        elif choice == '3':
            delete_single_fruit()
        elif choice == '4':
            confirm = input("Are you sure? This will delete all fruits (yes/no): ").strip().lower()
            if confirm == 'yes':
                clear_all_fruits()
                print("✓ All fruits cleared.")
            else:
                print("Cancelled.")
        elif choice == '5':
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please choose 1-5.")


if __name__ == '__main__':
    main()