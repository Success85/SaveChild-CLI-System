# from data_handler import get_cursor, init_db
# from utils import clear_screen, pause

# conn = init_db()
# cursor = get_cursor()
# ADMIN_USERNAME = "admin"
# ADMIN_PASSWORD = "admin_Login111" 

# def login():
#     """
#     Handles the admin login process.
#     """
#     clear_screen()
#     print("=== Admin Login ===")
#     username = input("Username: ").strip()
#     password = input("Password: ").strip()


#     if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
#         print("Login successful. Welcome, Admin!")
#         return True
#     else:
#         print("Invalid username or password.")
#         pause()
#         return False

# def view_all_reports():
#     """
#     Fetches and displays all reports directly from MySQL.
#     """
#     print("\n--- All Submitted Reports ---")
#     try:
#         conn, cursor = get_cursor() 
#         print("\n--- All Submitted Reports ---")
#         query = "SELECT case_id, first_name, last_name, location, abuse_type, case_status FROM cases"
#         cursor.execute(query)
#         rows = cursor.fetchall()

#         if not rows:
#             print("No reports found in database.")
#         else:
#             for row in rows:
#                 print("-" * 40)
#                 print("Case ID: {} | Status: {}".format(row[0], row[5]))
#                 print("Name: {} {} | Loc: {}".format(row[1], row[2], row[3]))
#                 print("Abuse Type: {}".format(row[4]))
            
#         cursor.close()

#     except Exception as e:
#         print("Database Error: {}".format(e))
    
#     pause()


# def update_report_status():
#     print("\n--- Update Report Status ---")
#     case_id = input("Enter Case ID: ").strip()
    
#     statuses = ["Pending", "Under Investigation", "In Court", "Resolved"]
#     print("Select a new status:")
#     for i, status in enumerate(statuses, 1):
#         print("{}. {}".format(i, status))

#     try:
#         choice = int(input("Choice (1-4): ")).strip()
#         if 1 <= choice <= 4:
#             new_status = statuses[choice - 1]
#             conn, cursor = get_cursor()
#             cursor.execute("SELECT case_id FROM cases WHERE case_id = %s", (case_id,))
#             if not cursor.fetchone():
#                 print("Error: Case ID not found.")
#             else:
#                 cursor.execute("UPDATE cases SET case_status = %s WHERE case_id = %s", (new_status, case_id))
                
#                 conn.commit()
#                 print("Successfully updated Case ID {} to '{}'.".format(case_id, new_status))
            
#             cursor.close()
#         else:
#             print("Invalid choice. Please select a number between 1 and 4.")
#     except ValueError:
#         print("Invalid input. Please enter a number.")
#     pause()

# def delete_report():
#     print("\n--- Delete Report ---")
#     case_id = input("Enter Case ID to DELETE: ")

#     confirm = input("Are you sure you want to PERMANENTLY delete Case ID {}? (yes/no): ".format(case_id)).lower()

#     if confirm == 'yes':
#         try:
#             conn, cursor = get_cursor()
            
#             cursor.execute("SELECT case_id FROM cases WHERE case_id = %s", (case_id,))
#             if not cursor.fetchone():
#                 print("Error: Case ID not found.")
#             else:
#                 cursor.execute("DELETE FROM cases WHERE case_id = %s", (case_id,))
                
#                 conn.commit()
#                 print("Successfully deleted Case ID {}.".format(case_id))
            
#             cursor.close()
            
#         except Exception as e:
#             print("Database Error: {}".format(e))

#     else:
#         print("Deletion cancelled.")
    
#     pause()

# def admin_menu():
#     """
#     The main menu for the admin after logging in.
#     """

#     if not login():
#         return

#     while True:
#         print("\n=== Admin Dashboard ===")
#         print("1. View all reports")
#         print("2. Update a report status")
#         print("3. Delete a report")
#         print("4. Logout")

#         choice = input("Enter your choice (1-4): ").strip()
#         clear_screen()

#         if choice == '1':
#             view_all_reports()
#         elif choice == '2':
#             update_report_status()
#         elif choice == '3':
#             delete_report()
#         elif choice == '4':
#             print("Logging out...")
#         else:
#             print("Invalid choice.")
#             pause()

# if __name__ == "__main__":
#     admin_menu()
