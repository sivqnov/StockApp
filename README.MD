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
- shop (FK to Shop)
- manufacture (FK to Manufacture)
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

Manufacture:
- id
- name
- about
- photo

CatalogItem:
- id
- manufacturer (FK to Manufacture)
- name
- about
- code (13 digits)
- photo
- date of manufacture
- expiration date
- price


