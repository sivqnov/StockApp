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

# Applications

Members:
- login
- register
- reset_password
- reset_password_done
- reset_password_confirm
- reset_password_complete
- profile
- edit_user
- change_password

Main:
- main
- about
- contacts
- search

Shop:
- shop
- edit_shop
- delete_shop
- products
- product
- add_product
- edit_product
- delete_product

Manufacture:
- manufacture
- edit_manufacture
- delete_manufacture
- catalog
- catalog_item
- add_catalog_item
- edit_catalog_item
- delete_catalog_item