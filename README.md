# otus-python-qa
Homework for online course Python QA Engineer from OTUS
https://otus.ru/lessons/avtomatizaciya-web-testirovaniya/


### Preparation
To run tests for **opencart**:
1. Add `auth.py` in the `pages` directory with the following content structure:

```
class Users:
    ADMIN = {"username": "", "password": ""}
    ADMIN_USER2 = {"username": "", "password": ""}  # need to create
    NON_ADMIN = {"username": "", "password": ""}  # need to create
    NON_EXISTING_USER = {"username": "foofoo", "password": "barbar"}
```
2. Fill in credentials in this file, where:
   1. `ADMIN` is a default '**opencart**' admin (get from: https://gist.github.com/konflic/ecd93a4bf7666d97d62bcecbe2713e55)
   2. `ADMIN_USER2` and `NON_ADMIN` do not exist by default. You need to create them manually in `http://OPENCART_BASE_URL/admin` (with admin and non-admin rights respectively)
