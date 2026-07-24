from db import get_connection


def test_connection():
    try:
        conn = get_connection()

        if conn.is_connected():
            print("=" * 40)
            print(" Restaurant Management System")
            print("=" * 40)
            print(" Database Connected Successfully!")

        conn.close()

    except Exception as e:
        print("Connection Error")
        print(e)


if __name__ == "__main__":
    test_connection()