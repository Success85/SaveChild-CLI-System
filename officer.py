from data_handler import init_db
from utils import pause

# Officers for login
officers = {"officer1": "901", "officer2": "902"}
current_officer = None
officer_id = None


# OFFICER LOGIN
def officer_login():
    print("\n--- OFFICER LOGIN ---")
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    if username in officers and officers[username] == password:
        print(f"Welcome Officer {username}!")
        global current_officer
        global officer_id
        current_officer = username 

        officer_menu(username)
    else:
        print("Invalid username or password")
        pause()


# OFFICER MENU 
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
            update_case_status()
        elif choice == "5":
            print("Logging out...")
            break
        


# FUNCTION DEFINITIONS
def view_all_cases():
    conn = init_db()
    cursor = conn.cursor()
    cursor.execute("SELECT case_id, first_name, last_name, age, gender, location, abuse_type,case_status, date_reported,status_updated_by FROM cases")
    rows = cursor.fetchall()

    if rows:
        print("\n--- All Cases ---")
        for row in rows:
                case_id, first_name, last_name, age, gender, location, abuse_type,case_status, date_reported, status_updated_by = row
                print(f"ID:{case_id} | {first_name} {last_name} | Age:{age} | Gender:{gender} | "
                  f"Location:{location} | Abuse:{abuse_type} |"
                  f"Status:{case_status} | Reported:{date_reported} | Status updated by: {status_updated_by}")
    else:
        print("No cases found.")

    pause("Press Enter to return to Officer Menu...")

def search_case():
    conn = init_db()
    cursor = conn.cursor()
    case_id = input ("Enter ID: ")
    cursor.execute("SELECT case_id, first_name, last_name, age, location, abuse_type, status, date_reported, follow_up_note, status_updated_by  FROM cases WHERE case_id=%s", (case_id,))
    row = cursor.fetchone()

    if row:
        case_id, first_name, last_name, age, location, abuse_type, status, date_reported, follow_up_note, status_updated_by = row
        print("\n------ CASE DETAILS ------")
        print(f"Case ID     : {case_id}")
        print(f"First Name  : {first_name}")
        print(f"Last Name   : {last_name}")
        print(f"Age         : {age}")
        print(f"Location    : {location}")
        print(f"Abuse Type  : {abuse_type}")
        print(f"Status      : {status}")
        print(f"Submitted on  : {date_reported}")
        print(f"Status      : {status}")
        print(f"note     : {follow_up_note}")
        print(f"Status updated by     : {status_updated_by}")
        print("---------------------")
    else:
        print("Case not found.")
    
    conn.close()
    pause()


def filter_cases():
    conn = init_db()
    cursor = conn.cursor()
    status = input("Enter Status: ").strip()
    
    cursor.execute("SELECT case_id, first_name, last_name, age, gender, location, abuse_type,case_status, date_reported,status_updated_by FROM cases WHERE case_status=%s", (status,))
    rows = cursor.fetchall()

    if rows:
        case_id, first_name, last_name, age, location, abuse_type, status, date_reported, status_updated_by = row
        for row in rows:

            print("\n------ CASE DETAILS ------")
            print(f"Case ID     : {case_id}")
            print(f"First Name  : {first_name}")
            print(f"Last Name   : {last_name}")
            print(f"Age         : {age}")
            print(f"Location    : {location}")
            print(f"Abuse Type  : {abuse_type}")
            print(f"Status      : {status}")
            print(f"Submitted on  : {date_reported}")
            print(f"Status updated by     : {status_updated_by}")

    else:
        print("No cases found.")

    pause()


def update_case_status():
    """
    Update the case status AND automatically add a follow-up note.
    """
    global current_officer
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
            follow_up_note = CONCAT(IFNULL(follow_up_note, ''), ' | ', %s),
            status_updated_by = %s
        WHERE case_id = %s
    """
    cursor.execute(query, (status, note, current_officer, case_id))
    conn.commit()
    print(f"Case updated to '{status}' with follow-up note by {current_officer}.")
    pause()
