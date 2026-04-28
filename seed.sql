BEGIN;

-- Managers
INSERT INTO Managers (Name, SSN, Email) VALUES
('Alice Manager', '111-11-1111', 'alice.manager@example.com'),
('Bob Manager',   '222-22-2222', 'bob.manager@example.com')
ON CONFLICT (SSN) DO NOTHING;

-- Clients
INSERT INTO Client (Name, Email) VALUES
('Carol Client', 'carol@example.com'),
('Dan Client',   'dan@example.com')
ON CONFLICT (Email) DO NOTHING;

-- Hotels
INSERT INTO Hotel (Name, HotelID, Address) VALUES
('Lakeside Hotel', 'H100', '100 Lake Shore Dr, Chicago, IL'),
('City Inn',       'H200', '200 State St, Chicago, IL')
ON CONFLICT (HotelID) DO NOTHING;

-- Rooms (AccessMode must be 'lift' or 'stairs')
INSERT INTO Room (RoomNumber, HotelID, AccessMode, NumWindows, LastRenovatedYear) VALUES
(101, 'H100', 'lift',   2, 2020),
(102, 'H100', 'stairs', 1, 2018),
(201, 'H200', 'lift',   3, 2022)
ON CONFLICT (RoomNumber, HotelID) DO NOTHING;

-- Addresses (Address.Number is PK in your schema)
INSERT INTO Address (Street, City, Number, CreditCardNumber, ClientEmail, Hotel) VALUES
('Main St',   'Chicago', 1001, 40000001, 'carol@example.com', NULL),
('Oak Ave',   'Chicago', 1002, 40000002, 'dan@example.com',   NULL),
('Pine Blvd', 'Evanston', 1003, NULL,    'carol@example.com', NULL)
ON CONFLICT (Number) DO NOTHING;

-- Credit cards (BillingAddressID must exist in Address.Number)
INSERT INTO CreditCard (CreditCardNumber, ClientEmail, BillingAddressID) VALUES
('4111111111111111', 'carol@example.com', 1001),
('4222222222222222', 'dan@example.com',   1002)
ON CONFLICT (CreditCardNumber) DO NOTHING;

-- Bookings
INSERT INTO Booking (BookingID, ClientEmail, HotelID, RoomNumber, Price, StartDate, EndDate) VALUES
(1, 'carol@example.com', 'H100', 101, 120, '2026-05-10', '2026-05-12'),
(2, 'dan@example.com',   'H200', 201, 150, '2026-05-15', '2026-05-18')
ON CONFLICT (BookingID) DO NOTHING;

-- Reviews
INSERT INTO Review (ReviewID, Message, Rating, ClientEmail, HotelID) VALUES
(1, 'Great stay', 9, 'carol@example.com', 'H100'),
(1, 'Good overall', 8, 'dan@example.com', 'H200')
ON CONFLICT (ReviewID, HotelID) DO NOTHING;

COMMIT;
