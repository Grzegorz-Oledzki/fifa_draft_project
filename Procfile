web: gunicorn fifa_draft.wsgi --log-file -
heroku ps:scale web=1
python manage.py collectstatic --noinput
manage.py migrate
