

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

- project model have 3 Entities

  - User
    - For separating authentication and user creation logic from vendor
  - Vendor
    - A user can have create multiple vendor accounts for better branching
  - Purchase Order
    - A vendor can have multiple purchase order



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