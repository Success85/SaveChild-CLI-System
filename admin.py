<<<<<<< HEAD
# Coded by Cedric (so please if it doesn't work ask god not me cause I'm just as confused)

import data_handler  

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin_work_sucks" 

def login():
    """
    Handles the admin login process.
    Returns True if login is successful, False otherwise.
    """
=======

from data_handler import get_cursor

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin_Login111" 

def login():

>>>>>>> 20b9d786c9acd41f73532b36ca18df52193607a4
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
<<<<<<< HEAD
    """
    Fetches and displays all reports from the data handler.
    """
    print("\n--- All Submitted Reports ---")
    reports = data_handler.read_reports() 
    
    if not reports:
        print("No reports found.")
        return

    for report in reports:
        print("-" * 20)
        print("Case ID: {}".format(report.get('case_id')))
        print("Status: {}".format(report.get('status')))
        print("Location: {}".format(report.get('location')))
        print("Abuse Type: {}".format(report.get('abuse_type')))
        print("Description: {}".format(report.get('description')))
    print("-" * 20)


def update_report_status():
    """
    Updates the status of a specific report.
    """
    print("\n--- Update Report Status ---")
    case_id = input("Enter the Case ID of the report to update: ")
    
=======
    print("\n--- All Submitted Reports ---")
    
    try:
        conn = get_cursor() 
        cursor = get_cursor() 
        
        query = "SELECT case_id, first_name, last_name, location, abuse_type, case_status FROM cases"
        cursor.execute(query)
        
        rows = cursor.fetchall()

        if not rows:
            print("No reports found in database.")
        else:
            for row in rows:
                print("-" * 20)
                print("Case ID: {}".format(row[0]))
                print("Name: {} {}".format(row[1], row[2]))
                print("Location: {}".format(row[3]))
                print("Abuse Type: {}".format(row[4]))
                print("Status: {}".format(row[5]))
            print("-" * 20)
            
        cursor.close()

    except Exception as e:
        print("Error fetching reports: {}".format(e))


def update_report_status():
    print("\n--- Update Report Status ---")
    case_id = input("Enter the Case ID of the report to update: ")

>>>>>>> 20b9d786c9acd41f73532b36ca18df52193607a4
    statuses = ["Pending", "Under Investigation", "In Court", "Resolved"]
    print("Select a new status:")
    for i, status in enumerate(statuses, 1):
        print("{}. {}".format(i, status))

    try:
        choice = int(input("Enter choice (1-4): "))
        if 1 <= choice <= 4:
            new_status = statuses[choice - 1]
            
<<<<<<< HEAD
            if data_handler.update_status(case_id, new_status):
                print("Successfully updated Case ID {} to '{}'.".format(case_id, new_status))
            else:
                print("Error: Case ID {} not found.".format(case_id))
=======
            cursor = get_cursor()
            
            check_query = "SELECT case_id FROM cases WHERE case_id = %s"
            cursor.execute(check_query, (case_id,))
            
            if cursor.fetchone():
                update_query = "UPDATE cases SET case_status = %s WHERE case_id = %s"
                cursor.execute(update_query, (new_status, case_id))
                
                cursor._connection.commit()
                
                print("Successfully updated Case ID {} to '{}'.".format(case_id, new_status))
            else:
                print("Error: Case ID {} not found.".format(case_id))
            
            cursor.close()
            
>>>>>>> 20b9d786c9acd41f73532b36ca18df52193607a4
        else:
            print("Invalid choice. Please select a number between 1 and 4.")
    except ValueError:
        print("Invalid input. Please enter a number.")
<<<<<<< HEAD

def delete_report():
    """
    Deletes a specific report by its Case ID.
    """
    print("\n--- Delete Report ---")
    case_id = input("Enter the Case ID of the report to DELETE: ")
    

    confirm = input("Are you sure you want to PERMANENTLY delete Case ID {}? (yes/no): ".format(case_id)).lower()
    
    if confirm == 'yes':
        if data_handler.delete_report(case_id): 
            print("Successfully deleted Case ID {}.".format(case_id))
        else:
            print("Error: Case ID {} not found.".format(case_id))
=======
    except Exception as e:
        print("Database Error: {}".format(e))

def delete_report():
    print("\n--- Delete Report ---")
    case_id = input("Enter the Case ID of the report to DELETE: ")

    confirm = input("Are you sure you want to PERMANENTLY delete Case ID {}? (yes/no): ".format(case_id)).lower()

    if confirm == 'yes':
        try:
            cursor = get_cursor()
            
            check_query = "SELECT case_id FROM cases WHERE case_id = %s"
            cursor.execute(check_query, (case_id,))
            
            if cursor.fetchone():
                delete_query = "DELETE FROM cases WHERE case_id = %s"
                cursor.execute(delete_query, (case_id,))
                
                cursor._connection.commit()
                
                print("Successfully deleted Case ID {}.".format(case_id))
            else:
                print("Error: Case ID {} not found.".format(case_id))
            
            cursor.close()
            
        except Exception as e:
            print("Database Error: {}".format(e))
>>>>>>> 20b9d786c9acd41f73532b36ca18df52193607a4
    else:
        print("Deletion cancelled.")

def admin_menu():
<<<<<<< HEAD
    """
    The main menu for the admin after logging in.
    """
    if not login():
        return 

    while True:
        print("\n=== Admin Dashboard ===")
=======
    if not login():
        return

    while True:
        print("\n=== Admin Dashboard (MySQL) ===")
>>>>>>> 20b9d786c9acd41f73532b36ca18df52193607a4
        print("1. View all reports")
        print("2. Update a report status")
        print("3. Delete a report")
        print("4. Logout and return to Main Menu")
<<<<<<< HEAD
        
=======

>>>>>>> 20b9d786c9acd41f73532b36ca18df52193607a4
        choice = input("Enter your choice (1-4): ")

        if choice == '1':
            view_all_reports()
        elif choice == '2':
            update_report_status()
        elif choice == '3':
            delete_report()
        elif choice == '4':
            print("Logging out...")
<<<<<<< HEAD
            break 
=======
            break
>>>>>>> 20b9d786c9acd41f73532b36ca18df52193607a4
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

if __name__ == "__main__":
    print("Testing admin.py module...")
    admin_menu()
