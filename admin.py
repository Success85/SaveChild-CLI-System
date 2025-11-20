# Coded by Cedric (so please if it doesn't work ask god not me cause I'm just as confused)

import data_handler

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin_Login123" 

def login():
    print("\n--- Admin Login ---")
    username = input("Enter username: ")
    password = input("Enter password: ")

    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        print("Login successful. Welcome, Admin!")
        return True
    else:
        print("Invalid username or password.")
        return False

def view_all_reports():
    print("\n--- All Submitted Reports ---")
    reports = data_handler.read_reports()

    if not reports:
        print("No reports found in database.")
        return

    for report in reports:
        print("-" * 20)
        print("Case ID: {}".format(report.get('case_id')))
        
        full_name = "{} {}".format(report.get('first_name'), report.get('last_name'))
        print("Name: {}".format(full_name))
        
        print("Status: {}".format(report.get('status')))
        print("Location: {}".format(report.get('location')))
        print("Abuse Type: {}".format(report.get('abuse_type')))
        print("Description: {}".format(report.get('description')))
    print("-" * 20)


def update_report_status():
    print("\n--- Update Report Status ---")
    case_id = input("Enter the Case ID of the report to update: ")

    statuses = ["Pending", "Under Investigation", "In Court", "Resolved"]
    print("Select a new status:")
    for i, status in enumerate(statuses, 1):
        print("{}. {}".format(i, status))

    try:
        choice = int(input("Enter choice (1-4): "))
        if 1 <= choice <= 4:
            new_status = statuses[choice - 1]

            if data_handler.update_status(case_id, new_status):
                print("Successfully updated Case ID {} to '{}'.".format(case_id, new_status))
            else:
                print("Error: Case ID {} not found.".format(case_id))
        else:
            print("Invalid choice. Please select a number between 1 and 4.")
    except ValueError:
        print("Invalid input. Please enter a number.")

def delete_report():
    print("\n--- Delete Report ---")
    case_id = input("Enter the Case ID of the report to DELETE: ")

    confirm = input("Are you sure you want to PERMANENTLY delete Case ID {}? (yes/no): ".format(case_id)).lower()

    if confirm == 'yes':
        if data_handler.delete_report(case_id):
            print("Successfully deleted Case ID {}.".format(case_id))
        else:
            print("Error: Case ID {} not found.".format(case_id))
    else:
        print("Deletion cancelled.")

def admin_menu():
    if not login():
        return

    while True:
        print("\n=== Admin Dashboard ===")
        print("1. View all reports")
        print("2. Update a report status")
        print("3. Delete a report")
        print("4. Logout and return to Main Menu")

        choice = input("Enter your choice (1-4): ")

        if choice == '1':
            view_all_reports()
        elif choice == '2':
            update_report_status()
        elif choice == '3':
            delete_report()
        elif choice == '4':
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

if __name__ == "__main__":
    print("Testing admin.py module...")
    admin_menu()
