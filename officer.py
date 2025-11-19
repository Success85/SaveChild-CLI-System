from data_handler import init_db
from utils import pause
# Officers for login
officers = {"officer1": "901", "officer2": "902"}

# OFFICER LOGIN
def officer_login():
    print("\n--- OFFICER LOGIN ---")
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    if username in officers and officers[username] == password:
        print(f"Welcome Officer {username}!")
        officer_menu(username)
    else:
        print("Invalid username/password")
        pause()


#  OFFICER MENU
def officer_menu(username):
    while True:
        print("\n--- OFFICER MENU ---")
        print("1. View All Cases")
        print("2. Search Case by ID")
        print("3. Filter Cases by Status")
        print("4. Update Case Status & Add Follow-up Note")
        print("5. Logout")
        choice = input("Choice: ").strip()

        if choice == "1":
            view_all_cases()
        elif choice == "2":
            search_case()
        elif choice == "3":
            filter_cases()
        elif choice == "4":
            update_case_status(username)
        elif choice == "5":
            print("Logging out...")
            break
       else:
            print("Invalid choice. Try again.")


#FUNCTION DEFINITIONS
def view_all_cases():
    conn = init_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cases")
    rows = cursor.fetchall()

    if rows:
        print("\n--- All Cases ---")
        for row in rows:
            case_id, first_name, last_name, age, gender, location, abuse_type, follow_up, case_status, date_reported, follow_up_by, status_updated_by = row
            print(f"ID:{case_id} | {first_name} {last_name} | Age:{age} | Gender:{gender} | "
                  f"Location:{location} | Abuse:{abuse_type} | Follow-up:{follow_up} | "
                  f"Status:{case_status} | Reported:{date_reported} | Followed-up by:{follow_up_by} | Status updated by:{status_updated_by}")
    else:
        print("No cases found.")

    pause("Press Enter to return to Officer Menu...")


def search_case():
    conn = init_db()
    cursor = conn.cursor()
    case_id = input("Enter Case ID: ").strip()
    
    cursor.execute("SELECT * FROM cases WHERE case_id=%s", (case_id,))
    row = cursor.fetchone()

    if row:
        print(row)
    else:
        print("Case not found.")

    pause()


def filter_cases():
    conn = init_db()
    cursor = conn.cursor()
    status = input("Enter Status: ").strip()
    
    cursor.execute("SELECT * FROM cases WHERE case_status=%s", (status,))
    rows = cursor.fetchall()

    if rows:
        for row in rows:
            print(row)
    else:
        print("No cases found.")

    pause()


def update_case_status():
    """
    Update the case status AND automatically add a follow-up note.
    """
    conn = init_db()
    cursor = conn.cursor()
    case_id = input("Enter Case ID: ").strip()
    if not case_id:
        print("Case ID cannot be empty.")
        return

    status = input("New Status: ").strip()
    note = input("Follow-up Note: ").strip()
    if not status or not note:
        print("Status and follow-up note cannot be empty.")
        return

    query = """
        UPDATE cases
        SET case_status = %s,
            follow_up = CONCAT(IFNULL(follow_up, ''), ' | ', %s),
            follow_up_by = %s,
            status_updated_by = %s
        WHERE case_id = %s
    """
    cursor.execute(query, (status, note, username, username, case_id))
    conn.commit()
    print(f"Case updated to '{status}' with follow-up note by {username}.")
    pause()