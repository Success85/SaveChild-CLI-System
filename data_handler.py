import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
    "port": int(os.getenv("DB_PORT")),
}

# Global connection object
connection = None


def init_db():
    """
    Initialize and return a single shared database connection.
    Prevents creation of multiple connections.
    """
    global connection

    try:
        # Reuse existing connection
        if connection and connection.is_connected():
            return connection

        # Create new connection
        connection = mysql.connector.connect(**DB_CONFIG)

        if connection.is_connected():
            print("Database connected successfully.")
            return connection
        else:
            print("Database connection failed.")
            return None

    except mysql.connector.Error as error:
        print(f"Database Error: {error}")
        return None


def get_cursor():
    """Return a cursor from the active database connection."""
    conn = init_db()
    if conn and conn.is_connected():
        return conn.cursor()
    else:
        raise ConnectionError("Database connection is not available.")


def create_tables():
    """Create database tables if they don't exist."""
    conn = init_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cases (
            case_id INT AUTO_INCREMENT PRIMARY KEY,
            first_name VARCHAR(50),
            last_name VARCHAR(50),
            age INT,
            gender CHAR(1),
            location VARCHAR(100),
            abuse_type VARCHAR(50),
            case_status VARCHAR(50) DEFAULT 'Pending',
            date_reported TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            secret_word VARCHAR(100),
            follow_up_note VARCHAR(100),
            status_updated_by VARCHAR(100),
        )
    """)

    conn.commit()
    cursor.close()

    print("Tables created and verified successfully.")

