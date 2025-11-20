<<<<<<< HEAD
<<<<<<<<< Temporary merge branch 1
# Coded by Cedric (so please if it doesn't work ask god not me cause I'm just as confused)

import data_handler  
=======
from data_handler import get_cursor
from utils import clear_screen, pause
>>>>>>> 3c95f5360ae593e36408aa68e765c383e719bf9b

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin_work_sucks"

def login():
    """
    Handles the admin login process.
    """
<<<<<<< HEAD
=========

from data_handler import get_cursor

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin_Login111" 

def login():

>>>>>>>>> Temporary merge branch 2
    print("\n--- Admin Login ---")
    username = input("Enter username: ")
    password = input("Enter password: ")
=======
    clear_screen()
    print("=== Admin Login ===")
    username = input("Username: ").strip()
    password = input("Password: ").strip()
>>>>>>> 3c95f5360ae593e36408aa68e765c383e719bf9b

    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        print("Login successful. Welcome, Admin!")
        return True
    else:
        print("Invalid username or password.")
        pause()
        return False

def view_all_reports():
<<<<<<< HEAD
<<<<<<<<< Temporary merge branch 1
=======
>>>>>>> 3c95f5360ae593e36408aa68e765c383e719bf9b
    """
    Fetches and displays all reports directly from MySQL.
    """
<<<<<<< HEAD
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
    
=========
    print("\n--- All Submitted Reports ---")
    
=======
>>>>>>> 3c95f5360ae593e36408aa68e765c383e719bf9b
    try:
        conn, cursor = get_cursor() 
        
        print("\n--- All Submitted Reports ---")
        
        query = "SELECT case_id, first_name, last_name, location, abuse_type, case_status FROM cases"
        cursor.execute(query)
        rows = cursor.fetchall()

        if not rows:
            print("No reports found in database.")
        else:
            for row in rows:
                print("-" * 40)
                print("Case ID: {} | Status: {}".format(row[0], row[5]))
                print("Name: {} {} | Loc: {}".format(row[1], row[2], row[3]))
                print("Abuse Type: {}".format(row[4]))
            
        cursor.close()

    except Exception as e:
        print("Database Error: {}".format(e))
    
    pause()

def update_report_status():
    print("\n--- Update Report Status ---")
<<<<<<< HEAD
    case_id = input("Enter the Case ID of the report to update: ")

>>>>>>>>> Temporary merge branch 2
=======
    case_id = input("Enter Case ID: ").strip()
    
>>>>>>> 3c95f5360ae593e36408aa68e765c383e719bf9b
    statuses = ["Pending", "Under Investigation", "In Court", "Resolved"]
    print("Select a new status:")
    for i, status in enumerate(statuses, 1):
        print("{}. {}".format(i, status))

    try:
        choice = int(input("Choice (1-4): "))
        if 1 <= choice <= 4:
            new_status = statuses[choice - 1]
            
<<<<<<< HEAD
<<<<<<<<< Temporary merge branch 1
            if data_handler.update_status(case_id, new_status):
                print("Successfully updated Case ID {} to '{}'.".format(case_id, new_status))
            else:
                print("Error: Case ID {} not found.".format(case_id))
=========
            cursor = get_cursor()
=======
            conn, cursor = get_cursor()
>>>>>>> 3c95f5360ae593e36408aa68e765c383e719bf9b
            
            cursor.execute("SELECT case_id FROM cases WHERE case_id = %s", (case_id,))
            if not cursor.fetchone():
                print("Error: Case ID not found.")
            else:
                cursor.execute("UPDATE cases SET case_status = %s WHERE case_id = %s", (new_status, case_id))
                
                conn.commit()
                print("Successfully updated Case ID {} to '{}'.".format(case_id, new_status))
            
            cursor.close()
        else:
            print("Invalid choice.")
            
<<<<<<< HEAD
>>>>>>>>> Temporary merge branch 2
        else:
            print("Invalid choice. Please select a number between 1 and 4.")
    except ValueError:
        print("Invalid input. Please enter a number.")
<<<<<<<<< Temporary merge branch 1

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
=========
=======
    except ValueError:
        print("Invalid input.")
>>>>>>> 3c95f5360ae593e36408aa68e765c383e719bf9b
    except Exception as e:
        print("Database Error: {}".format(e))
    
    pause()

def delete_report():
    print("\n--- Delete Report ---")
    case_id = input("Enter Case ID to DELETE: ")

    confirm = input("Are you sure you want to PERMANENTLY delete Case ID {}? (yes/no): ".format(case_id)).lower()

    if confirm == 'yes':
        try:
            conn, cursor = get_cursor()
            
            cursor.execute("SELECT case_id FROM cases WHERE case_id = %s", (case_id,))
            if not cursor.fetchone():
                print("Error: Case ID not found.")
            else:
                cursor.execute("DELETE FROM cases WHERE case_id = %s", (case_id,))
                
                conn.commit()
                print("Successfully deleted Case ID {}.".format(case_id))
            
            cursor.close()
            
        except Exception as e:
            print("Database Error: {}".format(e))
<<<<<<< HEAD
>>>>>>>>> Temporary merge branch 2
=======
>>>>>>> 3c95f5360ae593e36408aa68e765c383e719bf9b
    else:
        print("Deletion cancelled.")
    
    pause()

def admin_menu():
<<<<<<< HEAD
<<<<<<<<< Temporary merge branch 1
    """
    The main menu for the admin after logging in.
    """
    if not login():
        return 

    while True:
        print("\n=== Admin Dashboard ===")
=========
=======
>>>>>>> 3c95f5360ae593e36408aa68e765c383e719bf9b
    if not login():
        return

    while True:
<<<<<<< HEAD
        print("\n=== Admin Dashboard (MySQL) ===")
>>>>>>>>> Temporary merge branch 2
        print("1. View all reports")
        print("2. Update a report status")
        print("3. Delete a report")
        print("4. Logout and return to Main Menu")
<<<<<<<<< Temporary merge branch 1
        
=========

>>>>>>>>> Temporary merge branch 2
        choice = input("Enter your choice (1-4): ")
=======
        clear_screen()
        print("=== Admin Dashboard (MySQL) ===")
        print("1. View all reports")
        print("2. Update a report status")
        print("3. Delete a report")
        print("4. Logout")

        choice = input("Enter choice: ").strip()
>>>>>>> 3c95f5360ae593e36408aa68e765c383e719bf9b

        if choice == '1':
            view_all_reports()
        elif choice == '2':
            update_report_status()
        elif choice == '3':
            delete_report()
        elif choice == '4':
            print("Logging out...")
<<<<<<< HEAD
<<<<<<<<< Temporary merge branch 1
            break 
=========
            break
>>>>>>>>> Temporary merge branch 2
=======
            break
>>>>>>> 3c95f5360ae593e36408aa68e765c383e719bf9b
        else:
            print("Invalid choice.")
            pause()

if __name__ == "__main__":
    admin_menu()


