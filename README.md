Dependencies: Django, pillow, sorl-thumbnail

How to install:
1. Clone or download this rep
2. In main folder create your virtual env, using virtualenv myvenv (if you don't have this package, install using: pip install virtualenv)
3. activate this virtual env:

  Windows:
    myvenv\Scripts\activate
    
  Linux:
    source myvenv/bin/activate
    
4. Install all dependecies, just put this command: pip install django pillow sorl-thumbnail
5. create database for your project - python manage.py migrate
6. Because sorl-thumbnail sometimes didn't create tabs in db, you must create this yourself: python manage.py makemigrations thumbnail
7. Run again - python manage.py migrate
8. create your superuser - python manage.py createsuperuser
9. Excelent! Hard work is done. Run your server - python manage.py runserver, and open any web browser you like.
10. Go to 127.0.0.1:8000 in your browser, and login using your superuser account.
11. Open 127.0.0.1:8000/admin and search here for "Users", and fill on bottom page for your superuser (Select your nickname, enter date of birth, and choose any image you like)
12. DONE, you're great.


