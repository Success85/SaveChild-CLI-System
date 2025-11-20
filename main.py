#! /usr/bin/env python3

import sys
from data_handler import init_db
from utils import clear_screen, pause
import report
import officer
import admin
import emergency

def main_menu():
    """Displays the main CLI menu and routes user choices."""
    while True:
        clear_screen()
        print(" " * 50)
        print(" SAFECHILD CLI SYSTEM ".center(50))
        print(" " * 50)
        print("1️⃣  Report Child Abuse")
        print("2️⃣  Check Case Status")
        print("3️⃣  Officer Login")
        print("4️⃣  Admin Login")
        print("5️⃣  Emergency Support")
        print("6️⃣  Exit")
        print("=" * 50)

        choice = input("Select an option (1–6): ").strip()

        if choice == "1":
            report.report_case()
        elif choice == "2":
            report.check_case_status()
        elif choice == "3":
            officer.officer_login()
        elif choice == "4":
            admin.admin_login()
        elif choice == "5":
            emergency.emergency_support()
        elif choice == "6":
            print("\nThank you for using SafeChild CLI System.")
            print("Together, we protect children and save lives ❤️")
            sys.exit(0)
        else:
            print("\n Invalid option. Please enter 1–6.")
            pause()

def start_app():
    """Initializes DB and starts the main menu."""
    clear_screen()
    print("Initializing SafeChild CLI System...\n")
    try:
        init_db()
        print(" Database initialized successfully!")
    except Exception as e:
        print(f" Database initialization failed: {e}")
        pause()
        return

    pause("Press Enter to launch the system menu...")
    main_menu()


if __name__ == "__main__":
    try:
        start_app()
    except KeyboardInterrupt:
        print("\n\nApplication exited by user. Goodbye")
        sys.exit(0)
