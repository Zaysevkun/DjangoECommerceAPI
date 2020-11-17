# DjangoECommerceAPI

API of a simple online shop

## Requirements
You need installed:
1. Redis
2. wkhtmltopdf

## Project setup 

1. `git clone https://github.com/Zaysevkun/DjangoECommerceAPI`
2.  `create postgres db`
3. `cd DjangoECommerceAPI`
4. `pip install -r requirements.txt`
5. Add __.env__ file
##### EXAMPLE:
```
SECRET_KEY=qwerty123
DATABASE_URL=postgres://your_db_user_name:user_password@127.0.0.1:5432/your_db_name
ALLOWED_HOSTS=*
DEBUG=0
```
6. `python manage.py migrate`
7. `python manage.py collectstatic`
8. `python manage.py runserver 0.0.0.0:8000`

## END POINTS

| *URL* | *Method*|*Description*|
|-------|---------|-------------|
| `api/token-auth/` | `POST` | Token authentication endpoint|

POST request body:
```
{"Token"}
```
| *URL* | *Method*|*Description*|
|-------|---------|-------------|
| `api/products/` | `GET,POST,PUT,DELETE` | endpoint for manipulating Products model|

GET response body:
```
{"pk", "vendor_code", "name", "retail_price", "purchase_price"}
```
POST request body:
```
{"vendor_code", "name", "retail_price", "purchase_price"}
```

| *URL* | *Method*|*Description*|
|-------|---------|-------------|
| `api/orders/` | `GET,POST,DELETE` | endpoint for manipulating Orders model(order only accessible by owner user or moderator)|

GET response body:
```
{"pk", "user", "products", "price"}
```
POST request body:
```
{"user", "products"}
```

| *URL* | *Method*|*Description*|
|-------|---------|-------------|
| `api/order_products/` | `POST` | endpoint for adding products to orders|

POST request body:
```
{"product", "order", "quantity"}
```
POST request body:
```
{"product", "order", "quantity", "sum"}
```

| *URL* | *Method*|*Description*|
|-------|---------|-------------|
| `api/file_upload/` | `PUT` | endpoint for adding products to orders|

PUT response:
status code: 204

| *URL* | *Method*|*Description*|
|-------|---------|-------------|
| `api/checkout_pdf/` | `POST` | endpoint for adding products to orders|

POST request body:
status code: 200
