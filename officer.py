# officer.py
from data_handler import get_conn
from utils import clear_screen, pause, verify_password
import getpass
from utils import now_iso

def officer_login():
    clear_screen()
    print("=== Officer Login ===")
    username = input("Username: ").strip()
    password = getpass.getpass("Password: ")
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username=? AND role='officer'", (username,))
    user = cur.fetchone()
    conn.close()
    if user and verify_password(user['password_hash'], password):
        return dict(user)
    else:
        print("Invalid officer credentials.")
        pause()
        return None

def officer_menu(user):
    while True:
        clear_screen()
        print(f"Officer Dashboard - {user['full_name'] or user['username']}")
        print("1. View My Assigned Cases")
        print("2. View Pending Unassigned Cases")
        print("3. Take / Assign Case to Me")
        print("4. Add Progress Note to a Case")
        print("5. Logout")
        choice = input("Choose: ").strip()
        if choice == "1":
            view_assigned_cases(user['id'])
        elif choice == "2":
            view_pending_unassigned_cases()
        elif choice == "3":
            take_case(user['id'])
        elif choice == "4":
            add_progress_note(user['id'])
        elif choice == "5":
            break
        else:
            print("Invalid choice.")
            pause()

def view_assigned_cases(officer_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM cases WHERE assigned_officer_id = ? ORDER BY created_at DESC", (officer_id,))
    rows = cur.fetchall()
    if not rows:
        print("No cases assigned to you yet.")
    else:
        for r in rows:
            print("----------------------------------------")
            print(f"Case ID: {r['case_id']} | Status: {r['status']} | Type: {r['abuse_type']}")
            print(f"Victim: {r['victim_name']} Age: {r['victim_age']} | Location: {r['location']}")
            print(f"Reported at: {r['created_at']} | Last updated: {r['last_updated']}")
    conn.close()
    pause()

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

def take_case(officer_id):
    conn = get_conn()
    cur = conn.cursor()
    case_id = input("Enter Case ID to take/assign to yourself: ").strip()
    cur.execute("SELECT id, status, assigned_officer_id FROM cases WHERE case_id=?", (case_id,))
    row = cur.fetchone()
    if not row:
        print("Case not found.")
    else:
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

def add_progress_note(user_id):
    conn = get_conn()
    cur = conn.cursor()
    case_id = input("Enter Case ID to add note to: ").strip()
    cur.execute("SELECT id, case_id, status FROM cases WHERE case_id=?", (case_id,))
    row = cur.fetchone()
    if not row:
        print("Case not found.")
        conn.close()
        pause()
        return
    note = input("Write your progress note (what was done, next steps): ").strip()
    cur.execute("INSERT INTO notes (case_id, user_id, note, created_at) VALUES (?,?,?,?)",
                (row['id'], user_id, note, now_iso()))
    cur.execute("UPDATE cases SET last_updated=? WHERE id=?", (now_iso(), row['id']))
    conn.commit()
    print("Note added.")
    conn.close()
    pause()
