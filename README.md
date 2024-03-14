# Nexu Backend Coding Exercise

## Running

The project was built using Python 3.12 and virtualenv

Steps:
 1. Create virtualenv with python -m virtualenv -p "Path to your Python interpreter python.exe" venv
 2. Activate virtual environment with (Windows): .\venv\Scripts\activate
 3. Install dependencies: pip install -r requirements.txt
 4. Add .env, check .env_example:
 5. Create db structure: python manage.py migrate
 6. Create superuser for Django admin: python manage.py createsuperuser
 7. Create initial data from models.json: python manage.py createinitialdata
 8. Run server: python manage.py runserver
##

## Test
To run test cases use: python manage.py test

## URL
Test server: 


