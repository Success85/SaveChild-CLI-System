from data_handler import init_db, get_cursor


conn = init_db()
cursor = get_cursor()
def get_string_info(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        else:
            print("Field can't be empty!!!!")
def get_age(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            try:
                value = int(value)
                if value > 0:
                    return value
                else:
                    print("Age must be greater than 0")
            except:
                print("Age must be a number")
        else:
            print("Age can't be empty")

def get_gender(prompt):
    while True:
        value = input(prompt).strip().upper()
        if value:
            if value == "M" or value == "F":
                return value
            else:
                print("Enter 'M,m' or 'F,f'")
        else:
            print("Gender can't be empty")

def report_new_case():
    print("\n--- Report New Case ---")
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

    query = """
        INSERT INTO cases (first_name, last_name, age, gender, location, abuse_type)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    values = (f_name, l_name, age, gender, location, abuse_type)
    cursor.execute(query, values)
    conn.commit()

    print("\nCase Submitted Successfully!")
    print("Your Case ID is:", cursor.lastrowid)
    print("-----------------------------------")

def check_case_status():
    print("\n--- Check Case Status ---")
    while True:
        case_id = input("Enter Case ID: ")
        if case_id:
            query = "SELECT case_status FROM cases WHERE case_id = %s"
            cursor.execute(query, (case_id,))
            result = cursor.fetchone()

            if result:
                print("\nCase Status:", result[0])
                break
            else:
                print("\nCase Not Found. Check the Case ID again.")
                print("-----------------------------------")
        else:
         print("Id can't be empty")

    
def report_menu():
    while True:
        print("\n--- Report Menu ---")
        print("1. Report New Case")
        print("2. Check Case Status")
        print("3. Back to Main Menu")
        choice = input("Enter choice: ")

        if choice == '1':
            report_new_case()
        elif choice == '2':
            check_case_status()
        elif choice == '3':
            break
        else:
            print("\nInvalid Choice. Try Again.")