

import os
import time

def clear_screen():
    # Clears the terminal (Windows or Mac/Linux)
    os.system("cls" if os.name == "nt" else "clear")

def get_string_info(prompt):
    """Forces user to enter a non-empty string."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Field can't be empty!")

def get_age(prompt):
    """Validates that the input is a number > 0."""
    while True:
        value = input(prompt).strip()
        if value:
            try:
                value = int(value)
                if value > 0:
                    return value
                print("Age must be greater than 0")
            except:
                print("Age must be a number")
        else:
            print("Age can't be empty")

def get_gender(prompt):
    """Validates input is M or F."""
    while True:
        value = input(prompt).strip().upper()
        if value:
            if value == "M" or value == "F":
                return value
            else:
                print("Enter 'M' or 'F'")
        else:
            print("Gender can't be empty")

def pause(message="Press Enter to continue..."):
    input(message)
