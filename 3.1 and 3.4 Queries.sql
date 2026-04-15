-- 3.1 Managers
CREATE TABLE Managers (
	Name VARCHAR,
	SSN CHAR(11),
	Email VARCHAR,
	PRIMARY KEY (SSN)
);

-- 3.4 Hotel
CREATE TABLE Hotel (
	Name VARCHAR,
	HotelID CHAR(15),
	Address VARCHAR,
	PRIMARY KEY (HotelID)
);