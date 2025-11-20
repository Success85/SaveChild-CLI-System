from data_handler import init_db


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
            view_assigned_cases(user['id'])
        elif choice == "2":
            view_pending_unassigned_cases()
        elif choice == "3":
            take_case(user['id'])
        elif choice == "4":
            update_case_status(username)
        elif choice == "5":
            print("Logging out...")
            break
        


# FUNCTION DEFINITIONS
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

def view_pending_unassigned_cases():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM cases WHERE status='Pending' AND assigned_officer_id IS NULL ORDER BY created_at")
    rows = cur.fetchall()
    if not rows:
        print("No pending unassigned cases.")
    else:
        for r in rows:
            print("----------------------------------------")
            print(f"Case ID: {r['case_id']} | Type: {r['abuse_type']} | Location: {r['location']}")
            print(f"Victim: {r['victim_name']} Age: {r['victim_age']}")
            print(f"Description: {r['description'][:120]}{'...' if len(r['description'])>120 else ''}")
    conn.close()
    pause()

def search_case():
    conn = init_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM cases WHERE case_id=%s", (case_id,))
    row = cursor.fetchone()

    if row:
        print(row)
    else:
        print("Case not found.")
    
        if row['assigned_officer_id'] == officer_id:
            print("You are already assigned to this case.")
        elif row['assigned_officer_id'] is not None:
            print("Case is already assigned to another officer.")
        else:
            cur.execute("UPDATE cases SET assigned_officer_id=?, status=?, last_updated=? WHERE id=?",
                        (officer_id, "Under Investigation", now_iso(), row['id']))
            conn.commit()
            print("Case assigned to you and status set to Under Investigation.")
    conn.close()
    pause()

    pause()


def filter_cases():
    conn = init_db()
    cursor = conn.cursor()
    status = input("Enter Status: ").strip()
    
    cursor.execute("SELECT * FROM cases WHERE case_status=%s", (status,))
    rows = cursor.fetchall()

    if row:
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
