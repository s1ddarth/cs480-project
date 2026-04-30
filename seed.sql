BEGIN;

-- 1. Addresses (Must come first so IDs exist)
-- Assuming AddressID is SERIAL or IDENTITY
INSERT INTO Address (Street, City) VALUES
('100 Lake Shore Dr', 'Chicago'), -- ID 1
('200 State St', 'Chicago'),      -- ID 2
('123 Main St', 'Naperville'),    -- ID 3 (Carol Res)
('456 Oak Ave', 'Chicago'),       -- ID 4 (Dan Res)
('789 Billing Way', 'Evanston'),  -- ID 5 (Carol Billing)
('321 Credit Ln', 'Chicago')      -- ID 6 (Dan Billing)
ON CONFLICT DO NOTHING;

-- 2. Managers
INSERT INTO Managers (Name, SSN, Email) VALUES
('Alice Manager', '111-11-1111', 'alice.manager@example.com'),
('Bob Manager',   '222-22-2222', 'bob.manager@example.com')
ON CONFLICT (SSN) DO NOTHING;

-- 3. Hotels (Now links to AddressID)
-- Assuming Lakeside is Address 1, City Inn is Address 2
INSERT INTO Hotel (Name, AddressID) VALUES
(
  'Lakeside Hotel',
  (SELECT Number FROM Address WHERE Street = '100 Lake Shore Dr' AND City = 'Chicago')
),
(
  'City Inn',
  (SELECT Number FROM Address WHERE Street = '200 State St' AND City = 'Chicago')
)
ON CONFLICT (HotelID) DO NOTHING;

-- 4. Clients (Now links to AddressID)
-- Carol is Address 3, Dan is Address 4
INSERT INTO Client (Name, Email, AddressID) VALUES
('Carol Client', 'carol@example.com',
	(SELECT Number FROM Address WHERE Street = '123 Main St' AND City = 'Naperville')
),
('Dan Client', 'dan@example.com',
	(SELECT Number FROM Address WHERE Street = '456 Oak Ave' AND City = 'Chicago')
)
ON CONFLICT (Email) DO NOTHING;

-- 5. Credit Cards (Links to ClientEmail and BillingAddressID)
-- Carol's Bill is Address 5, Dan's Bill is Address 6
INSERT INTO CreditCard (CreditCardNumber, ClientEmail, BillingAddressID) VALUES
('4111111111111111', 'carol@example.com', 
	(SELECT Number FROM Address WHERE Street = '789 Billing Way' AND City = 'Evanston')
),
('4222222222222222', 'dan@example.com', 
	(SELECT Number FROM Address WHERE Street = '321 Credit Ln' AND City = 'Chicago')
)
ON CONFLICT (CreditCardNumber) DO NOTHING;

-- 6. Rooms
INSERT INTO Room (RoomNumber, HotelID, AccessMode, NumWindows, LastRenovatedYear) VALUES
(101, 
	(SELECT HotelID FROM Hotel WHERE Name = 'Lakeside Hotel'), 
	'lift',
	2,
	2020
),
(102,
	(SELECT HotelID FROM Hotel WHERE Name = 'Lakeside Hotel'),
	'stairs',
	1,
	2018
),
(201,
	(SELECT HotelID FROM Hotel WHERE Name = 'City Inn'),
	'lift',
	3,
	2022
)
ON CONFLICT (RoomNumber, HotelID) DO NOTHING;

-- 7. Bookings
INSERT INTO Booking (ClientEmail, HotelID, RoomNumber, Price, StartDate, EndDate) VALUES
('carol@example.com',
	(SELECT HotelID FROM Hotel WHERE Name = 'Lakeside Hotel'),
	101,
	120,
	'2026-05-10',
	'2026-05-12'
),
('dan@example.com',
	(SELECT HotelID FROM Hotel WHERE Name = 'City Inn'),
	201,
	150,
	'2026-05-15',
	'2026-05-18'
)
ON CONFLICT (BookingID) DO NOTHING;

-- 8. Reviews
INSERT INTO Review (Message, Rating, ClientEmail, HotelID) VALUES
('Great stay',
	9,
	'carol@example.com',
	(SELECT HotelID FROM Hotel WHERE Name = 'Lakeside Hotel')
),
('Good overall',
	8,
	'dan@example.com',
	(SELECT HotelID FROM Hotel WHERE Name = 'City Inn')
)
ON CONFLICT (ReviewID, HotelID) DO NOTHING;

COMMIT;