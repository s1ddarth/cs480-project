-- 3.1 Managers
CREATE TABLE Managers (
	Name VARCHAR(100) NOT NULL,
	SSN CHAR(11) NOT NULL,
	Email VARCHAR(100) NOT NULL,
	PRIMARY KEY (SSN)
);

-- 3.2 Client
CREATE TABLE Client (
	Name VARCHAR(100) NOT NULL,
	Email VARCHAR(100) NOT NULL,
    AddressID INT NOT NULL,
	PRIMARY KEY (Email),
    FOREIGN KEY (AddressID) REFERENCES Address
);

-- 3.4 Hotel
CREATE TABLE Hotel (
	Name VARCHAR(100) NOT NULL,
	HotelID INT GENERATED ALWAYS AS IDENTITY NOT NULL,
	AddressID INT NOT NULL,
	PRIMARY KEY (HotelID),
    FOREIGN KEY (AddressID) REFERENCES Address
);

-- 3.5 Room
CREATE TABLE Room (
	RoomNumber INT NOT NULL,
	HotelID INT NOT NULL,
	AccessMode VARCHAR(10) NOT NULL,
	NumWindows INT NOT NULL DEFAULT 0,
	LastRenovatedYear INT,
	PRIMARY KEY (RoomNumber, HotelID),
	FOREIGN KEY (HotelID) REFERENCES Hotel (HotelID),
	CONSTRAINT chk_access CHECK (AccessMode IN ('lift', 'stairs'))
);

-- 3.7 Address
CREATE TABLE Address (   --strong entity
    Street VARCHAR(50),
    City VARCHAR(50),
    Number INT GENERATED ALWAYS AS IDENTITY,
    -- CreditCardNumber INT,
    -- ClientEmail VARCHAR(100),
    -- Hotel VARCHAR(15),
    PRIMARY KEY (Number),
    -- FOREIGN KEY (ClientEmail) REFERENCES Client(Email),
    -- FOREIGN KEY (Hotel) REFERENCES Hotel(HotelID)
);

-- 3.8 Credit Card
CREATE TABLE CreditCard (  --strong entity
    CreditCardNumber VARCHAR(30) NOT NULL,
    ClientEmail VARCHAR(100) NOT NULL,
    BillingAddressID INT NOT NULL,
    PRIMARY KEY (CreditCardNumber),
    FOREIGN KEY (ClientEmail) REFERENCES Client(Email),
    FOREIGN KEY (BillingAddressID) REFERENCES Address(Number)
);

-- 3.3 Booking
CREATE TABLE Booking (
    BookingID INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    ClientEmail VARCHAR(100),
    HotelID VARCHAR(15),
    RoomNumber INT,
    Price INT CHECK (Price >= 0),
    StartDate DATE NOT NULL,
    EndDate DATE NOT NULL,
    FOREIGN KEY (ClientEmail) REFERENCES Client(Email),
    FOREIGN KEY (HotelID, RoomNumber) REFERENCES Room(HotelID, RoomNumber),
    CONSTRAINT chk_booking_dates CHECK (StartDate <= EndDate)
);

-- 3.6 Review
CREATE TABLE Review (
    ReviewID INT GENERATED ALWAYS AS IDENTITY,
    Message VARCHAR(500),
    Rating INT,
    ClientEmail VARCHAR(100),
    HotelID VARCHAR(15),
    PRIMARY KEY  (ReviewID, HotelID),
    FOREIGN KEY (HotelID) REFERENCES Hotel(HotelID),
    FOREIGN KEY (ClientEmail) REFERENCES Client(Email),
    CONSTRAINT chk_rating CHECK (Rating BETWEEN 0 AND 10)
);

