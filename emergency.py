# emergency.py
from data_handler import get_conn
from utils import clear_screen, pause

def emergency_support():
    clear_screen()
    print("=== Emergency Support ===")
    print("Enter abuse type and your location to get helpline contacts.")
    abuse_type = input("Abuse type (physical/sexual/domestic/trafficking/general): ").strip().lower() or "general"
    location = input("Your location (city / area) [leave blank for Any]: ").strip() or "Any"
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT contact, abuse_type, location FROM helplines WHERE abuse_type=? AND (location=? OR location='Any')", (abuse_type, location))
    rows = cur.fetchall()
    if not rows:
        cur.execute("SELECT contact, abuse_type, location FROM helplines WHERE abuse_type=? OR location='Any'", (abuse_type,))
        rows = cur.fetchall()
    if not rows:
        print("No helplines found for that query.")
    else:
        print("\nMatches:")
        for r in rows:
            print(f"- [{r['abuse_type']}] ({r['location']}) -> {r['contact']}")
    conn.close()
    pause()
