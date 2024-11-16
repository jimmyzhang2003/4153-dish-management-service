# 4153-dish-management-service

This is a Flask-based microservice that connects to a MySQL database and provides RESTful endpoints for creating, retrieving, updating, and deleting dish records.

## REST Endpoints

### Dish Endpoints

- **POST /api/v1/dishes**: Create a new dish
- **GET /api/v1/dishes**: Retrieve a list of dishes (with optional filtering by name and category)
- **GET /api/v1/dishes/{id}**: Retrieve detailed information about a specific dish
- **PUT /api/v1/dishes/{id}**: Update details of an existing dish
- **DELETE /api/v1/dishes/{id}**: Delete a dish

### Dining Hall Endpoints

- **GET /api/v1/dining_halls**: Retrieve a list of all dining halls (with optional filtering by name)
- **POST /api/v1/dining_halls**: Create a new dining hall
- **DELETE /api/v1/dining_halls/{id}**: Delete a dining hall
- **GET /api/v1/stations**: Retrieve a list of all stations (with optional filtering by name)
- **GET /api/v1/dining_halls/{id}/stations**: Retrieve all the stations within a specific dining hall (with optional filtering by name)
- **POST /api/v1/dining_halls/{id}/stations**: Create a new station to a particular dining hall
- **DELETE /api/v1/dining_halls/{id}/stations/{station_id}**: Delete a station within a specific dining hall

## Prerequisites

- Python 3.10 (for local development)
- Docker (for containerized development)
- MySQL Server
- `pip` for dependency management
- libraries in `requirements.txt`

## Setup Instructions

1. **Clone the Repository**

   ```bash
   git clone https://github.com/jimmyzhang2003/4153-dish-management-service.git
   cd 4153-dish-management-microservice
   ```

2. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables**

   Create a `.env` file in the root directory with the following variables:

   ```env
   DB_ENGINE=your-database-engine
   DB_USER=your-database-username
   DB_PASSWORD=your-database-password
   DB_HOST=your-database-host
   DB_PORT=your-database-port
   DB_NAME=your-database-name
   ```

4. **Create Database and Table**

   Ensure that your MySQL database has a `dishes` table, a `dining_halls` table, and a `stations` table:

   ```sql
    CREATE TABLE dining_halls (
        id INT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(255) NOT NULL UNIQUE
    );

    CREATE TABLE stations (
        id INT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(255) NOT NULL,
        dining_hall_id INT NOT NULL,
        FOREIGN KEY (dining_hall_id) REFERENCES dining_halls(id) ON DELETE CASCADE
    );

    CREATE TABLE dishes (
        id INT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(255) NOT NULL,
        description TEXT,
        dining_hall_id INT NOT NULL,
        station_id INT NOT NULL,
        FOREIGN KEY (dining_hall_id) REFERENCES dining_halls(id) ON DELETE CASCADE,
        FOREIGN KEY (station_id) REFERENCES stations(id) ON DELETE CASCADE
    );
   ```

5. **Run the Microservice**

   ```bash
   cd app
   python3 app.py
   ```

## Docker Instructions

1. **Build the Docker Image**

   ```bash
   docker build -t 4153-dish-management-service .
   ```

2. **Run the Docker Container (if connecting to localhost database, set DB_HOST=host.docker.internal)**

   ```bash
   docker run -p 5001:5001 --env-file .env 4153-dish-management-service
   ```
