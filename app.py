import os
import psycopg2
from datetime import date


def load_env_file(path=".env"):
    if not os.path.exists(path):
        print('whoops')
        return
    # print('Wohooo')
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
        load_env_file('.env.example')
        # print(os.getenv('DB_Password'))
        # print(os.getenv("Password"))
        self.conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME", "CS480Project"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("PASSWORD", "postgres"),
            host=os.getenv("DB_HOST", "localhost"),
            port=os.getenv("DB_PORT", "5432"),
        )
        self.cur = self.conn.cursor()

    def close(self):
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()

    def commit(self):
        self.conn.commit()

    def get_hotel_id(self, hotel_name):
        self.cur.execute(
            """
            SELECT HotelID
            FROM Hotel
            WHERE Name = %s;
            """,
            (hotel_name,),
        )
        row = self.cur.fetchone()
        return row[0] if row else None


class HotelCLI:
    def __init__(self, db):
        self.db = db
        self.current_client_email = None

    def run(self):
        user_type = self.read_int("Are You A Manager (1) Or A Client (2)?: ")

        if user_type == 1:
            while True:
                option = self.read_int("Enter 1 to register manager, enter 2 to login: ")
                if option==1:
                    self.register_manager()
                    continue
                elif option==2:
                    break
                print("Please enter valid option")
            self.manager_flow()
        elif user_type == 2:
            while True:
                option = self.read_int("Enter 1 if you are a new client, enter 2 to login: ")
                if option==1:
                    if self.register_user():
                        break
                elif option==2:
                    break
                else:
                    print("Invalid option")

            self.client_menu()
        else:
            print("Unrecognized")

    def manager_flow(self):
        self.manager_login()
        self.manager_menu_loop()

    def client_menu(self):
        self.client_login()
        self.client_menu_loop()

    def client_login(self):
        while True:
            client_email = input("Please Enter Your Email: ").strip()
            self.db.cur.execute(
                """
                SELECT Email
                FROM Client
                WHERE Email = %s;
                """,
                (client_email,),
            )
            row = self.db.cur.fetchone()
            if row:
                self.current_client_email = row[0]
                return

            print("Client not found. Please Try Again.")

    def client_menu_loop(self):
        while True:
            self.print_client_menu()
            query = self.read_int("Enter Your Query Here: ")

            if query == -1:
                break

            self.handle_client_query(query)

    @staticmethod
    def print_client_menu():
        print("1 - Update information")
        print("2 - View available rooms")
        print("3 - Book Specific Room")
        print("4 - Submit Hotel Review")
        print("5 - View My Bookings")
        print("6 - Automatic Booking")
        print("-1 - Quit")

    def handle_client_query(self, query):
        if query==1:
            self.update_client_info()
        elif query==2:
            self.get_all_rooms()
        elif query == 3:
            self.book_specific_room()
        elif query == 4:
            self.submit_review()
        elif query == 5:
            self.view_my_bookings()
        elif query == 6:
            self.automatic_booking()
        else:
            print("Unrecognized Request. Please Try Again.")

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
            self.hotel_rooms_and_bookings()
        elif query == 10:
            self.hotels_info()
        elif query == 11:
            self.client_to_hotels_on_cities()
        elif query == 12:
            self.client_to_hotels_on_cities()
        elif query == 13:
            self.client_amount()
        else:
            print("Unrecognized Request. Please Try Again.")

    # Insert Hotel (4.1.2)
    def insert_hotel(self):
        newHotelName = input("Please Enter Hotel Name: ")
        newAddress = input("Please Enter New Hotel's Street Address: ")
        newAddressCity = input("Please Enter New Hotel's City: ")

        # Insert Address First
        self.db.cur.execute("""INSERT INTO Address (Street, City)
                                VALUES (%s, %s)""", (newAddress, newAddressCity))

        # Get Address ID
        self.db.cur.execute("""SELECT Number FROM Address
                                WHERE Street = %s AND City = %s""", (newAddress, newAddressCity,))
        addressID = self.db.cur.fetchone()

        # Insert Hotel and tie address to it
        self.db.cur.execute("""INSERT INTO Hotel (Name, AddressID)
                                VALUES (%s, %s);""", (newHotelName, addressID,))
        self.db.commit()

    # Remove Hotel (4.1.3)
    def remove_hotel(self):

        deleteHotelID = self.read_int("Please Enter Hotel ID: ")

        # Get associated Address ID
        self.db.cur.execute("""SELECT AddressID FROM Hotel
                                WHERE HotelID = %s;""", (deleteHotelID,))
        row = self.db.cur.fetchone()
        addressID = row[0] if row else None

        if addressID == None:
            print("No such ID Exists")
            return

        # Delete Bookings
        self.db.cur.execute("""DELETE FROM Booking
                                WHERE HotelID = %s;""", (deleteHotelID,))

        # Delete Hotel Rooms
        self.db.cur.execute("""DELETE FROM Room
                                WHERE HotelID = %s;""", (deleteHotelID,))

        # Delete Hotel
        self.db.cur.execute("""DELETE FROM Hotel
                                WHERE HotelID = %s;""", (deleteHotelID,))
        
        # Delete Hotel Address
        self.db.cur.execute("""DELETE FROM Address
                                WHERE Number = %s;""", (addressID,))

        self.db.commit()

    # Update Hotel (4.1.4)
    def update_hotel(self):
        hotelID = self.read_int("Please Enter ID Of Hotel To Update: ")
        newHotelName = input("Please Enter New Hotel Name: ")
        newAddress = input("Please Enter New Hotel's Street Address: ")
        newAddressCity = input("Please Enter New Hotel's City: ")

        # Get associated Address ID
        self.db.cur.execute("""SELECT AddressID FROM Hotel
                                WHERE HotelID = %s;""", (hotelID,))
        row = self.db.cur.fetchone()
        addressID = row[0] if row else None

        if addressID == None:
            print("No such ID Exists")
            return

        # Update old address
        self.db.cur.execute("""UPDATE Address
                                SET Street = %s, City = %s
                                WHERE Number = %s;""", (newAddress, newAddressCity, addressID,))

        # Update hotel info
        self.db.cur.execute("""UPDATE Hotel
                                SET Name = %s
                                WHERE HotelID = %s;""", (newHotelName, hotelID,))
        self.db.commit()

    # Insert Room (4.1.5)
    def insert_room(self):
        hotelName = input("Please Enter Hotel Name: ")
        roomNumber = self.read_int("Please Enter Room Number: ")
        accessMode = input("Please Enter Access Mode: ")
        numWindows = self.read_int("Please Enter Number Of Windows: ")
        lastRenovatedYear = self.read_int("Please Enter Last Year Of Renovation: ")

        # Check for correct hotel ID
        hotelID = self.db.get_hotel_id(hotelName)

        # Return if hotel id does not exist
        if hotelID == None:
            print("Incorrect Or Missing Name From Hotel Table")
            return
        
        # Insert New Room
        self.db. cur.execute("""INSERT INTO Room (RoomNumber, HotelID, AccessMode, NumWindows, LastRenovatedYear)
                                 VALUES (%s, %s, %s, %s, %s);
                                 """, (roomNumber, hotelID, accessMode, numWindows, lastRenovatedYear,))

        self.db.commit()

    # Remove Room (4.1.6)
    def remove_room(self):
        hotelName = input("Please Enter Hotel Name: ")
        roomNumber = self.read_int("Please Enter Room Number: ")

        # Get associated hotel ID first
        hotelID = self.db.get_hotel_id(hotelName)

        if hotelID is None:
            print("Hotel not found.")
            return

        # Check that room exists
        self.db.cur.execute("""SELECT RoomNumber FROM Room
                                WHERE HotelID = %s AND RoomNumber = %s;""", (hotelID, roomNumber,))
        row = self.db.cur.fetchone()
        roomExists = row[0] if row else None

        if roomExists == None:
            print("No such room exists")
            return

        # Delete Bookings
        self.db.cur.execute("""DELETE FROM Booking
                                WHERE RoomNumber = %s;""", (roomNumber,))
        
        # Remove room
        self.db.cur.execute("""DELETE FROM Room
                                WHERE RoomNumber = %s AND HotelID = %s;""", (roomNumber, hotelID,))
        self.db.commit()

    # Update Room (4.1.7)
    def update_room(self):
        hotelName = input("Please Enter Hotel Name: ")
        roomNumber = self.read_int("Please Enter Room Number: ")
        newRoomNumber = self.read_int("Please Enter New Room Number: ")
        accessMode = input("Please Enter New Access Mode: ")
        numWindows = self.read_int("Please Enter New Number Of Windows: ")
        lastRenovatedYear = self.read_int("Please Enter New Last Year Of Renovation: ")

        # Get associated hotel ID first
        hotelID = self.db.get_hotel_id(hotelName)

        # If not found, return
        if hotelID is None:
            print("Hotel not found.")
            return

        # Check that room exists
        self.db.cur.execute("""SELECT RoomNumber FROM Room
                                WHERE HotelID = %s AND RoomNumber = %s;""", (hotelID, roomNumber,))
        row = self.db.cur.fetchone()
        roomExists = row[0] if row else None

        if roomExists == None:
            print("No such room exists")
            return

        # Then query with hotel ID
        self.db.cur.execute("""UPDATE Room
                                SET RoomNumber = %s, AccessMode = %s, NumWindows = %s, LastRenovatedYear = %s
                                WHERE RoomNumber = %s AND HotelID = %s;""", (newRoomNumber, accessMode, numWindows, lastRenovatedYear, roomNumber, hotelID,))

        self.db.commit()

    # Remove Client (4.1.8)
    def remove_client(self):
        clientEmail = input("Please Enter Client Email To Remove: ").strip()

        # 1. Collect all potential AddressIDs associated with this client
        # We need the client's home address and all their credit card billing addresses
        addr_query = """
            SELECT AddressID FROM Client WHERE Email = %s
            UNION
            SELECT BillingAddressID FROM CreditCard WHERE ClientEmail = %s
        """
        self.db.cur.execute(addr_query, (clientEmail, clientEmail))
        address_ids = [row[0] for row in self.db.cur.fetchall() if row[0] is not None]

        try:
            # 2. Delete from tables that reference ClientEmail (The "Children")
            # Order matters if there are further dependencies
            self.db.cur.execute("DELETE FROM Review WHERE ClientEmail = %s", (clientEmail,))
            self.db.cur.execute("DELETE FROM Booking WHERE ClientEmail = %s", (clientEmail,))
            self.db.cur.execute("DELETE FROM CreditCard WHERE ClientEmail = %s", (clientEmail,))

            # 3. Delete the Client (The "Parent")
            self.db.cur.execute("DELETE FROM Client WHERE Email = %s", (clientEmail,))

            # 4. Clean up Addresses (Only if not used by Hotels or other Clients)
            for addr_id in address_ids:
                # This subquery checks if the address is still in use elsewhere
                check_usage = """
                    SELECT 
                        (SELECT COUNT(*) FROM Hotel WHERE AddressID = %s) +
                        (SELECT COUNT(*) FROM Client WHERE AddressID = %s) +
                        (SELECT COUNT(*) FROM CreditCard WHERE BillingAddressID = %s)
                """
                self.db.cur.execute(check_usage, (addr_id, addr_id, addr_id))
                if self.db.cur.fetchone()[0] == 0:
                    self.db.cur.execute("DELETE FROM Address WHERE Number = %s", (addr_id,))

            self.db.conn.commit()
            print(f"Successfully removed client {clientEmail} and all associated unique data.")

        except Exception as e:
            self.db.conn.rollback()
            print(f"Error during removal: {e}")

    # Show Top K Clients (4.1.9)
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

    # Register Manager (4.1.10)
    def register_manager(self):
        newManagerName = input("Please Enter New Manager Name: ")
        newManagerEmail = input("Please Enter New Manager Email: ")
        newManagerSSN = input("Please Enter New Manager SSN: ")

        self.db.cur.execute("""INSERT INTO Managers (Name, Email, SSN)
                                 VALUES (%s, %s, %s);
                                 """, (newManagerName, newManagerEmail, newManagerSSN,))
        self.db.commit()

    # List of all Hotel Rooms and Number of Bookings (4.1.11)
    def hotel_rooms_and_bookings(self):
        self.db.cur.execute("""
            SELECT
                H.Name,
                R.RoomNumber,
                COUNT(B.ClientEmail) AS NumBookings
            FROM Hotel H
            JOIN Room R
                ON H.HotelID = R.HotelID
            LEFT JOIN Booking B
                ON R.HotelID = B.HotelID
                AND R.RoomNumber = B.RoomNumber
            GROUP BY H.HotelID, H.Name, R.RoomNumber
            ORDER BY H.Name, R.RoomNumber;
        """)

        rows = self.db.cur.fetchall()

        print()
        print(f"{'Hotel Name':<25} {'Room Number':<15} {'Number of Bookings':<20}")

        for name, room, count in rows:
            print(f"{name:<25} {room:<15} {count:<20}")
        print()

    # Clients to Hotels on cities (4.1.12)
    def client_to_hotels_on_cities(self):
        first_city = input("Please enter client city: ")
        second_city = input("Please enter hotel city: ")

        self.db.cur.execute("""
                SELECT DISTINCT
                C.Name,
                C.Email
            FROM Client C
            JOIN Address ClientAddress
                ON C.AddressID = ClientAddress.Number
            JOIN Booking B
                ON C.Email = B.ClientEmail
            JOIN Hotel H
                ON B.HotelID = H.HotelID
            JOIN Address HotelAddress
                ON H.AddressID = HotelAddress.Number
            WHERE LOWER(ClientAddress.City) = LOWER(%s)
            AND LOWER(HotelAddress.City) = LOWER(%s)
            ORDER BY C.Name, C.Email;
        """, (first_city, second_city))
        rows = self.db.cur.fetchall()

        print()
        print(f"{'Client Name':<25}        {'Email':<15}")
        for name, email in rows:
            print(f"{name:<25}        {email:<15}")
        print()

    # List of Hotels and Info (4.1.13)
    def hotels_info(self):
        self.db.cur.execute("""
            SELECT H.Name, COUNT(DISTINCT B.BookingID) AS TotalBookings, AVG(R.Rating) AS AverageRating
            FROM Hotel H
            LEFT JOIN Booking B
                ON H.HotelID = B.HotelID
            LEFT JOIN Review R
                ON H.HotelID = R.HotelID
            GROUP BY H.HotelID, H.Name
            ORDER BY H.Name;
        """)
        rows = self.db.cur.fetchall()

        print()
        print(f"{'Hotel Name':<25}      {'Total Bookings':<18}       {'Average Rating':<18}")
        for hotel_name, total_bookings, average_rating in rows:
            if average_rating is None:
                average_rating_text = "No reviews"
            else:
                average_rating_text = f"{average_rating:.2f}"

            print(f"{hotel_name:<25}        {total_bookings:<18}        {average_rating_text:<18}")
        print()

     # Problematic Chicago Hotels (4.1.14)
    def problematic_hotels(self):
        self.db.cur.execute("""
                SELECT
                H.Name,
                AVG(RV.Rating) AS AverageRating
            FROM Hotel H
            JOIN Address HotelAddress
                ON H.AddressID = HotelAddress.Number
            JOIN Review RV
                ON H.HotelID = RV.HotelID
            JOIN Booking B
                ON H.HotelID = B.HotelID
            JOIN Client C
                ON B.ClientEmail = C.Email
            JOIN Address ClientAddress
                ON C.AddressID = ClientAddress.Number
            WHERE LOWER(HotelAddress.City) = LOWER('Chicago')
            AND LOWER(ClientAddress.City) <> LOWER('Chicago')
            GROUP BY H.HotelID, H.Name
            HAVING AVG(RV.Rating) < 2
            AND COUNT(DISTINCT B.ClientEmail) >= 2
            ORDER BY H.Name;
        """)
        rows = self.db.cur.fetchall()

        print()
        print(f"{'Hotel Name':<25}      {'Average Rating':<18}")
        for hotel_name, avg_rating in rows:
            print(f"{hotel_name:<25}             {avg_rating:<18}")
        print()

    # 4.1.13 Total amount spent by every client
    def client_amount(self):
        self.db.cur.execute("""WITH emails as (SELECT Client.Email, SUM((Booking.EndDate - Booking.StartDate) * Booking.Price) AS Rev FROM Client LEFT JOIN Booking ON Client.Email = Booking.ClientEmail
GROUP BY Client.Email)
        Select Client.Name, emails.Rev FROM emails LEFT JOIN Client on emails.email=CLient.Email;""")
        rows = self.db.cur.fetchall()

        for row in rows:
            print(f"Name: {row[0]} | Total Amount Spent: {row[1]}")
        
        return
    
    # Helper to get street and city from user
    def get_address(self):
        street = input("Enter your street: ").strip()
        city = input("Enter your city: ").strip()
        return (street, city)

    # Helper to insert address and return the ID
    def save_address(self, address_tuple):
        # Unpack street and city
        street, city = address_tuple
        # INSERT and get the auto-generated ID back
        query = "INSERT INTO Address (Street, City) VALUES (%s, %s) RETURNING Number;"
        self.db.cur.execute(query, (street, city))
        address_id = self.db.cur.fetchone()[0]
        return address_id

    # Register client (4.2.1)
    def register_user(self):
        name = input("Please enter your full name: ").strip()
        email = input("Please enter your email: ").strip()
        
        if '@' not in email:
            print('You did not enter a valid email')
            return False
        
        # Check for existing email using parameters
        self.db.cur.execute("SELECT email FROM Client WHERE email = %s", (email,))
        if self.db.cur.fetchone():
            print("Email already exists, try another email")
            return False

        # 1. Get and Save Client Address
        print("Please enter your residential address")
        res_address_data = self.get_address()
        res_address_id = self.save_address(res_address_data)

        # 2. Insert Client
        # Note: Using %s placeholders is safer and handles strings correctly
        client_query = "INSERT INTO Client (Name, Email, AddressID) VALUES (%s, %s, %s);"
        self.db.cur.execute(client_query, (name, email, res_address_id))

        # 3. Get and Save Credit Card Billing Address
        print("Please enter your credit card information")
        number = self.read_int("Please enter your credit card number: ") 
        
        option = self.read_int("Please enter 1 to add new Billing address or 2 to use your address: ")
        if option==1:
            bill_address_data = self.get_address()
            bill_address_id = self.save_address(bill_address_data)
        elif option==2:
            bill_address_id = res_address_id

        # 4. Insert Credit Card
        card_query = "INSERT INTO CreditCard (CreditCardNumber, ClientEmail, BillingAddressID) VALUES (%s, %s, %s);"
        self.db.cur.execute(card_query, (number, email, bill_address_id))

        # 5. Commit all changes to the DB
        self.db.commit()
        print(f"Success! User {name} and card {number} registered.")
        
        return True

    def safe_delete_address(self, address_id):
        """Deletes an address only if not linked to any Hotel, Client, or CreditCard."""
        if not address_id:
            return

        # Check all three tables for references
        check_query = """
            SELECT 
                (SELECT COUNT(*) FROM Hotel WHERE AddressID = %s) +
                (SELECT COUNT(*) FROM Client WHERE AddressID = %s AND Email != %s) +
                (SELECT COUNT(*) FROM CreditCard WHERE BillingAddressID = %s AND ClientEmail != %s)
        """
        self.db.cur.execute(check_query, (address_id, self.self.current_client_email, address_id, address_id, self.current_client_email))
        count = self.db.cur.fetchone()[0]

        if count == 0:
            self.db.cur.execute("DELETE FROM Address WHERE AddressID = %s", (address_id,))
            print(f"Old address (ID: {address_id}) was unused and has been removed.")

    def update_client_info(self):
        while True:
            print("\n--- Update Profile ---")
            print("1 - Update Name")
            print("2 - Add New Credit Card")
            print("3 - Change Residential Address")
            print("-1 - Quit")
            choice = self.read_int("Enter your choice: ")
            
            if choice == -1:
                return
            if choice in [1, 2, 3]:
                break
            print("Please enter a valid option")

        if choice == 1:
            new_name = input("Please enter your new name: ").strip()
            query = "UPDATE Client SET Name = %s WHERE Email = %s;"
            self.db.cur.execute(query, (new_name, self.current_client_email))
            print("Name updated successfully.")

        elif choice == 2:
            # --- Add a New Credit Card (Keeping old ones) ---
            print("Please enter your NEW credit card information")
            number = self.read_int("Enter card number: ")
            print("Please enter the billing address for this card")
            bill_address_data = self.get_address()
            bill_address_id = self.save_address(bill_address_data)

            # Insert New Card (No DELETE, we support multiple cards)
            card_query = "INSERT INTO CreditCard (CreditCardNumber, ClientEmail, BillingAddressID) VALUES (%s, %s, %s);"
            self.db.cur.execute(card_query, (number, self.current_client_email, bill_address_id))
            print("New credit card added successfully.")

        elif choice == 3:
            # --- Change Residential Address ---
            # 1. Get the current AddressID so we can try to clean it up after the update
            self.db.cur.execute("SELECT AddressID FROM Client WHERE Email = %s", (self.current_client_email,))
            old_res_id = self.db.cur.fetchone()[0]

            print("Please enter your new residential address")
            res_address_data = self.get_address()
            res_address_id = self.save_address(res_address_data)

            # 2. Update Client to point to the new ID
            query = "UPDATE Client SET AddressID = %s WHERE Email = %s;"
            self.db.cur.execute(query, (res_address_id, self.current_client_email))
            
            # 3. Clean up old address if it's now a "ghost" record
            self.safe_delete_address(old_res_id)
            print("Residential address updated.")

        self.db.conn.commit()
        return
    
    # 4.2.3 get all available rooms
    def get_all_rooms(self):
        startDate = self.read_date("Please enter your checkin date (YYYY-MM-DD): ")
        endDate = self.read_date("Please enter your checkout date (YYYY-MM-DD): ")

        if endDate <= startDate:
            print("Error: Checkout must be after Checkin.")
            return

        # Using a subquery to find all ROOMS that are NOT booked during those dates to get rooms which are not booked at all and the available ones
        query = """
            SELECT h.Name, r.RoomNumber
            FROM Room r
            JOIN Hotel h ON r.HotelID = h.HotelID
            WHERE (r.HotelID, r.RoomNumber) NOT IN (
                SELECT Booking.HotelID, Booking.RoomNumber 
                FROM Booking 
                WHERE Booking.StartDate < %s AND Booking.EndDate > %s
            );
        """
        
        
        self.db.cur.execute(query, (endDate, startDate))
        rows = self.db.cur.fetchall()

        if not rows:
            print("No rooms available for these dates.")
        else:
            print(f"\nAvailable rooms from {startDate} to {endDate}:")
            for row in rows:
                print(f"Hotel: {row[0]} | Room: {row[1]}")

        return

    # Book specific room (4.2.4)
    def book_specific_room(self):
        hotel_name = input("Enter Hotel Name: ").strip()
        room_number = self.read_int("Enter Room Number: ")
        start_date = self.read_date("Enter Start Date (YYYY-MM-DD): ")
        end_date = self.read_date("Enter End Date (YYYY-MM-DD): ")
        price_per_day = self.read_int("Enter Price Per Day: ")

        if start_date > end_date:
            print("Start date must be on or before end date.")
            return

        hotel_id = self.db.get_hotel_id(hotel_name)
        if hotel_id is None:
            print("Hotel not found.")
            return

        self.db.cur.execute(
            """
            SELECT 1
            FROM Room
            WHERE HotelID = %s AND RoomNumber = %s;
            """,
            (hotel_id, room_number),
        )
        if self.db.cur.fetchone() is None:
            print("Room not found at this hotel.")
            return

        self.db.cur.execute(
            """
            SELECT 1
            FROM Booking
            WHERE HotelID = %s
              AND RoomNumber = %s
              AND NOT (EndDate < %s OR StartDate > %s);
            """,
            (hotel_id, room_number, start_date, end_date),
        )
        if self.db.cur.fetchone():
            print("Room is not available for this date range.")
            return

        # booking_id = self.get_next_booking_id()
        self.db.cur.execute(
            """
            INSERT INTO Booking (ClientEmail, HotelID, RoomNumber, Price, StartDate, EndDate)
            VALUES (%s, %s, %s, %s, %s, %s);
            """,
            (self.current_client_email, hotel_id, room_number, price_per_day, start_date, end_date,)
        )

        self.db.commit()

        self.db.cur.execute(""" SELECT BookingID FROM Booking
                                 WHERE ClientEmail = %s AND HotelID = %s AND RoomNumber = %s AND Price = %s AND StartDate = %s AND EndDate = %s;""",
                                 (self.current_client_email, hotel_id, room_number, price_per_day, start_date, end_date,)
        )
        row = self.db.cur.fetchone()
        booking_id = row[0]
        
        print(f"Booking successful. BookingID: {booking_id}")

    # Submit review check (4.2.7)
    def submit_review(self):
        hotel_name = input("Enter Hotel Name For Review: ").strip()
        rating = self.read_int("Enter Rating (0-10): ")
        message = input("Enter Review Message: ").strip()

        if rating < 0 or rating > 10:
            print("Rating must be between 0 and 10.")
            return

        hotel_id = self.db.get_hotel_id(hotel_name)
        if hotel_id is None:
            print("Hotel not found.")
            return

        self.db.cur.execute(
            """
            SELECT 1
            FROM Booking
            WHERE ClientEmail = %s
              AND HotelID = %s
              AND EndDate < %s
            LIMIT 1;
            """,
            (self.current_client_email, hotel_id, date.today()),
        )
        if self.db.cur.fetchone() is None:
            print("You can only review hotels where you have previously stayed.")
            return

        review_id = self.get_next_review_id(hotel_id)
        self.db.cur.execute(
            """
            INSERT INTO Review (ReviewID, Message, Rating, ClientEmail, HotelID)
            VALUES (%s, %s, %s, %s, %s);
            """,
            (review_id, message, rating, self.current_client_email, hotel_id),
        )
        self.db.commit()
        print(f"Review {review_id} submitted.")

    # View my bookings (4.2.6)
    def view_my_bookings(self):
        self.db.cur.execute(
            """
            SELECT H.Name, B.HotelID, B.RoomNumber, B.StartDate, B.EndDate, B.Price,
                   ((B.EndDate - B.StartDate + 1) * B.Price) AS TotalCost
            FROM Booking B
            JOIN Hotel H ON H.HotelID = B.HotelID
            WHERE B.ClientEmail = %s
            ORDER BY B.StartDate DESC;
            """,
            (self.current_client_email,),
        )
        rows = self.db.cur.fetchall()

        if not rows:
            print("No bookings found.")
            return

        for row in rows:
            print(
                f"Hotel: {row[0]} ({row[1]}), Room: {row[2]}, Dates: {row[3]} to {row[4]}, "
                f"Price/Day: {row[5]}, Total Cost: {row[6]}"
            )

    # Automatic booking (4.2.5)
    def automatic_booking(self):
        hotel_name = input("Enter Hotel Name: ").strip()
        start_date = self.read_date("Enter Start Date (YYYY-MM-DD): ")
        end_date = self.read_date("Enter End Date (YYYY-MM-DD): ")
        price_per_day = self.read_int("Enter Price Per Day: ")

        if start_date > end_date:
            print("Start date must be on or before end date.")
            return

        hotel_id = self.db.get_hotel_id(hotel_name)
        if hotel_id is None:
            print("Hotel not found.")
            return

        self.db.cur.execute(
            """
            SELECT R.RoomNumber
            FROM Room R
            WHERE R.HotelID = %s
              AND NOT EXISTS (
                  SELECT 1
                  FROM Booking B
                  WHERE B.HotelID = R.HotelID
                    AND B.RoomNumber = R.RoomNumber
                    AND NOT (B.EndDate < %s OR B.StartDate > %s)
              )
            ORDER BY R.RoomNumber
            LIMIT 1;
            """,
            (hotel_id, start_date, end_date),
        )
        room_row = self.db.cur.fetchone()

        if room_row:
            room_number = room_row[0]
            booking_id = self.get_next_booking_id()
            self.db.cur.execute(
                """
                INSERT INTO Booking (BookingID, ClientEmail, HotelID, RoomNumber, Price, StartDate, EndDate)
                VALUES (%s, %s, %s, %s, %s, %s, %s);
                """,
                (booking_id, self.current_client_email, hotel_id, room_number, price_per_day, start_date, end_date),
            )
            self.db.commit()
            print(
                f"Automatic booking successful. Hotel: {hotel_name}, Room: {room_number}, "
                f"Dates: [{start_date}, {end_date}]"
            )
            return

        print("No room available at this hotel for the provided dates.")
        self.db.cur.execute(
            """
            SELECT DISTINCT H.Name
            FROM Hotel H
            JOIN Room R ON R.HotelID = H.HotelID
            WHERE H.HotelID <> %s
              AND NOT EXISTS (
                  SELECT 1
                  FROM Booking B
                  WHERE B.HotelID = R.HotelID
                    AND B.RoomNumber = R.RoomNumber
                    AND NOT (B.EndDate < %s OR B.StartDate > %s)
              )
            ORDER BY H.Name;
            """,
            (hotel_id, start_date, end_date),
        )
        alternatives = [row[0] for row in self.db.cur.fetchall()]

        if alternatives:
            print("Alternatives:")
            for alt in alternatives:
                print(f"- {alt}")
        else:
            print("No alternatives found in this date range.")

    def get_next_booking_id(self):
        self.db.cur.execute(""" SELECT CASE
                                WHEN COUNT(*) = 0 THEN 1
                                ELSE MAX(BookingID) + 1
                                END
                                FROM Booking;""")
        return self.db.cur.fetchone()[0]

    def get_next_review_id(self, hotel_id):
        self.db.cur.execute("""SELECT CASE
                                WHEN COUNT(*) = 0 THEN 1
                                ELSE MAX(ReviewID) + 1
                                END
                                FROM Review
                                WHERE HotelID = %s;""", (hotel_id,))
        return self.db.cur.fetchone()[0]

    @staticmethod
    def read_int(prompt):
        while True:
            try:
                return int(input(prompt))
            except ValueError:
                print("Please enter a valid number.")

    @staticmethod
    def read_date(prompt):
        while True:
            value = input(prompt).strip()
            try:
                return date.fromisoformat(value)
            except ValueError:
                print("Please enter a valid date in YYYY-MM-DD format.")


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
