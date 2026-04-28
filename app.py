import os
import psycopg2


def load_env_file(path=".env"):
    if not os.path.exists(path):
        return

    with open(path, "r", encoding="utf-8") as env_file:
        for raw_line in env_file:
            line = raw_line.strip()

            if not line or line.startswith("#") or "=" not in line:
                continue

            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")

            if key and key not in os.environ:
                os.environ[key] = value


class Database:
    def __init__(self):
        load_env_file()
        self.conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME", "CS480Project"),
            user=os.getenv("DB_USER", "username"),
            password=os.getenv("DB_PASSWORD", "password"),
            host=os.getenv("DB_HOST", "localhost"),
            port=os.getenv("DB_PORT", "5432"),
        )
        self.cur = self.conn.cursor()

class HotelCLI:
    def __init__(self, db):
        self.db = db

    def run(self):
        user_type = self.read_int("Are You A Manager (1) Or A Client (2)?: ")

        if user_type == 1:
            self.manager_flow()
        elif user_type == 2:
            print("Test")
        else:
            print("Unrecognized")

    def manager_flow(self):
        self.manager_login()
        self.manager_menu_loop()

    def manager_login(self):
        while True:
            managerSSN = input("Please Enter Your SSN: ")
            self.db.cur.execute(
                """
                SELECT *
                FROM Managers
                WHERE SSN = %s;
                """,
                (managerSSN,),
            )
            rows = self.db.cur.fetchall()

            if len(rows) > 0:
                return

            print("Incorrect SSN. Please Try Again")

    def manager_menu_loop(self):
        while True:
            self.print_manager_menu()
            query = self.read_int("Enter Your Query Here: ")

            if query == -1:
                break

            self.handle_manager_query(query)

    @staticmethod
    def print_manager_menu():
        print("1 - Insert New Hotel")
        print("2 - Remove Hotel")
        print("3 - Update Hotel")
        print("4 - Insert New Room")
        print("5 - Remove Room")
        print("6 - Update Room")
        print("7 - Remove Client")
        print("8 - Show Top K Clients")
        print("9 - List of All Hotel Rooms and Number of Bookings")
        print("10 - List of Hotels and Info")
        print("11 - Clients to Hotels on cities")
        print("12 - Problematic Chicago Hotels")
        print("13 - Clients list and amount spent")
        print("14 - Register New Manager")
        print("-1 - Quit")

    def handle_manager_query(self, query):
        if query == 1:
            self.insert_hotel()
        elif query == 2:
            self.remove_hotel()
        elif query == 3:
            self.update_hotel()
        elif query == 4:
            self.insert_room()
        elif query == 5:
            self.remove_room()
        elif query == 6:
            self.update_room()
        elif query == 7:
            self.remove_client()
        elif query == 8:
            self.show_top_k_clients()
        elif query == 9:
            print("TODO")
        elif query == 10:
            print("TODO")
        elif query == 11:
            print("TODO")
        elif query == 12:
            print("TODO")
        elif query == 13:
            print("TODO")
        elif query == 14:
            self.register_manager()
        else:
            print("Unrecognized Request. Please Try Again.")

    def insert_hotel(self):
        newHotelID = self.read_int("Please Enter Hotel ID: ")
        newHotelName = input("Please Enter Hotel Name: ")
        newAddress = input("Please Enter New Hotel's Address: ")

        self.db.cur.execute("""INSERT INTO Hotel (Name, HotelID, Address)
                                VALUES (%s, %s);""", (newHotelName, newHotelID, newAddress,))
        self.db.commit()

    def remove_hotel(self):
        deleteHotelID = self.read_int("Please Enter Hotel ID: ")
        self.db.cur.execute("""DELETE FROM Hotel
                                WHERE HotelID = %s;""", (deleteHotelID,))
        self.db.commit()

    def update_hotel(self):
        hotelID = self.read_int("Please Enter ID Of Hotel To Update: ")
        newHotelName = input("Please Enter Hotel Name: ")
        newAddress = input("Please Enter New Hotel's Address: ")

        self.db.cur.execute("""UPDATE Hotel
                                SET Name = %s, Address = %s
                                WHERE HotelID = %s;""", (newHotelName, newAddress, hotelID,))
        self.db.commit()

    def insert_room(self):
        hotelID = self.read_int("Please Enter Hotel ID: ")
        roomNumber = self.read_int("Please Enter Room Number: ")
        accessMode = input("Please Enter Access Mode: ")
        numWindows = self.read_int("Please Enter Number Of Windows: ")
        lastRenovatedYear = self.read_int("Please Enter Last Year Of Renovation: ")

        self.db. cur.execute("""INSERT INTO Room (RoomNumber, HotelID, AccessMode, NumWindows, LastRenovatedYear)
                                 VALUES (%s, %s, %s, %s, %s);
                                 """, (roomNumber, hotelID, accessMode, numWindows, lastRenovatedYear,))
        self.db.commit()

    def remove_room(self):
        hotelName = input("Please Enter Hotel Name: ")
        roomNumber = self.read_int("Please Enter Room Number: ")
        hotelID = self.db.get_hotel_id(hotelName)

        if hotelID is None:
            print("Hotel not found.")
            return

        self.db.cur.execute("""DELETE FROM Room
                                WHERE RoomNumber = %s AND HotelID = %s;""", (roomNumber, hotelID,))
        self.db.commit()

    def update_room(self):
        hotelName = input("Please Enter Hotel Name: ")
        roomNumber = self.read_int("Please Enter Room Number: ")
        accessMode = input("Please Enter Access Mode: ")
        numWindows = self.read_int("Please Enter Number Of Windows: ")
        lastRemnovatedYear = self.read_int("Please Enter Last Year Of Renovation: ")
        # Get associated hotel ID first
        hotelID = self.db.get_hotel_id(hotel_name)

        # If not found, return
        if hotelID is None:
            print("Hotel not found.")
            return

        # Then query with hotel ID
        self.db.cur.execute("""UPDATE Room
                                SET AccessMode = %s, NumWindows = %s, LastRenovatedYear = %s
                                WHERE RoomNumber = %s AND HotelID = %s;""", (accessMode, numWindows, lastRenovatedYear, roomNumber, hotelID,))
        self.db.commit()

    def remove_client(self):
        # Deletes by client email
        clientEmail = input("Please Enter Client Email To Remove: ")
        self.db.cur.execute("""DELETE FROM Client
                                WHERE Email = %s;""", (clientEmail,))
        self.db.commit()

    def show_top_k_clients(self):
        kNum = self.read_int("Please Enter The K Number Of Clients To Return: ")

        self.db.cur.execute("""SELECT C.Name, C.Email, COUNT(*) as booking_count
                                FROM Client C
                                JOIN Booking B ON C.Email = B.ClientEmail
                                GROUP BY C.Name, C.Email
                                ORDER BY booking_count DESC
                                LIMIT %s;
                                """, (kNum,))
        rows = self.db.cur.fetchall()

        for row in rows:
            print(f"Name: {row[0]}, Email: {row[1]}")

    def register_manager(self):
        newManagerName = input("Please Enter New Manager Name: ")
        newManagerEmail = input("Please Enter New Manager Email: ")
        newManagerSSN = input("Please Enter New Manager SSN: ")

        self.db.cur.execute("""INSERT INTO Managers (Name, Email, SSN)
                                 VALUES (%s, %s, %s);
                                 """, (newManagerName, newManagerEmail, newManagerSSN,))
        self.db.commit()

    @staticmethod
    def read_int(prompt):
        while True:
            try:
                return int(input(prompt))
            except ValueError:
                print("Please enter a valid number.")


def main():
    db = None
    try:
        db = Database()
        app = HotelCLI(db)
        app.run()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if db:
            db.close()


if __name__ == "__main__":
    main()