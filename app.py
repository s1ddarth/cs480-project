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

            if (len(rows) > 0):
                login = True
            else:
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
            print("Test")
        elif query == 10:
            print("Test")
        elif query == 11:
            print("Test")
        elif query == 12:
            print("Test")
        elif query == 13:
            print("Test")
        elif query == 14:
            self.register_manager()
        else:
            print("Unrecognized Request. Please Try Again.")

    def insert_hotel(self):
        new_hotel_id = self.read_int("Please Enter Hotel ID: "))
                    
                    cur.execute("""DELETE FROM Hotel
                                WHERE HotelID = %s;""", (deleteHotelID,))
                    
                    conn.commit()
                    
                # Update Hotel (4.1.2)
                case 3:
                    
                    hotelID = int(input("Please Enter ID Of Hotel To Update: "))
                    newHotelName = input("Please Enter Hotel Name: ")
                    newAddress = input("Please Enter New Hotel's Address: ")

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


                    # If not found, return
                    if hotelID is None:
                        print("Hotel not found.")
                        continue

                    # Then query with hotel ID
                    cur.execute("""DELETE FROM Room
                                WHERE RoomNumber = %s AND HotelID = %s;""", (roomNumber, hotelID,))
                    
                    conn.commit()
                    
                # Update Room (4.1.2)
                case 6:
                    
                    hotelName = input("Please Enter Hotel Name: ")
                    roomNumber = int(input("Please Enter Room Number: "))
                    accessMode = input("Please Enter Access Mode: ")
                    numWindows = int(input("Please Enter Number Of Windows: "))
                    lastRenovatedYear = int(input("Please Enter Last Year Of Renovation: "))

                    # Get associated hotel ID first
                    hotelID = getHotelID(hotelName)

                    # If not found, return
                    if hotelID is None:
                        print("Hotel not found.")
                        continue

                    # Then query with hotel ID
                    cur.execute("""UPDATE Room
                                SET AccessMode = %s, NumWindows = %s, LastRenovatedYear = %s
                                WHERE RoomNumber = %s AND HotelID = %s;""", (accessMode, numWindows, lastRenovatedYear, roomNumber, hotelID,))
                    
                    conn.commit()

                # Remove Clients (4.1.3)
                case 7:
                    
    def remove_client(self):
        # Deletes by client email
        clientEmail = input("Please Enter Client Email To Remove: ")
        self.db.cur.execute("""DELETE FROM Client
                                WHERE Email = %s;""", (clientEmail,))
        self.db.commit()


                    cur.execute("""SELECT C.Name, C.Email, COUNT(*) as booking_count
                                FROM Client C
                                JOIN Booking B ON C.Email = B.ClientEmail
                                GROUP BY C.Name, C.Email
                                ORDER BY booking_count DESC
                                LIMIT %s;
                                """, (kNum,))

                    # Retrieve query results
                    rows = cur.fetchall()
    
                    for row in rows:
                        print(f"Name: {row[0]}, Email: {row[1]}")

                # List of All Hotel Rooms and Number of Bookings (4.1.5)
                case 9:
                    print("Test")
                
                # List of Hotels and Info  (4.1.6)
                case 10:
                    print("Test")

                # Clients to Hotels on cities (4.1.7)
                case 11:
                    print("Test")

                # Problematic Chicago Hotels (4.1.8)
                case 12:
                    print("Test")

                # Clients list and amount spent (4.1.9)
                case 13:
                    print("Test")

                # Add New Manager (4.1.1)
                case 14:
                    
                    newManagerName = input("Please Enter New Manager Name: ")
                    newManagerEmail = input("Please Enter New Manager Email: ")
                    newManagerSSN = input("Please Enter New Manager SSN: ")

                    cur.execute("""INSERT INTO Managers (Name, Email, SSN)
                                 VALUES (%s, %s, %s);
                                 """, (newManagerName, newManagerEmail, newManagerSSN,))
                    
                    conn.commit()

                # Exit
                case -1:
                    break
                
                # Unrecognized
                case _:
                    print("Unrecognized Request. Please Try Again.") 

    # User is Client
    elif (userType == 2):
        print("Test")

    # Unrecognized Type
    else:
        print("Unrecognized")
    

    # Execute a query
    # cur.execute("SELECT id, name FROM users WHERE id < %s;", (10,))

    # Retrieve query results
    # Use fetchall() for all rows, or fetchone() for just one
    # rows = cur.fetchall()
    
    #for row in rows:
    #    print(f"ID: {row[0]}, Name: {row[1]}")

except Exception as e:
    print(f"Error: {e}")

finally:
    # Close communication with the database
    if cur:
        cur.close()
    if conn:
        conn.close()
     