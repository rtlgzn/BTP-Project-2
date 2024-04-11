# Cloud-Based-Restaurant-Reservation-System

# Development Process

## System Architecture (design) used: 

For this project I decided to use a microservice architecture style approach the reason why I chose this approach is because this type of architecture can have many benefits:

- Scalability: The microservices can be scaled on an independent level based on the demand. If one of the services scales with a lot of traffic then that service will be scaled up without touching the other parts of my application
- Maintenance: These microservices are independent and loosely coupled. This allows easy maintenance with the application
- Agility: Each microservice is small and can focus on a specific function allowing for easier management
- Many aspects: In a microservice style each microservice is referred to a different aspect of the overall application: In a PHR system we can have one service responsible for the (user auth, user registration, etc (frontend)) and other for the creation, retrieving, updating and deleting records (CRUD).

## Vision Statement

`FOR` individuals `WHO` need to manage, update and cancel reservations for a restaurant system. `THE` cloud-based restaurant reservation system is a tool to achieve these tasks `THAT` allows the user to create new reservations, update pre existing reservations and delete reservations (cancel). Additionally the system allows users to register for an account before making the reservation to their desired restaurant. These features can be done via APIS. `UNLIKE` traditional restaurant reservation systems, this system asks the user to register for an account in which the user will have access to multiple restaurants. This will act like a central system in which the user can make a reservation to different restaurants, saving the user time as they don’t have to go to different websites for different restaurants. `OUR` product lets the user manage their reservations in a secure environment with the proper security measures to ensure that no sensitive data gets leaked to anyone beside them and the restaurant in which they made the reservation to. 

FORMAT USED: (Moore’s vision template)

- FOR (target customer)
- WHO (statement of the need or opportunity)
- THE (Product name) is a (product category)
- THAT (key benefit, compelling reason to buy)
- UNLIKE (primary competitive alternative)
- OUR PRODUCT (statement of primary differentiation

## Personas

Persona one:  Sam Cill

- Age: 45
- Occupation: Business man 
- Currently needs: since Sam is a busy man, he doesn’t have time to search for multiple restaurants to choose a booking 
- What the restaurant reservation system does for them: the reservation system allows Sam to search for different restaurants from one central website. Saving him time and effort.

Persona two:  Sheila Shoon, Housewife (children two)
- Age: 45
- Occupation: Housewife 
- Currently needs: this household books for multiple people every week at least one time making them a frequent outside eater. They want the system to apply corresponding promotions and coupons with applicable. 
- What the restaurant reservation system does for them: the system automatically applies coupons and discounts when they book for the reservation so when they arrive at the restaurant they will get a discount. 

Persona three: Mike Loop
- Age: 30
- Occupation: Restaurant Manager 
- Currently needs: A way to manage incoming restaurant reservations in a fast and effective way with a easy to use user interface for optimal use
- What the restaurant reservation system does for them:  the system allows this user to manage the current reservations by allowing them to update, or cancel (remove) the current reservations that have been made in the system.

## Scenarios and user stories:

- `Name`: Sam Cill
- Scenario: While at work Sam realises that he forgot to book for a reservation at a restaurant. He doesn’t have time to go to multiple restaurant websites to see which one is optimal. 
- User Story: As Sam a busy business man, I want to search for different restaurants from one place so I can save time and effort

- `Name`: Sheila Shoon
- Scenario: It’s Thursday morning and Sheila plans to go to a restaurant with her two kids tomorrow but wants to get the best deals for her order, she wants all available coupons to be applied to her reservation so when she goes they are ready. 
- User Story: As Sheila A housewife, I want to have available coupons applied to my reservation so when I go to the restaurant those coupons automatically apply to my checkout.

- `Name`: Mike Loop
- Scenario: When Mike arrives to work, his staff complains of not having an automatic system in place to manage incoming reservations, and to edit user information. Incoming reservations sometimes get messed up due to this system not being in place.
- User Story: As Mike a restaurant manager, I want incoming reservations to be managed by a system so it lighten’s the staff workload

## System Architecture Diagram 

![image](https://github.com/KabeerH/Cloud-Based-Restaurant-Reservation-System/assets/122492914/bb93063e-fa62-4056-94cd-c5418f1099e3)



# Restaurant Reservation System Documentation

## Overview of Application

This application is a system that uses the built-in package `http.server`  to handle HTTP requests that allow the user to create, recieve, update and delete requests. For data storage I am using a MySQL database that is implemented inside my code where if the database is not presented then make one database and the associated tables (One for user's and one for reservations) - Backend. For the frontend I have used next.js to provide a responsive user interface that using the methods from my backend (server.py) to securely add, create, update and delete actions.

## Tools and Technology Used
- Programming Language(s): Python for backend, javascript (next.js) for frontend 
- Database: SQLite
- Version Control: Git 
- Containerization: Docker
- API Testing: Postman

## Getting Started (local run)

1. Clone the repository using the command in cmd
```bash
git clone https://github.com/KabeerH/Cloud-Based-Restaurant-Reservation-System
```
2. Change to the directory where you have cloned the project
```bash
cd directory
```
4. Naviagate to the ./backend and create a .env file import the following line:
```bash
DB_NAME = 'reservation_db'
```
5. To build the project using docker
```bash 
docker-compose up --build
```
6. To start the project if not started
```bash 
docker-compose up 
```
7. To Stop the application and delete the container
```bash
docker-compose down
```

Once the application is started, you can go to http://localhost:3000 to access the frontend application and http://localhost:8000 to access api calls

## METHODS Functions (POSTMAN)

Before accessing the system you have to: 

- `Register`: To start using the Restaurant Reservation system you must register for an account. To do this send a POST request to the /register endpoint or go to http://localhost:3000/register after starting the application. Register with a “username”, “password”, and "email" field. Example below: 

  ![image](https://github.com/KabeerH/Cloud-Based-Restaurant-Reservation-System/assets/122492914/1d81f6c1-382e-4a65-9dd9-5180e3434f24)

- `Log In`:  After you have registered for an account then you can login by first sending a POST request to the /login endpoint or go to  http://localhost:3000/login after starting the application. Login with the "username" and "password". The credentials you registered with. The response should give you a "jwt token" in response. Input the token value into "Auth -> Bearer Token -> set token value". Example below:

  ![image](https://github.com/KabeerH/Cloud-Based-Restaurant-Reservation-System/assets/122492914/242b7315-3ad0-4918-bf33-acce235e8f1b)
  ![image](https://github.com/KabeerH/Cloud-Based-Restaurant-Reservation-System/assets/122492914/607ec6c8-b868-4081-98e6-67f34f5512ee)


Now you should be able to access the following endpoints. If the Bearer Token value is incorrect then you should be returned with "Invaild token" response.

### GET (ALL) /reservations

This endpoint retrieves all reservations from the database.

- Method: `GET`
- URL: `/reservations`

**Usage with Postman:**
1. Set the HTTP method to `GET`.
2. Enter the request URL as `http://localhost:8000/reservations`.
3. Click on `Send` to make the request.

![image](https://github.com/KabeerH/Cloud-Based-Restaurant-Reservation-System/assets/122492914/b20a61c2-3f2f-4275-9967-94766dc95748)


### POST /reservations

This endpoint creates a new reservation in the database.

- Method: `POST`
- URL: `/reservations`
- Request Body: A JSON object containing 'date', 'time' and 'party_size'
  
**Usage with Postman:**
1. Set the HTTP method to `POST`.
2. Enter the request URL as `http://localhost:8000/reservations`.
3. Click on `Body`, then select `raw` and `JSON`.
4. In the text field, enter your reservation in the format: 'date', 'time', 'party_size'
5. Click on `Send` to make the request.

![image](https://github.com/KabeerH/Cloud-Based-Restaurant-Reservation-System/assets/122492914/76768bc4-a247-4fe3-bb3f-0acdd13c8d1e)

### PUT /reservations/:id

This endpoint updates an existing reservation in the database.

- Method: `PUT`
- URL: `/reservations`
- Request Body: A JSON object containing 'date', 'time', 'party_size'

**Usage with Postman:**
1. Set the HTTP method to `PUT`.
2. Enter the request URL as `http://localhost:8000/reservations/:id`.
3. Click on `Body`, then select `raw` and `JSON`.
4. In the text field, enter your reservation in the following format: 'date', 'time', 'party_size'
5. Click on `Send` to make the request.

![image](https://github.com/KabeerH/Cloud-Based-Restaurant-Reservation-System/assets/122492914/13f74791-6aca-44ea-a778-74bac8bf6d82)

### DELETE /reservations/:id

This endpoint deletes a reservation from the database.

- Method: `DELETE`
- URL: `/reservations/:id`

**Usage with Postman:**
1. Set the HTTP method to `DELETE`.
2. Enter the request URL as `http://localhost:8000/reservations/:id`.
3. change reservation id with the id you trying to delete
4. Click on `Send` to make the request

![image](https://github.com/KabeerH/Cloud-Based-Restaurant-Reservation-System/assets/122492914/cfafbc83-c32b-43af-aca4-f01fdc00ddbe)

## Security precautions made: 

- User Authentication: Using JWT Token Authentication the system first verifies the identity of the user. When making any request to the system it checks the user’s credentials against the users table in the reservation_db database. This JWT token value will be random everytime to ensure timeout if the user is logged in for too long (inactive).  If the user credentials also don't match then display a error message

  ![image](https://github.com/KabeerH/Cloud-Based-Restaurant-Reservation-System/assets/122492914/cd35f2f4-05fe-4810-860a-1cf4996b5b55)

- Password Hashing: Whenever a new user is added to the system, their data is hashed using the bcrypt python library and salting the password before storing the data into the SQlite database, if someone gets access to the users table then the data won’t show their password but instead hashed values.

  ![image](https://github.com/KabeerH/Cloud-Based-Restaurant-Reservation-System/assets/122492914/c3c84300-c0d4-4849-8872-2bbb9d2f1f1d)

- Access Control: The reservations are associated with the user_id, the system will check which user_id is trying to access what data and only return the data associated with that user ensuring data security.

  ## Contributors 

- Kabeer Harjani | https://github.com/KabeerH

