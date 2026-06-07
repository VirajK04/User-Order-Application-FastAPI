# User-Order Management Backend

A high-performance, asynchronous FastAPI backend application designed for managing users and their orders. The application uses PostgreSQL as its database and features connection pooling and query optimization (via eager loading with `selectinload`) to handle high-throughput loads.

---

## Tech Stack

- **Backend Framework:** [FastAPI](https://fastapi.tiangolo.com/) (Asynchronous ASGI framework)
- **Database ORM:** [SQLAlchemy](https://www.sqlalchemy.org/) (Async session management)
- **Database Driver:** [asyncpg](https://github.com/MagicStack/asyncpg) (Fast, async PostgreSQL client library)
- **Database:** [PostgreSQL](https://www.postgresql.org/) (Containerized with Docker)
- **ASGI Server:** [Uvicorn](https://www.uvicorn.org/)
- **Load Testing:** [Locust](https://locust.io/)

---

## API Reference

The server runs by default on `http://127.0.0.1:8001`. Interactive API documentation is available at `/docs` (Swagger UI) or `/redoc` (ReDoc).

### General Endpoints

* **GET `/`**: Quick health check/welcome message.
  - **Response:** `{"message": "API is online and running asynchronously!"}`

### User Endpoints (`/api/users`)

| Method | Endpoint | Request Body | Description |
| :--- | :--- | :--- | :--- |
| **POST** | `/api/users/` | `{"name": "string", "email": "string"}` | Create a new user. Returns created user object. |
| **GET** | `/api/users/{user_id}` | *None* | Retrieve a specific user by ID. |
| **GET** | `/api/users/{user_id}/orders` | *None* | Retrieve a user and all their associated orders. Optimized using eager loading to prevent N+1 query issues. |
| **PUT** | `/api/users/{user_id}` | `{"name": "string", "email": "string"}` (optional fields) | Update a user's details. |
| **DELETE** | `/api/users/{user_id}` | *None* | Delete a user and cascade delete their orders. |

### Order Endpoints (`/api/orders`)

| Method | Endpoint | Request Body | Description |
| :--- | :--- | :--- | :--- |
| **POST** | `/api/orders/` | `{"user_id": int, "product_name": "string", "quantity": int}` | Create a new order for a user. |
| **GET** | `/api/orders/{order_id}` | *None* | Retrieve details of a specific order. |
| **PUT** | `/api/orders/{order_id}` | `{"user_id": int, "product_name": "string", "quantity": int}` (optional fields) | Update order details. |
| **DELETE** | `/api/orders/{order_id}` | *None* | Delete a specific order. |

---

## Setup & Running the Project

### Prerequisites

Ensure you have the following installed:
- Python 3.10 or higher
- Docker & Docker Compose (for running PostgreSQL)

### 1. Start the Database
The project includes a `docker-compose.yml` to spawn a PostgreSQL 15 instance. Run the following command in the root directory:

```bash
docker compose up -d
```

This spins up a container named `fastapi_postgres` with:
- **Port:** `5432`
- **Database Name:** `fastapi`
- **User:** `postgres`
- **Password:** `password`

### 2. Configure Python Virtual Environment & Install Dependencies

Create and activate a virtual environment:

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

Install the required packages:
```bash
pip install -r requirements.txt
```

### 3. Run the FastAPI Application

Start the server using `uvicorn`:

```bash
uvicorn app.main:app --host 127.0.0.1 --port 8001 --reload
```

- `--reload` enables auto-reloading upon file changes (useful during development).
- The database tables will be auto-created on start due to the FastAPI lifecycle setup in `app/main.py`.

---

## Load Testing using Locust

This project has a Locust configuration file (`locustfile.py`) designed to simulate user traffic and stress test the backend endpoints.

### What the Load Test Simulates

The virtual users (spawned by Locust) perform the following tasks:
1. **Setup (`on_start`):** Each user registers a unique account when they spawn so they have a valid `user_id` for order transactions.
2. **Place Orders (`create_order` - weight 3):** Simulates placing an order for products (e.g., `Product-45` with a quantity from 1 to 5).
3. **Fetch User Dashboard (`fetch_user_dashboard` - weight 4):** Simulates a user retrieving their profile containing all their orders. This is the critical query that validates the SQLAlchemy `selectinload` optimization.
4. **New Signups (`create_new_user` - weight 1):** Simulates new users registering accounts.

### How to Run the Load Test

1. Ensure the FastAPI application is running (e.g., on `http://127.0.0.1:8001`).
2. Make sure your virtual environment is active and run:

   ```bash
   locust
   ```

   *Locust automatically picks up `locustfile.py` in the root folder.*

3. Open your web browser and navigate to:
   [http://localhost:8089](http://localhost:8089)

4. Configure the Locust Swarm parameters:
   - **Number of users:** E.g., `100` (Number of concurrent users to simulate)
   - **Spawn rate:** E.g., `10` (Users spawned per second)
   - **Host:** `http://127.0.0.1:8001` (The address of your FastAPI server)

5. Click **"Start swarming"** to begin the load test. You can monitor request statistics, charts, response times, and failure rates live in the Locust dashboard.

---

## Load Test Results

Below are the results from the load test conducted with **100 concurrent users** and a **10 users/sec spawn rate**. The application demonstrated excellent performance with **0% failure rate** and an average throughput of **~55.5 requests/second (RPS)**.

### Request Statistics

| Request Type | Endpoint / Name | # Requests | # Fails | Average (ms) | Min (ms) | Max (ms) | Average Size (bytes) | RPS | Failures/s |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **POST** | `/api/orders/` | 1,684 | 0 | 271.10 | 8 | 2,301 | 106.44 | 19.93 | 0 |
| **POST** | `/api/users/` | 654 | 0 | 286.89 | 9 | 2,512 | 105.99 | 7.74 | 0 |
| **GET** | `/api/users/[id]/orders` | 2,353 | 0 | 208.66 | 6 | 2,243 | 992.85 | 27.84 | 0 |
| **Aggregated** | **Total** | **4,691** | **0** | **241.98** | **6** | **2,512** | **551.00** | **55.51** | **0** |

### Task Distribution Ratio

- **fetchUserDashboard:** 50.0% (Weight: 4)
- **createOrder:** 37.5% (Weight: 3)
- **createNewUser:** 12.5% (Weight: 1)

### Performance Charts

#### Total Requests per Second & Response Times
![Total Requests per Second & Response Times](load%20test%20results/Screenshot%202026-06-07%20170913.png)

#### Response Times & User Spawning Timeline
![Response Times & User Spawning Timeline](load%20test%20results/Screenshot%202026-06-07%20170712.png)

#### Final Ratio
![Final Ratio](load%20test%20results/Screenshot%202026-06-07%20170725.png)

#### Detailed Request Statistics
![Request Statistics Table](load%20test%20results/Screenshot%202026-06-07%20170736.png)

