# 4153-dish-management-service
This is a Flask-based microservice that connects to a MySQL database and provides RESTful endpoints for creating, retrieving, updating, and deleting dish records.

## REST Endpoints

- **POST /dishes**: Add a new dish
- **GET /dishes**: Retrieve a list of dishes (with optional filtering by name and category)
- **GET /dishes/{id}**: Retrieve detailed information about a specific dish
- **PUT /dishes/{id}**: Update details of an existing dish
- **DELETE /dishes/{id}**: Delete a dish

## Prerequisites

- Python 3.10.1
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
    DB_HOST=your-database-host
    DB_USER=your-database-username
    DB_PASSWORD=your-database-password
    DB_NAME=your-database-name
    ```

4. **Create Database and Table**

   Ensure that your MySQL database has a `dishes` table:
    ```sql
    CREATE TABLE dishes (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        description TEXT,
        category VARCHAR(255),
        dietary_info VARCHAR(255)
    );
    ```

5. **Run the Microservice**
    ```bash
    python3 app.py
    ```
