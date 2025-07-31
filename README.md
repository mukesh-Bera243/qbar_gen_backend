# Virtualenv modules installation (Windows based systems) (One time installation)
pip install virtualenv

python -m virtualenv .qbar

# to activate virtualenv
.qbar/Scripts/activate

# Install modules
pip install -r requirements.txt

# Create tables, user and collect statics
python manage.py makemigrations qbargen
python manage.py migrate

# Create super user and masters
python manage.py createsuperuser

# To run the server
python manage.py runserver   


