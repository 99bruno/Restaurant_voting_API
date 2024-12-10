# Restaurant Voting API

This is a backend API for managing restaurant voting, where users can vote for their favorite menus.
The system provides endpoints to create votes, fetch vote statistics, and view the most popular menu for today.

## Table of Contents

- **[Technologies](#technologies)**
- **[Getting Started](#getting-started)**
- **[Endpoint](#endpoints)**
- **[Contributing](#contributing)**
- **[License](#license)**
- **[Contact](#contact)**

## Technologies

- **[Django](https://www.djangoproject.com/):**  A high-level Python web framework that encourages rapid development and clean, pragmatic design.
- **[PostgreSQL](https://www.postgresql.org/):**  An open-source relational database system known for its robustness and reliability.
- **[Docker](https://www.docker.com/):**  A platform for developing, shipping, and running applications in containers.


## Getting Started

1. Clone the repository:
    ```sh
    git clone https://github.com/99bruno/restaurant_voting_api.git
    cd restaurant_voting_api
    ```

2. Download Docker and Docker Compose:
    ```sh
    sudo apt-get update && sudo apt-get install docker.io docker-compose
    ```

3. Run the Docker container for application:
    ```sh
    docker-compose up --build
    ```

4Access the application at `http://127.0.0.1:8000/`.


## Endpoints:

1. Authentication
   - `POST /authentication/register/` - Register a new user
   - `POST /authentication/register/admin/` - Register a new admin user (only for superusers)
   - `POST /authentication/token/` - Get a JWT token
   - `POST /authentication/token/refresh/` - Refresh a JWT token

2. Restaurants
   - `GET /restaurants/` - List all restaurants
   - `POST /restaurants/` - Create a new restaurant (only for superusers)
   - `GET /restaurants/{restaurant_id}/menu/` - Get the menu of a restaurant
   - `POST /restaurants/{restaurant_id}/menu/` - Create a new menu for a restaurant (only for superusers or restaurant owners)
   - `GET /restaurants/menu` - Get the menu of all restaurants for today

3. Voting
   - `GET /voting/` - Get the statistics of the votes for the day
   - `POST /voting/` - Create a new vote for a menu
   - `GET /voting/today/` - Get today menu

## Managing Database Connections

### PostgreSQL

The PostgreSQL connection settings are configured in the `.env` file. Ensure the following environment variables are set:

```dotenv
POSTGRES_USER=postgres
POSTGRES_PASSWORD=123456789
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_DB=postgres
```

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.

## License

This project is licensed under the MIT License. See the **[LICENSE](LICENSE)** file for more details.

## Contact

For any inquiries or feedback, please contact **[99bruno](https://github.com/99bruno)**.
