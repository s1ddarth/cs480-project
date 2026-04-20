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
	PRIMARY KEY (Email)
);

-- 3.4 Hotel
CREATE TABLE Hotel (
	Name VARCHAR(100) NOT NULL,
	HotelID VARCHAR(15) NOT NULL,
	Address VARCHAR(500) NOT NULL,
	PRIMARY KEY (HotelID)
);

-- 3.5 Room
CREATE TABLE Room (
	RoomNumber INT NOT NULL,
	HotelID VARCHAR(15) NOT NULL,
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
    Number INT,
    CreditCardNumber INT,
    ClientEmail VARCHAR(100),
    Hotel VARCHAR(15),
    PRIMARY KEY (Number),
    FOREIGN KEY (ClientEmail) REFERENCES Client(Email),
    FOREIGN KEY (Hotel) REFERENCES Hotel(HotelID)
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
    BookingID INT,
    ClientEmail VARCHAR(100),
    RoomNumber INT,
    Price INT CHECK (Price >= 0),
    Dates DATETIME NOT NULL,
    FOREIGN KEY (ClientID) REFERENCES Client(Email),
    FOREIGN KEY (RoomNumber) REFERENCES Room(RoomNumber),
    PRIMARY KEY (BookingID, ClientEmail, RoomNumber)
);

-- 3.6 Review
CREATE TABLE Review (
    ReviewID INT,
    Message VARCHAR(500),
    Rating INT,
    ClientEmail VARCHAR(100),
    HotelID INT,
    PRIMARY KEY  (ReviewID, HotelID),
    FOREIGN KEY (HotelID) REFERENCES Hotel(HotelID),
    FOREIGN KEY (ClientID) REFERENCES Client(Email),
    CONSTRAINT chk_rating CHECK (Rating BETWEEN 0 AND 10)
);

