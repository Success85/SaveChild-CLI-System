# main.py
from data_handler import init_db
import report
import officer
import admin
import emergency
from utils import clear_screen, pause
import sys

def main_menu():
    while True:
        clear_screen()
        print("*** SaveChild: CHILD ABUSE REPORTING SYSTEM ***")
        print("1. Report a Case")
        print("2. Check Case Status")
        print("3. Officer Login")
        print("4. Admin Login")
        print("5. Emergency Support")
        print("6. Exit")
        choice = input(">>> Enter your choice: ").strip()
        if choice == "1":
            report.report_case()
        elif choice == "2":
            report.check_case_status()
        elif choice == "3":
            user = officer.officer_login()
            if user:
                officer.officer_menu(user)
        elif choice == "4":
            user = admin.admin_login()
            if user:
                admin.admin_menu(user)
        elif choice == "5":
            emergency.emergency_support()
        elif choice == "6":
            print("Exiting. Stay safe.")
            break
        else:
            print("Invalid option. Please try again.")
            pause()

if __name__ == "__main__":
    init_db()
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)
