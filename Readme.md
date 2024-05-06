

# Vendor System

Project is live on [render](https://vendors-backend.onrender.com)

**Setup Instruction**


```bash
# install packages
pip install -r req.txt
```
```bash
# setup local environment
python3 -m venv env
```
```bash
# setup models and db
# this project uses sqlite
python3 manage.py makemigrations
python3 manage.py migrate
```

```bash
# run app
python3 manage.py runserver
```


## Project Structure

<video width="320" height="240" controls>
  <source src="sample.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>


What is provided in the project

- User
  - Create a new user
  - Get all user
  - Delete a user
  - Get user by id

- Vendor
  - Create a new vendor
  - Get all vendor
  - Get vendor by id
  
- Purchase Order
  - Create a new purchase order
  - Get all purchase order
  - Get purchase order by vendor
  - Get purchase order by purchase order id
  - Acknowledge purchase order

- Performance matrices
  > Automatic calculation of these metrics and update in the database upon creation and update of purchase order
  - On-Time Delivery Rate
  - Fulfillment Rate
  - Quality Rating Average
  - Average Response Time

- Authentication
  - Obtain new access token
  - Obtain new refresh token
  - Verify token



## API Documentation



**To create a new user** <br>

```
POST -> /api/user/

body -> 
  email
  password
  first_name
  last_name
```

**To optain new access token** <br>

```
GET -> /api/token/

body -> 
  email
  password
```

**To create a new vendor** <br>

```
POST -> /api/vendor/

body -> 
  name
  address
  phone
```

**To create a new purchase order** <br>

```
POST -> /api/purchase_order/

body -> 
  vendor
  product
  quantity
  price
```

**To get all purchase order** <br>

```
GET -> /api/purchase_order/
```

**To get all vendor** <br>

```
GET -> /api/vendors/
```

**To get vendor by id** <br>

```
GET -> /api/vendors/<int:vendor_id>/
```

**To get all user** <br>

```
GET -> /api/user/
```

**To get purchase order by vendor** <br>

```
GET -> /api/purchase_order/vendor/<int:vendor_id>/
```

**To get purchase order by purchase order id** <br>

```
GET -> /api/purchase_order/user/<int:po_id>/
```

**To acknowledge purchase order** <br>

```
GET -> /api/purchase_order/<int:po_id>/acknowledge
```

- Django concepts in the project
  - The project is designed to be scalable and fast
  - The project uses Django ORM for database operations
  - The project uses Django Rest Framework for API creation
  - The project uses Django Rest Framework Simple JWT for token authentication
  - The project uses Django Rest Framework Pagination for pagination
  - The project uses Django Rest Framework Filtering for filtering
  - The project uses Django Rest Framework Serializers for serialization
  - The project uses Django Rest Framework Response for response
  - The project uses Django Rest Framework Status for status
  - The project uses Django Rest Framework APIView for APIView
  - The project uses Django Rest Framework mixins for mixins
  - The project uses Django Rest Framework decorators for decorators
  - The project uses Django Rest Framework exceptions for exceptions
