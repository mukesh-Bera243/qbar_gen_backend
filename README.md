
# Create tables, user and collect statics
python manage.py makemigrations qbargen
python manage.py migrate

# Create super user and masters
python manage.py createsuperuser

# Activate Virtualenv
qbar\scripts\activate  

# To run the server
python manage.py runserver   


