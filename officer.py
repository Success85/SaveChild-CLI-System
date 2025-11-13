#!/usr/bin/env python3
#officer operations

officers = {
    "officer1": "901",
    "officer2": "902"
}

cases = [
    {
        "case_id": "C001",
        "victim_name": "Alice",
        "location": "Nigeria",
        "abuse_type": "Physical",
        "status": "Pending",
        "notes": []
    },
    {
        "case_id": "C002",
        "victim_name": "Clary",
        "location": "Ghana",
        "abuse_type": "Sexual",
        "status": "Under Investigation",
        "notes": ["Visited location", "Interviewed victim"]
    }
]

# Officer login 
def officer_login():
    print("\n--- OFFICER LOGIN ---")
    username = input("Enter username: ")
    password = input("Enter password: ")

    if username in officers and officers[username] == password:
        print(f"✅ Login successful. Welcome Officer {username}!")
        officer_menu()
    else:
        print("Invalid username or password. Please try again.")

#Officer menu
def officer_menu():
    while True:
        print("\n--- OFFICER MENU ---")
        print("1. View All Cases")
        print("2. Search Case by ID")
        print("3. Filter Cases by Status")
        print("4. Add Follow-up Note")
        print("5. Mark Case Progress")
        print("6. Logout")

        choice = input("Enter your choice: ")

        if choice == "1":
            view_all_cases()
        elif choice == "2":
            search_case()
        elif choice == "3":
            filter_cases()
        elif choice == "4":
            add_follow_up()
        elif choice == "5":
            update_case_status()
        elif choice == "6":
            print("👋 Logging out... Goodbye Officer!")
            break
        else:
            print("⚠️ Invalid choice. Please try again.")

# 4. View All Cases
def view_all_cases():
    print("\n--- ALL REPORTED CASES ---")
    for case in cases:
        print(f"Case ID: {case['case_id']}, Victim: {case['victim_name']}, "
              f"Location: {case['location']}, Type: {case['abuse_type']}, "
              f"Status: {case['status']}")
    print("-----------------------------")


# 5. Search Case by ID
def search_case():
    case_id = input("Enter Case ID to search: ")
    found = False

    for case in cases:
        if case["case_id"].lower() == case_id.lower():
            print("\n--- CASE DETAILS ---")
            print(f"Case ID: {case['case_id']}")
            print(f"Victim: {case['victim_name']}")
            print(f"Location: {case['location']}")
            print(f"Abuse Type: {case['abuse_type']}")
            print(f"Status: {case['status']}")
            print(f"Notes: {case['notes']}")
            found = True
            break

    if not found:
        print("Case not found.")

# 6. Filter Cases by Status
def filter_cases():
    status = input("Enter status (Pending, Under Investigation, In Court, Resolved): ")
    print(f"\n--- CASES WITH STATUS '{status.upper()}' ---")
    found = False
    for case in cases:
        if case["status"].lower() == status.lower():
            print(f"Case ID: {case['case_id']}, Victim: {case['victim_name']}, Location: {case['location']}")
            found = True
    if not found:
        print("No cases found with that status.")

# 7. Add Follow-up Note

def add_follow_up():
    case_id = input("Enter Case ID to add a note: ")
    note = input("Enter your follow-up note: ")

    for case in cases:
        if case["case_id"].lower() == case_id.lower():
            case["notes"].append(note)
            print("✅ Note added successfully.")
            return
    print("Case not found.")


# 8. Update Case Status
def update_case_status():
    case_id = input("Enter Case ID to update: ")
    print("Available statuses: Pending → Under Investigation → In Court → Resolved")
    new_status = input("Enter new status: ")

    for case in cases:
        if case["case_id"].lower() == case_id.lower():
            case["status"] = new_status
            print(f"✅ Case {case_id} updated to '{new_status}'.")
            return
    print(" Case not found.")

# 9. Run file 
if __name__ == "__main__":
    officer_login()

