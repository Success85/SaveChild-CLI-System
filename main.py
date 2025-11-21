# main.py

import sys
from utils import clear_screen, pause
from data_handler import init_db, get_cursor, create_tables
import report_case
import officer
import emergency

def main_menu():    
    while True:
        clear_screen()
        print(" SAFECHILD CLI SYSTEM ".center(50, "="))
        print("1. Report Child Abuse")
        print("2. Check Case Status")
        print("3. Officer Login")
        print("4. Emergency Support")
        print("5. Exit")
        choice = input("Choice: ").strip()

        if choice == "1":
            report_case.report_new_case()
        elif choice == "2":
            report_case.check_case_status()
        elif choice == "3":
            officer.officer_login()
        elif choice == "4":
            emergency.show_emergency_menu()
        elif choice == "5":
            print("Goodbye!")
            sys.exit(0)
        else:
            print("Invalid choice.")
            pause()

def start_app():
    clear_screen()
    print("Initializing SafeChild CLI System...\n")
    try:
        init_db()
    except Exception as e:
        print(f"DB init failed: {e}")
        pause()
        return
    pause("Press Enter to launch the menu...")
    create_tables()
    main_menu()

if __name__ == "__main__":
    try:
        start_app()
    except KeyboardInterrupt:
        print("\nExited by user.")
        sys.exit(0)

