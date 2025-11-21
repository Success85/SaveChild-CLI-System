from data_handler import init_db, get_cursor
from utils import get_string_info, get_age, get_gender,pause

# Get database connection and cursor safely
conn = init_db()
cursor = get_cursor()

# Collects case details from the user and stores a new abuse case in the database.
def report_new_case():
    print("\n--- Report New Case ---")
    
    # Collect basic personal information
    f_name = get_string_info("Enter First Name: ")
    l_name = get_string_info("Enter Last Name: ")
    age = get_age("Enter Age: ")
    gender = get_gender("Enter Gender (M/F): ")
    location = get_string_info("Enter Location: ")
    secret_word = get_string_info("Enter a keyword you can remember for searching your case later: ")

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
        INSERT INTO cases (first_name, last_name, age, gender, location, abuse_type, secret_word)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    values = (f_name, l_name, age, gender, location, abuse_type,secret_word)
    
    # Insert the record into the database
    cursor.execute(query, values)
    conn.commit()

    print("\nCase Submitted Successfully!")
    print("Your Case ID is:", cursor.lastrowid)
    print("-----------------------------------")
    pause()





# Retrieves and displays the current status of a case using the provided case ID.
def check_case_status():
    print("\n--- Check Case Status ---")

    # Keep asking until the user provides a non-empty ID
    while True:
        print("\nChoose a search method:")
        print("1. Search by Name + Abuse Type")
        print("2. Search Using Any Word You Remember")
        print("3. Search by Name + Age")
        print("4. Search by Name + Location")
        print("5. Return to Main Menu")

        choice = input("Enter choice: ").strip()
        
        if choice == "1":
            first = get_string_info("Enter First Name: ")
            abuse = get_string_info("Enter Abuse Type: ")
            query = """
                SELECT case_id, first_name, last_name, age, location 
                FROM cases 
                WHERE first_name = %s AND abuse_type = %s
            """
            params = (first, abuse)
        elif choice == "2":
            word = input("Enter any word you remember: ").strip()
            like = f"%{word}%"
            query = """
                SELECT case_id, first_name, last_name, age, location 
                FROM cases 
                WHERE first_name LIKE %s 
                   OR last_name LIKE %s
                   OR location LIKE %s
                   OR abuse_type LIKE %s
                   OR secret_word LIKE %s
            """
            params = (like, like, like, like, like)
        elif choice == "3":
            first = input("Enter First Name: ").strip()
            age = input("Enter Age: ").strip()
            query = """
                SELECT case_id, first_name, last_name, age, location 
                FROM cases 
                WHERE first_name = %s AND age = %s
            """
            params = (first, age)
        elif choice == "4":
            first = input("Enter First Name: ").strip()
            loc = input("Enter Location: ").strip()
            query = """
                SELECT case_id, first_name, last_name, age, location 
                FROM cases 
                WHERE first_name = %s AND location = %s
            """
            params = (first, loc)

        elif choice == "5":
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
            cid,fn, ln, age, loc = r
            print(f"{i}. Name: {fn[:3]}*** {ln[:3]}*** | Age: {age} | Location: {loc[:4]}***")

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

        secret = input("Enter your secret word: ").strip()

        if secret != stored_secret:
            print("\n Secret word does NOT match. Access denied.")
            continue

        cursor.execute("""
            SELECT first_name, last_name, age, gender, location,
                abuse_type, case_status, date_reported
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
        print(f"Date Reported  : {case[7]}")
        print("-----------------------------------------------")