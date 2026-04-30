-- BEGIN;

-- -- Managers
-- INSERT INTO Managers (Name, SSN, Email) VALUES
-- ('Alice Manager', '111-11-1111', 'alice.manager@example.com'),
-- ('Bob Manager',   '222-22-2222', 'bob.manager@example.com')
-- ON CONFLICT (SSN) DO NOTHING;

-- -- Clients
-- INSERT INTO Client (Name, Email) VALUES
-- ('Carol Client', 'carol@example.com'),
-- ('Dan Client',   'dan@example.com')
-- ON CONFLICT (Email) DO NOTHING;

-- -- Hotels
-- INSERT INTO Hotel (Name, HotelID, Address) VALUES
-- ('Lakeside Hotel', 1, '100 Lake Shore Dr, Chicago, IL'),
-- ('City Inn',       2, '200 State St, Chicago, IL')
-- ON CONFLICT (HotelID) DO NOTHING;

-- -- Rooms (AccessMode must be 'lift' or 'stairs')
-- INSERT INTO Room (RoomNumber, HotelID, AccessMode, NumWindows, LastRenovatedYear) VALUES
-- (101, 'H100', 'lift',   2, 2020),
-- (102, 'H100', 'stairs', 1, 2018),
-- (201, 2, 'lift',   3, 2022)
-- ON CONFLICT (RoomNumber, HotelID) DO NOTHING;

-- -- Addresses (Address.Number is PK in your schema)
-- INSERT INTO Address (Street, City, Number, CreditCardNumber, ClientEmail, Hotel) VALUES
-- ('Main St',   'Chicago', 1001, 40000001, 'carol@example.com', NULL),
-- ('Oak Ave',   'Chicago', 1002, 40000002, 'dan@example.com',   NULL),
-- ('Pine Blvd', 'Evanston', 1003, NULL,    'carol@example.com', NULL)
-- ON CONFLICT (Number) DO NOTHING;

-- -- Credit cards (BillingAddressID must exist in Address.Number)
-- INSERT INTO CreditCard (CreditCardNumber, ClientEmail, BillingAddressID) VALUES
-- ('4111111111111111', 'carol@example.com', 1001),
-- ('4222222222222222', 'dan@example.com',   1002)
-- ON CONFLICT (CreditCardNumber) DO NOTHING;

-- -- Bookings
-- INSERT INTO Booking (BookingID, ClientEmail, HotelID, RoomNumber, Price, StartDate, EndDate) VALUES
-- (1, 'carol@example.com', 'H100', 101, 120, '2026-05-10', '2026-05-12'),
-- (2, 'dan@example.com',   2, 201, 150, '2026-05-15', '2026-05-18')
-- ON CONFLICT (BookingID) DO NOTHING;

-- -- Reviews
-- INSERT INTO Review (ReviewID, Message, Rating, ClientEmail, HotelID) VALUES
-- (1, 'Great stay', 9, 'carol@example.com', 'H100'),
-- (1, 'Good overall', 8, 'dan@example.com', 2)
-- ON CONFLICT (ReviewID, HotelID) DO NOTHING;

-- COMMIT;
-- ROLLBACK

-- DROP SCHEMA public CASCADE;
-- CREATE SCHEMA public;
-- GRANT ALL ON SCHEMA public TO postgres; -- Replace 'postgres' with your username (mine is postgres)
-- GRANT ALL ON SCHEMA public TO public;

-- SELECT * from Address

BEGIN;

-- 1. Addresses (Must come first so IDs exist)
-- Assuming AddressID is SERIAL or IDENTITY
INSERT INTO Address (Street, City) VALUES
('100 Lake Shore Dr', 'Chicago'), -- ID 1
('200 State St', 'Chicago'),      -- ID 2
('123 Main St', 'Chicago'),       -- ID 3 (Carol Res)
('456 Oak Ave', 'Chicago'),       -- ID 4 (Dan Res)
('789 Billing Way', 'Evanston'),  -- ID 5 (Carol Billing)
('321 Credit Ln', 'Chicago')      -- ID 6 (Dan Billing)
('123 Main St', 'Naperville'),       -- ID 3 (Carol Res)
('456 Oak Ave', 'Chicago'),       -- ID 4 (Dan Res)
('789 Billing Way', 'Evanston'),  -- ID 5 (Carol Billing)
('321 Credit Ln', 'Chicago'),      -- ID 6 (Dan Billing)
('342 Elm St',  'Oak Forest')     -- ID 7 (Lexi Res)
ON CONFLICT DO NOTHING;

-- 2. Managers
INSERT INTO Managers (Name, SSN, Email) VALUES
('Alice Manager', '111-11-1111', 'alice.manager@example.com'),
('Bob Manager',   '222-22-2222', 'bob.manager@example.com')
ON CONFLICT (SSN) DO NOTHING;


-- 3. Hotels (Now links to AddressID)
-- Assuming Lakeside is Address 1, City Inn is Address 2
INSERT INTO Hotel (Name, AddressID) VALUES
('Lakeside Hotel', 1),
('City Inn', 2)
ON CONFLICT (HotelID) DO NOTHING;

-- 4. Clients (Now links to AddressID)
-- Carol is Address 3, Dan is Address 4
INSERT INTO Client (Name, Email, AddressID) VALUES
('Carol Client', 'carol@example.com', 3),
('Dan Client',   'dan@example.com',   4),
('lexi Client',  'lexi@example.com',  7)
ON CONFLICT (Email) DO NOTHING;

-- 5. Credit Cards (Links to ClientEmail and BillingAddressID)
-- Carol's Bill is Address 5, Dan's Bill is Address 6
INSERT INTO CreditCard (CreditCardNumber, ClientEmail, BillingAddressID) VALUES
('4111111111111111', 'carol@example.com', 5),
('4222222222222222', 'dan@example.com',   6)
ON CONFLICT (CreditCardNumber) DO NOTHING;

-- 6. Rooms
INSERT INTO Room (RoomNumber, HotelID, AccessMode, NumWindows, LastRenovatedYear) VALUES
(101, 1, 'lift',   2, 2020),
(102, 1, 'stairs', 1, 2018),
(201, 2, 'lift',   3, 2022)
ON CONFLICT (RoomNumber, HotelID) DO NOTHING;

-- 7. Bookings
INSERT INTO Booking (ClientEmail, HotelID, RoomNumber, Price, StartDate, EndDate) VALUES
('carol@example.com', 1, 101, 120, '2026-05-10', '2026-05-12'),
('dan@example.com',   2, 201, 150, '2026-05-15', '2026-05-18'),
('lexi@example.com',  1, 102, 134, '2026-05-20', '2026-05-23')
ON CONFLICT (BookingID) DO NOTHING;

-- 8. Reviews
INSERT INTO Review (Message, Rating, ClientEmail, HotelID) VALUES
( 'Great stay', 1, 'carol@example.com', 1),
( 'Good overall', 8, 'dan@example.com', 2),
( 'Bad service', 1, 'lexi@example.com', 1)
ON CONFLICT (ReviewID, HotelID) DO NOTHING;

COMMIT;