## CS480 - Project

## 1  Project
The project has three deliverables. Each group will demo their application at the end of the
semester. The deliverables are:
-  ER-model: Each group should develop an ER-model for the application. This can be uploaded as a pdf file on gradescope. (please do not use esoteric formats). Deadline: April 9.
- Relational schema:  The second deliverable is a translation of the ER-model into a relational schema implemented as an SQL script.  The script should use Postgres’s SQL dialect. Please upload the script as a simple .sql file on gradescope. Deadline: April 16
- The last deliverable is an online taxi rental management application that uses the relational schema defined in the first two deliverables. This application can be either a web or desktop application. Deadline: April 29

Each group should have three or four members. If you cannot find a group please send me on piazza or an email and I will assign you to a group.

## 2  Overview
The goal is to build a hotel management application.  There will be two roles: managers and clients. A manager can add or delete rooms and clients from the system, and retrieve statistics about clients, rooms, ratings, etc. A client can search for available rooms, book a room, and manage their addresses and credit card information.

### 3  Data Requirements
You should not use any `n-ary` relationship for `n>2`.  You should not use any outer join operator.

### 3.1  Managers
For every manager we store the name, the SSN (which is also the key), and the email.

### 3.2  Client
Every client should register with their name and email address. The email address must be unique. Each client should have at least one address, and possibly multiple addresses. Each client should also have at least one credit card. A client should be able to book a room in one of the hotels for a given date range (provided that the room is available; see below). Finally, a client may write a review for a hotel where they have booked a room.

### 3.3  Booking
Each booking is associated with exactly one client and exactly one hotel room. The booking should store the start and end dates of the booking, a unique booking id, and the price per day. If a client books a room from date `x` to date `y`, then no other booking for the same room can overlap with the interval `[x, y]`.

### 3.4  Hotel
For every hotel we store its name and address. Every hotel has a unique hotel id.

### 3.5  Room
For every room we store the number of windows, the year of last renovation, and whether
access is via elevator or stairs. A room is uniquely identified by the hotel and room number.

### 3.6  Review
A review consists of a message and a rating (integer from 0 to 10). A review is uniquely identified by a hotel and a reviewid.

### 3.7  Address
Every address consists of a street name, number, and city.

### 3.8  Credit card
A credit card belongs to exactly one client and stores the credit card number. Each credit card has exactly one billing address.

## 4  Application requirements
The application should support the following actions for managers and clients.

### 4.1  Managers
1. A user can register as a manager by providing name, SSN, and email. A registered manager can log in using their SSN.
2.  Managers should be able to insert, remove, and update hotels and rooms.
3.  Managers should be able to remove clients from the system.
4. Managers should be able to input a number `k`, and the system should return the names and emails of the top-k clients based on the number of bookings.
5. Managers should be able to generate a list of all hotel rooms along with the number of bookings for each room.
6. Managers should be able to generate a list: for every hotel `X` show the name of `X`, the total number of bookings in `X`, and the average rating of `X`.
7. A manager should be able to input two cities C1 and C2, and the system should return the names and emails of clients who have at least one address in C1 and have booked a hotel located in C2
8. Managers should be able to report the names of problematic local hotels. These are hotels located in Chicago with an average rating less than 2, and that have been booked by at least two different clients, each of whom has no address in city Chicago.
9. Managers should be able to report a list showing each client’s name along with the total amount they have spent on bookings.

### 4.2  Clients
1. When registering, a client should provide their name and email address, along with their address(es) and credit card(s). Note that a client may have an address X, while a credit card may have a billing address Y different from X. A registered client can log in using their email.
2. A client should be able to update their information (except their email), including name, addresses, and credit cards.
3. A client should be able to input a start date and end date and view all available hotel rooms (including hotel name and room number). A room is available for `[x,y]` if no booking overlaps with that interval.
4. A client should be able to book a specific room for a given date range if it is available.
5. There is also an option for automatic booking. The client provides a hotel H and a date range `[x,y]`. The system automatically books a room in H if one is available. If successful, the system reports the room, the hotel (i.e. H), and booking dates (i.e., `[x,y]`).  Otherwise, it reports that no room is available at this hotel and suggests (if exist) all alternative hotels that have at least an available room in `[x,y]`.
6. A client should be able to view all their bookings, including the room, hotel name, and cost.
7. A client should be able to submit a review for a hotel only if they have previously stayed there.