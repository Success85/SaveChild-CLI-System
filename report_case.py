from data_handler import init_db, get_cursor
from utils import get_string_info, get_age, get_gender,get_phone_number,pause

# Get database connection and cursor safely
conn = init_db()
cursor = get_cursor()

# Collects case details from the user and stores a new abuse case in the database.
def report_new_case():
    print("\n--- Report New Case ---")
    
    # Collect basic personal information
    f_name = get_string_info("Enter First Name: ").capitalize()
    l_name = get_string_info("Enter Last Name: ").capitalize()
    age = get_age("Enter Age: ")
    gender = get_gender("Enter Gender (M/F): ")
    location = get_string_info("Enter Location: ").capitalize()
    Phone_number = get_phone_number("Enter phone number: ")
    secret_word = get_string_info("Enter a case access key: ")

    print("\nSelect Abuse Type:")
    print("1. Domestic Abuse")
    print("2. Sexual Abuse")
    print("3. Physical Abuse")
    print("4. Emotional Abuse")

    # Loop until the user selects a valid abuse type
    while True:
        abuse_choice = input("Enter choice: ").strip()
        if abuse_choice:
            if abuse_choice == "1":
               abuse_type = "Domestic Abuse"
               break
            elif abuse_choice == "2":
               abuse_type = "Sexual Abuse"
               break
            elif abuse_choice == "3":
               abuse_type = "Physical Abuse"
               break
            elif abuse_choice == "4":
               abuse_type = "Emotional Abuse"
               break
            else:
               print("Invalid Choise")
        else:
            print("Invalid Choise")

    # Prepare the SQL insert query
    query = """
        INSERT INTO cases (first_name, last_name, age, gender,Phone_number, location, abuse_type, secret_word)
        VALUES (%s, %s, %s, %s, %s, %s,  %s, %s)
    """
    values = (f_name, l_name, age, gender, location, Phone_number, abuse_type,secret_word)
    
    # Insert the record into the database
    cursor.execute(query, values)
    conn.commit()

    print("\nCase Submitted Successfully!")
    # print("Your Case ID is:", cursor.lastrowid)
    print("-----------------------------------")
    pause()





# Retrieves and displays the current status of a case using the provided case ID.
def check_case_status():
    print("\n--- Check Case Status ---")

    # Keep asking until the user provides a non-empty ID
    while True:
        print("1. Search by Name and phone number")
        print("2. Return to main menu")
        choice = input("Enter choice: ").strip()
 
        if choice == "1":
            first = get_string_info("Enter First Name: ").capitalize()
            last = get_string_info("Enter Last Name: ").capitalize()
            phone_number = get_phone_number("Enter phone number: ")
            query = """
                SELECT case_id, first_name, last_name, age,phone_number, location 
                FROM cases 
                WHERE first_name = %s AND last_name = %s AND phone_number = %s
            """
            params = (first, last, phone_number)
        elif choice == "2":
            return
        else:
            print("Invalid choice.")
            continue

        cursor.execute(query, params)
        rows = cursor.fetchall()

        if not rows:
            print("\nNo cases found.")
            continue

        print("\nMatching Cases:")
        print("-----------------")


        for i, r in enumerate(rows, start=1):
            cid,fn, ln, age, p_num, loc = r
            print(f"{i}. Name: {fn} {ln} | Age: {age} | Phone number: {p_num} | Location: {loc}")

        selection = input("\nWhich one is your case? Enter number: ").strip()

        if not selection.isdigit() or not (1 <= int(selection) <= len(rows)):
            print("Invalid selection.")
            continue
        real_case_id = rows[int(selection) - 1][0]

        cursor.execute("SELECT secret_word FROM cases WHERE case_id = %s", (real_case_id,))
        result = cursor.fetchone()

        if not result:
            print("Unexpected error: case disappeared.")
            continue

        stored_secret = result[0]

        secret = input("Enter your secret key word: ").strip()

        if secret != stored_secret:
            print("\n Secret word does NOT match. Access denied.")
            continue

        cursor.execute("""
            SELECT first_name, last_name, age, gender, location,
                abuse_type, case_status,  follow_up_note,
                status_updated_by, date_reported
            FROM cases
            WHERE case_id = %s
            """, (real_case_id,))

        case = cursor.fetchone()

        print("\nAccess granted! Here are your full case details:")
        print("-----------------------------------------------")
        print(f"First Name     : {case[0]}")
        print(f"Last Name      : {case[1]}")
        print(f"Age            : {case[2]}")
        print(f"Gender         : {case[3]}")
        print(f"Location       : {case[4]}")
        print(f"Abuse Type     : {case[5]}")
        print(f"Case Status    : {case[6]}")
        print(f"follow up note : {case[7]}")
        print(f"status_updated_by : {case[8]}")
        print(f"Date Reported  : {case[9]}")
        print("-----------------------------------------------")