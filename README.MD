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
- bio
- shops (MTM to Shop) i can start managing shop via shop code
- manufactures (MTM to Manufacture) i can start managing manufacture via manufacture code

Shop:
- id
- name
- bio
- photo
- code (random 16 symbols)

Product:
- id
- product (FK to CatalogItem)
- stock (FK to shop)
- amount (>= 0)
- price

Manufacture:
- id
- name
- bio
- photo
- code (random 16 symbols)

CatalogItem:
- id
- manufacturer (FK to Manufacture)
- name
- bio
- code (13 digits)
- photo
- date of manufacture
- expiration date
- price

# Applications

Members:
- login (+)
- register (+)
- reset_password (+)
- reset_password_done (+)
- reset_password_confirm (+)
- reset_password_complete (+)
- profile (+)
- edit_user (+)
- change_password (+)

Main:
- main (+)
- about
- contacts
- search

Shop:
- all
- view_shop
- add_shop (+)
- edit_shop (+)
- delete_shop (+)
- leave_shop (+)
- join_shop (+)
- view_product
- add_product
- edit_product
- delete_product

Manufacture:
- all (+)
- add_manufacture (+)
- edit_manufacture (+)
- delete_manufacture (+)
- leave_manufacture (+)
- join_manufacture (+)
- view_manufacture (+)
- view_catalog_item (+)
- add_catalog_item (+)
- edit_catalog_item (+)
- delete_catalog_item (+)
- transfer_item
