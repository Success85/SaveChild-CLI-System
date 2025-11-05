# admin.py
from data_handler import get_conn
from utils import clear_screen, pause, verify_password
import getpass
from utils import now_iso

def admin_login():
    clear_screen()
    print("=== Admin Login ===")
    username = input("Username: ").strip()
    password = getpass.getpass("Password: ")
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username=? AND role='admin'", (username,))
    user = cur.fetchone()
    conn.close()
    if user and verify_password(user['password_hash'], password):
        return dict(user)
    else:
        print("Invalid admin credentials.")
        pause()
        return None

def admin_menu(user):
    while True:
        clear_screen()
        print(f"Admin Dashboard - {user['full_name'] or user['username']}")
        print("1. View All Cases")
        print("2. View Cases by Status")
        print("3. Assign Case to Officer")
        print("4. Update Case Status")
        print("5. Create Officer Account")
        print("6. Remove Resolved Case")
        print("7. Logout")
        choice = input("Choose: ").strip()
        if choice == "1":
            admin_view_all_cases()
        elif choice == "2":
            admin_view_cases_by_status()
        elif choice == "3":
            admin_assign_case()
        elif choice == "4":
            admin_update_case_status()
        elif choice == "5":
            admin_create_officer()
        elif choice == "6":
            admin_remove_resolved_case()
        elif choice == "7":
            break
        else:
            print("Invalid choice.")
            pause()

def admin_view_all_cases():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""SELECT c.*, u.full_name as officer_name FROM cases c
                   LEFT JOIN users u ON c.assigned_officer_id = u.id
                   ORDER BY c.created_at DESC""")
    rows = cur.fetchall()
    if not rows:
        print("No cases in system.")
    else:
        for r in rows:
            print("----------------------------------------")
            print(f"Case ID: {r['case_id']} | Status: {r['status']} | Type: {r['abuse_type']}")
            print(f"Victim: {r['victim_name']} Age: {r['victim_age']} | Location: {r['location']}")
            print(f"Assigned officer: {r['officer_name'] or 'None'}")
            print(f"Reported at: {r['created_at']} | Last updated: {r['last_updated']}")
    conn.close()
    pause()

def admin_view_cases_by_status():
    status = input("Enter status (Pending, Under Investigation, In Court, Resolved): ").strip()
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM cases WHERE status = ? ORDER BY created_at DESC", (status,))
    rows = cur.fetchall()
    if not rows:
        print(f"No cases with status '{status}'.")
    else:
        for r in rows:
            print("----------------------------------------")
            print(f"{r['case_id']} | {r['victim_name']} | {r['abuse_type']} | {r['location']} | reported: {r['created_at']}")
    conn.close()
    pause()

def admin_assign_case():
    conn = get_conn()
    cur = conn.cursor()
    case_id = input("Enter Case ID to assign: ").strip()
    cur.execute("SELECT id, assigned_officer_id FROM cases WHERE case_id=?", (case_id,))
    r = cur.fetchone()
    if not r:
        print("Case not found.")
        conn.close()
        pause()
        return
    print("Officers available:")
    cur.execute("SELECT id, username, full_name FROM users WHERE role='officer'")
    officers = cur.fetchall()
    if not officers:
        print("No officers in system. Create one first.")
        conn.close()
        pause()
        return
    for o in officers:
        print(f"{o['id']}. {o['full_name'] or o['username']} ({o['username']})")
    try:
        chosen = int(input("Enter officer id to assign: ").strip())
    except ValueError:
        print("Invalid input.")
        conn.close()
        pause()
        return
    cur.execute("SELECT id FROM users WHERE id=? AND role='officer'", (chosen,))
    if not cur.fetchone():
        print("Officer not found.")
    else:
        cur.execute("UPDATE cases SET assigned_officer_id=?, status=?, last_updated=? WHERE id=?",
                    (chosen, "Under Investigation", now_iso(), r['id']))
        conn.commit()
        print("Case assigned.")
    conn.close()
    pause()

def admin_update_case_status():
    conn = get_conn()
    cur = conn.cursor()
    case_id = input("Enter Case ID to update status: ").strip()
    cur.execute("SELECT id, status FROM cases WHERE case_id=?", (case_id,))
    row = cur.fetchone()
    if not row:
        print("Case not found.")
        conn.close()
        pause()
        return
    print(f"Current status: {row['status']}")
    print("Valid transitions: Pending -> Under Investigation -> In Court -> Resolved")
    new_status = input("Enter new status: ").strip()
    if new_status not in ("Pending", "Under Investigation", "In Court", "Resolved"):
        print("Invalid status.")
    else:
        cur.execute("UPDATE cases SET status=?, last_updated=? WHERE id=?", (new_status, now_iso(), row['id']))
        conn.commit()
        print("Status updated.")
    conn.close()
    pause()

def admin_create_officer():
    conn = get_conn()
    cur = conn.cursor()
    username = input("New officer username: ").strip()
    password = getpass.getpass("New officer password: ").strip()
    full_name = input("Officer full name [optional]: ").strip() or None
    try:
        cur.execute("INSERT INTO users (username, password_hash, role, full_name, created_at) VALUES (?,?,?,?,?)",
                    (username, hash_password(password), 'officer', full_name, now_iso()))
        conn.commit()
        print("Officer account created.")
    except Exception:
        print("Error creating officer (username may exist).")
    conn.close()
    pause()

def admin_remove_resolved_case():
    conn = get_conn()
    cur = conn.cursor()
    case_id = input("Enter Case ID to remove (must be Resolved): ").strip()
    cur.execute("SELECT id, status FROM cases WHERE case_id=?", (case_id,))
    row = cur.fetchone()
    if not row:
        print("Case not found.")
    elif row['status'] != 'Resolved':
        print("Case is not Resolved. Only resolved cases can be removed.")
    else:
        confirm = input("Are you sure you want to permanently delete this resolved case? (yes/no): ").strip().lower()
        if confirm == 'yes':
            cur.execute("DELETE FROM notes WHERE case_id=?", (row['id'],))
            cur.execute("DELETE FROM cases WHERE id=?", (row['id'],))
            conn.commit()
            print("Case and associated notes removed.")
        else:
            print("Cancelled.")
    conn.close()
    pause()
