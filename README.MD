# Stock inventory control system


# Database
User:
- id
- username
- first_name
- last_name
- email
- password

Profile:
- id
- user (FK to User)
- photo
- about
- shop (FK to shop)
- role

Shop:
- id
- name
- about

Product:
- id
- product (FK to CatalogItem)
- stock (FK to shop)
- amount (>= 0)
- price

Manufacturer:
- id
- name
- about

CatalogItem:
- id
- manufacturer (FK to Manufacturer)
- name
- about
- code (13 digits)
- photo
- date of manufacture
- expiration date
- price


