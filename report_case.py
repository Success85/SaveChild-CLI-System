from data_handler import init_db, get_cursor
from utils import get_string_info, get_age, get_gender

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
        INSERT INTO cases (first_name, last_name, age, gender, location, abuse_type)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    values = (f_name, l_name, age, gender, location, abuse_type)
    
    # Insert the record into the database
    cursor.execute(query, values)
    conn.commit()

    print("\nCase Submitted Successfully!")
    print("Your Case ID is:", cursor.lastrowid)
    print("-----------------------------------")


# Retrieves and displays the current status of a case using the provided case ID.
def check_case_status():
    print("\n--- Check Case Status ---")

    # Keep asking until the user provides a non-empty ID
    while True:
        case_id = input("Enter Case ID: ").strip()
        if case_id:
            try:
                # Query the case status from the database for the given ID
                query = "SELECT case_status FROM cases WHERE case_id = %s"
                cursor.execute(query, (case_id,))
                result = cursor.fetchone()
                
                # If the case exists, display its status
                if result:
                    print("\nCase Status:", result[0])
                    break
                else:
                    # display a 'case ID not found in database' message6
                    print("\nCase Not Found. Check the Case ID again.")
                    print("-----------------------------------")
                    break
            except Exception as e:
                print(f"Error querying database: {e}")
                break
        else:
         print("Id can't be empty")