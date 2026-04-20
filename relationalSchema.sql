--3.8 Credit Card
CREATE TABLE CreditCard (  --strong entity
    CreditCardNumber VARCHAR(30),
    ClientEmail VARCHAR(100),
    BillingAddressID INT,
    PRIMARY KEY (CreditCardNumber),
    FOREIGN KEY (ClientEmail) REFERENCES Client(Email),
    FOREIGN KEY (BillingAddressID) REFERENCES Address(Number)
);

--3.7 Address
CREATE TABLE Address (   --strong entity
    Street VARCHAR(50),
    City VARCHAR(50),
    Number INT,
    CreditCardNumber INT,
    ClientEmail VARCHAR(100),
    Hotel VARCHAR(100),
    PRIMARY KEY (Number),
    FOREIGN KEY (ClientEmail) REFERENCES Client(Email),
    FOREIGN KEY (Hotel) REFERENCES Hotel(HoetelID),
    FOREIGN KEY (CreditCardNumber) REFERENCES CreditCard(CreditCardNumber)
);

--3.2 Client
CREATE TABLE Client (   --strong entity
    Name VARCHAR(50),
    Email VARCHAR(100),
    PRIMARY KEY (Email)
);

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

CREATE TABLE Room (
    RoomNumber INT,
    HotelID INT,
    AccessMode VARCHAR(10),
    NumWindows INT DEFAULT 0,
    LastRenovatedYear INT,
    PRIMARY KEY  (RoomNumber, HotelID),
    FOREIGN KEY (HotelID) REFERENCES Hotel,
    CONSTRAINT chk_access CHECK (AccessMode IN ('lift', 'stairs')),
);

CREATE TABLE Review (
    ReviewID INT,
    Message VARCHAR(500),
    Rating INT,
    ClientEmail VARCHAR(100),
    HotelID INT,
    PRIMARY KEY  (ReviewID, HotelID),
    FOREIGN KEY (HotelID) REFERENCES Hotel,
    FOREIGN KEY (ClientID) REFERENCES Client(Email),
    CONSTRAINT chk_rating CHECK (Rating BETWEEN 1 AND 5)
);
