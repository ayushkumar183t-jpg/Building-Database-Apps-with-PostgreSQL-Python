import psycopg2
from psycopg2 import ExtrasDefaults


def manage_student_database():
    # Database configuration details
    # Replace these credentials with your actual local PostgreSQL setup
    connection_config = {
        "dbname": "tutedude_db",
        "user": "postgres",
        "password": "your_password",
        "host": "localhost",
        "port": "5432"
    }

    conn = None
    cursor = None

    try:
        # 1. Establish connection to PostgreSQL
        print("Connecting to the PostgreSQL database...")
        conn = psycopg2.connect(**connection_config)
        cursor = conn.cursor()

        # 2. CREATE: Setup a sample students table
        print("\n--- Creating Table ---")
        create_table_query = """
        CREATE TABLE IF NOT EXISTS students (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            course VARCHAR(100) NOT NULL,
            marks INT NOT NULL
        );
        """
        cursor.execute(create_table_query)
        conn.commit()
        print("Table 'students' verified/created successfully.")

        # 3. INSERT (Clear existing first to ensure clean execution display)
        cursor.execute("TRUNCATE TABLE students RESTART IDENTITY;")

        print("\n--- Inserting Sample Records ---")
        insert_query = "INSERT INTO students (name, course, marks) VALUES (%s, %s, %s);"
        sample_data = [
            ("Alice", "Python Data Science", 85),
            ("Bob", "Full Stack Python", 92),
            ("Charlie", "PostgreSQL Basics", 78)
        ]
        cursor.executemany(insert_query, sample_data)
        conn.commit()
        print(f"Successfully inserted {len(sample_data)} student records.")

        # 4. READ: Fetch and display table records
        print("\n--- Displaying Current Database Records ---")
        cursor.execute("SELECT * FROM students;")
        records = cursor.fetchall()
        for row in records:
            print(f"ID: {row[0]} | Name: {row[1]} | Course: {row[2]} | Marks: {row[3]}")

        # 5. UPDATE: Update Bob's marks
        print("\n--- Updating Record ---")
        update_query = "UPDATE students SET marks = %s WHERE name = %s;"
        cursor.execute(update_query, (95, "Bob"))
        conn.commit()
        print("Successfully updated Bob's marks to 95.")

        # 6. DELETE: Remove Charlie's record
        print("\n--- Deleting Record ---")
        delete_query = "DELETE FROM students WHERE name = %s;"
        cursor.execute(delete_query, ("Charlie",))
        conn.commit()
        print("Successfully deleted Charlie's record.")

        # Final Read check to show state changes
        print("\n--- Final Database Records ---")
        cursor.execute("SELECT * FROM students;")
        final_records = cursor.fetchall()
        for row in final_records:
            print(f"ID: {row[0]} | Name: {row[1]} | Course: {row[2]} | Marks: {row[3]}")

    except Exception as error:
        print(f"\n[ERROR] Database operations failed: {error}")
        if conn:
            conn.rollback()

    finally:
        # Secure resource cleanup
        if cursor:
            cursor.close()
        if conn:
            conn.close()
            print("\nPostgreSQL connection closed safely.")


if __name__ == "__main__":
    manage_student_database()