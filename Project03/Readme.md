# CS 1XA3 Project03 - <MyMacId>
## Usage
Install conda enivornment with ...
...
Run locally with
python manage.py runserver localhost:8000
Run on mac1xa3.ca with
python manage.py runserver localhost:100192
...
Log in with TestUser, password SomePassword
...
## Objective 01
Description:
- this feature is displayed in something.djhtml which is rendered by
some_view
- it makes a POST Request to from something.js to /e/macid/something_post
which is handled by someting_post_view
Exceptions:
- If the /e/macid/something_post is called without arguments is redirects
to login.djhtml
## Objective 02
