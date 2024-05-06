# python3 -m venv env
# source env/bin/activate

pip install -r req.txt

python manage.py makemigrations
python manage.py migrate

# comment out if using on remote server
# python3 manage.py runserver
gunicorn --bind 0.0.0.0:8000 backend.wsgi:application