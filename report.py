# report.py
from data_handler import get_conn
from utils import clear_screen, pause, gen_case_id, now_iso

def report_case():
    clear_screen()
    print("=== Report a Child Abuse Case ===")
    reporter = input("Your name (reporter) [optional]: ").strip() or None
    reporter_contact = input("Your contact (phone/email) [optional]: ").strip() or None
    victim_name = input("Victim's name: ").strip()
    while True:
        try:
            victim_age = int(input("Victim age (years): ").strip())
            break
        except ValueError:
            print("Please enter a valid number for age.")
    victim_gender = input("Victim gender (M/F/Other): ").strip()
    print("Abuse type options: physical, sexual, domestic, trafficking, other")
    abuse_type = input("Type of abuse: ").strip().lower()
    location = input("Location (city / area): ").strip()
    description = input("Describe the incident: ").strip()
    case_id = gen_case_id()
    status = "Pending"
    created_at = now_iso()

    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO cases
        (case_id, reporter_name, reporter_contact, victim_name, victim_age, victim_gender, abuse_type, location, description, status, created_at, last_updated)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
    """, (case_id, reporter, reporter_contact, victim_name, victim_age, victim_gender, abuse_type, location, description, status, created_at, created_at))
    conn.commit()
    conn.close()

    print("\nThank you. Your report has been submitted.")
    print(f"Your Case ID is: {case_id}")
    print("Keep this ID to check status later.")
    pause()

def check_case_status():
    clear_screen()
    print("=== Check Case Status ===")
    case_id = input("Enter your Case ID: ").strip()
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM cases WHERE case_id = ?", (case_id,))
    row = cur.fetchone()
    if not row:
        print("No case found with that ID.")
    else:
        print(f"\nCase ID: {row['case_id']}")
        print(f"Victim: {row['victim_name']} (Age: {row['victim_age']}, Gender: {row['victim_gender']})")
        print(f"Type: {row['abuse_type']}")
        print(f"Location: {row['location']}")
        print(f"Status: {row['status']}")
        print(f"Reported at: {row['created_at']}")
        print(f"Last updated: {row['last_updated']}")
        print("Description:")
        print(row['description'] or "(No description)")

        cur.execute("SELECT n.note, n.created_at, u.full_name FROM notes n LEFT JOIN users u ON n.user_id=u.id WHERE n.case_id = ? ORDER BY n.created_at", (row['id'],))
        notes = cur.fetchall()
        if notes:
            print("\nProgress notes:")
            for n in notes:
                author = n['full_name'] or "Unknown"
                print(f"- {n['created_at']} by {author}: {n['note']}")
        else:
            print("\nNo progress notes yet.")
    conn.close()
    pause()
