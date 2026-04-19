--3.8 Credit Card
CREATE TABLE CreditCard {  --strong entity
    CreditCardNumber VARCHAR(30),
    ClientEmail VARCHAR(100),
    BillingAddressID INT,
    PRIMARY KEY (CreditCardNumber),
    FOREIGN KEY (ClientEmail) REFERENCES Client(Email),
    FOREIGN KEY (BillingAddressID) REFERENCES Address(Number)
};

--3.7 Address
CREATE TABLE Address {   --strong entity
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
};

--3.2 Client
CREATE TABLE Client {   --strong entity
    Name VARCHAR(50),
    Email VARCHAR(100),
    PRIMARY KEY (Email)
};
