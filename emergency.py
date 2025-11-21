import time


def show_emergency_menu():
    while True:
        print("\nEMERGENCY SUPPORT MENU")
        print("1. View Emergency Hotlines")
        print("2. View NGOs & Child Support Centers")
        print("3. Safety Tips for Children")
        print("4. Return to Main Menu")

        choice = input("Select an option (1–4): ").strip()

        if choice == "1":
            show_hotlines()
        elif choice == "2":
            show_ngos()
        elif choice == "3":
            show_safety_tips()
        elif choice == "4":
            print("\nReturning to Main Menu...")
            time.sleep(1)
            break
        else:
            print("Invalid choice. Please try again.")


#  Option 1: Emergency Hotlines.
def show_hotlines():
    while True:
        print("\nEMERGENCY HOTLINES (24/7)")
        hotlines = [
            {"Name": "Child Helpline", "Number": "116"},
            {"Name": "Police Emergency", "Number": "112"},
            {"Name": "Health Emergency (Ambulance)", "Number": "122"},
            {"Name": "SaveChild Support Line", "Number": "+250 789 654 321"},
        ]

        for h in hotlines:
            print(f" - {h['Name']}: {h['Number']}")
        print("---------------------------")
        print("\nIf you or someone else is in danger, call immediately!")
        print("\n0. Return to Emergency Support Menu")

        choice = input("Select an option: ").strip()
        if choice == "0":
            break
        else:
            print("Invalid option. Type 0 to go back.")


# Option 2: NGO Contacts.
def show_ngos():
    while True:
        print("\nPARTNER NGOs & CHILD PROTECTION ORGANIZATIONS")
        ngos = [
            {"Name": "Save the Children", "Contact": "+250 783 456 789",
                "Email": "info@savethechildren.org"},
            {"Name": "UNICEF Child Protection Desk",
                "Contact": "+250 780 111 222", "Email": "childhelp@unicef.org"},
            {"Name": "Hope for Every Child Foundation",
                "Contact": "+250 788 333 555", "Email": "support@hopechild.org"},
            {"Name": "TerraBox Education & Safety Network",
                "Contact": "+250 784 999 444", "Email": "outreach@terrabox.org"},
        ]

        for ngo in ngos:
            print(f"\nOrganization: {ngo['Name']}")
            print(f"Contact: {ngo['Contact']}")
            print(f"Email: {ngo['Email']}")
            print("---------------------------")

        print(
            "\nYou can reach out for counseling, reporting abuse, or protection support.")
        print("\n0. Return to Emergency Support Menu")

        choice = input("Select an option: ").strip()
        if choice == "0":
            break
        else:
            print("Invalid option. Type 0 to go back.")


# Option 3: Safety Tips.
def show_safety_tips():
    while True:
        print("\nCHILD SAFETY TIPS")
        tips = [
            "1. Always tell your Parents or any adult you know where you are going.",
            "2. Always report to an adult when you are being bullied or hurt.",
            "3. Memorize emergency numbers like 112 or 116.",
            "4. Avoid going alone with strangers, even if they seem nice.",
            "5. Speak up if you or a friend feels unsafe — help is available.",
        ]

        for tip in tips:
            print(f"- {tip}")

        print("\nRemember: Speaking up saves lives.")
        print("\n0. Return to Emergency Support Menu")

        choice = input("Select an option: ").strip()
        if choice == "0":
            break
        else:
            print(" Invalid option. Type 0 to go back.")


# Run standalone
if __name__ == "__main__":
    show_emergency_menu()
