
from data_handler import get_cursor

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin_Login111" 

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

    statuses = ["Pending", "Under Investigation", "In Court", "Resolved"]
    print("Select a new status:")
    for i, status in enumerate(statuses, 1):
        print("{}. {}".format(i, status))

    try:
        choice = int(input("Enter choice (1-4): "))
        if 1 <= choice <= 4:
            new_status = statuses[choice - 1]
            
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
            
        else:
            print("Invalid choice. Please select a number between 1 and 4.")
    except ValueError:
        print("Invalid input. Please enter a number.")
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
    else:
        print("Deletion cancelled.")

def admin_menu():
    if not login():
        return

    while True:
        print("\n=== Admin Dashboard (MySQL) ===")
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
