Here's the list of required items you need to install before running loan-app
1. python3 v3.11.3
2. poetry
3. virtualenv

Now for running loan app, I'm assuming that your present working directory is loan-app directory(parent directory). From here on, we need to run these following commands:
1. virtualenv .venv
2. poetry install
3. cd /loan_app
4. poetry run flask run 

After this, you will be able to access loan-app on http://127.0.0.1:5000

PLEASE NOTE:

I've already created an admin user with credentials {"name" : "admin", "password" : "password"}. You won't be able to create another admin user apart from this. Please use these credentials to view or approve loans.
