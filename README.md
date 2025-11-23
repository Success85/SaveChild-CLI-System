#  SaveChild CLI — Child Abuse Reporting & Case Management System
### A Python-Based Command-Line Application for Reporting, Tracking, and Managing Child Abuse Cases.*

---
#  Overview

SaveChild CLI is a menu-driven Command-Line Interface application built in Python to help users report child abuse, track case progress, and allow authorized officers to manage and update cases.
The system connects to an Aiven MySQL database, ensuring that all data is securely stored and accessible.

# Core features 
| Feature                   | Description                                                                                    |
| ------------------------- | ------------------------------------------------------------------------------------------------ |
| *Child Abuse Reporting* | Allows users to file new abuse reports with full victim and incident details.                    |
| *Case Tracking*         | Users can check their case using 4 different search methods plus a case access key for security. |
| *Officer Login System*  | Authorized officers can log in to manage, update, and track all cases.                           |
| *Case Status Updates*   | Officers can update case progress with mandatory follow-up notes.                                |
| *Emergency Support*     | Users can access emergency hotlines depending on abuse type or location.                         |
| *Secure Data Storage*   | All cases are stored in Aiven MySQL with automatic table creation during startup.                |

# System Architecture
##  App initialization

python main.py
# App lanuches main menu 
1. Report Child Abuse
2. Check Case Status
3. Officer Login
4. Emergency Support
5. Exit

# User Flow — Reporting Child Abuse
Steps
User selects Report Child Abuse
System collects:
Reporter name & contact (optional)
Victim info (name, age, gender)
Location of the incident
Type of abuse (sexual, domestic, physical, etc.)
Case access key (user-chosen secret word)

System:
Generates a unique Case ID
Saves the case with status = "Pending"
Confirms the report
Displays Case ID + Access Key reminder

# User Flow — Checking Case Status
The user must use search methods + their access key to view case progress.
1. Search by Name + Abuse Type
2. Search Using Any Word You Remember
3. Search by Name + Age
4. Search by Name + Location
5. Return to Main Menu
# Officer Flow — Secure Case Management
1. View All Cases
2. Search Case by ID
3. Filter Cases by Status
4. Update Case Status
5. Logout

## Updating Case Status (Most Important Feature)

Steps:

Officer selects Update Case Status
Enter Case ID
Choose new status:
Pending
Under Investigation
In Court
Resolved
Enter a mandatory follow-up note

# System Automatically Records:
New status
Follow-up note
followed_up_by = officer username
status_updated_by = officer username
Last updated timestamp

# Emergency Support Flow
| Field                  | Description                        |
| ---------------------- | ---------------------------------- |
| first_name / last_name | Victim identity                    |
| age                    | Victim's age                       |
| gender                 | Victim’s gender                    |
| abuse_type             | Type of abuse reported             |
| location               | Where the incident happened        |
| secret_word            | User’s access key                  |
| follow_up              | Notes from officers                |
| follow_up_by           | Which officer added note           |
| status_updated_by      | Officer who changed status         |
| case_status            | Current case stage                 |
| dates                  | Reported & last updated timestamps |

# User Journeys
# Reporter Journey
Report Abuse → Search Case → System Lists Matches → Select Case → Enter Access Key → View Updates
Officer Journey
Login → View/Find Case → Update Status → Add Follow-Up Note → System Records Officer
Emergency Journey
Select Abuse Type or Location → System Shows Hotline Number

# How to Run
Install dependencies
Set environment variables for the MySQL connection
Run:
python main.py
Follow the menu prompts.