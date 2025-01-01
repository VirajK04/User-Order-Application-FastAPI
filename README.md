
# User-Order Management Backend

This is a User-Order Management Backend built using FastAPI.
This project uses PostgreSQL as Backend.

Get your database link and add it.

You can check `docs` at `/docs` endpoint.
## API Reference

#### Get a user

```http
  GET /users/{user_id}
```

| Parameter | Return Type     | Description                |Request Body |
| :-------- | :------- | :------------------------- |:------ |
| `user_id` | `User Object` | Get a User |`None` |

#### Update User

```http
  PUT /users/{user_id}
```

| Parameter | Return Type     | Description                |Request Body |
| :-------- | :------- | :------------------------- |:------ |
| `user_id` | `User Object` | Update a user |name, email |

#### Add User

```http
  POST /users/
```

| Parameter | Return Type     | Description                |Request Body |
| :-------- | :------- | :------------------------- |:------ |
| `user_id` | `User Object` | Add new user |`None` |

#### Delete User

```http
  DELETE /users/{user_id}
```

| Parameter | Return Type     | Description                |Request Body |
| :-------- | :------- | :------------------------- |:------ |
| `user_id` | `string` | Delete a user |name, email |

#### Get a Order

```http
  GET /orders/{order_id}
```

| Parameter | Return Type     | Description                |Request Body |
| :-------- | :------- | :------------------------- |:------ |
| `user_id` | `Order Object` | Get order |`None` |

#### Update Order

```http
  PUT /orders/{order_id}
```

| Parameter | Return Type     | Description                |Request Body |
| :-------- | :------- | :------------------------- |:------ |
| `user_id` | `Order Object | Update an order |user_id,quantity,product_name |

#### Add Order

```http
  POST /orders/
```

| Parameter | Return Type     | Description                |Request Body |
| :-------- | :------- | :------------------------- |:------ |
| `user_id` | `Order Object | Add an order |user_id,quantity,product_name |

#### Delete Order

```http
  DELETE /orders/{order_id}
```

| Parameter | Return Type     | Description                |Request Body |
| :-------- | :------- | :------------------------- |:------ |
| `user_id` | `string` | Delete order |`None` |



## Run Locally

Install dependencies

```bash
  pip install -r requirements.txt
```

Start the server

```bash
  uvicorn app.main:app --host 127.0.0.1 --port 8001 --reload
```


## Tech Stack


**Backend App:** FastAPI, SQLAlchemy, AsyncPG, Postgres, Uvicorn

