# PPTS: Game Points Table Generation System (PUBG Specific, Works on similar)
Rough Build, Some Feature May be unstable.

## Installation
1. Clone the repository 
2. Install requirements `pip install -r requirements.txt`
2. Change values in settings.py as needed
3. For debug mode set environment variable `DJANGO_ENV=1` Otherwise you will have to save `SECRET_KEY` in environment variable
4. Migrate `python manage.py migrate`
5. Create Cache Table `python manage.py createcachetable`
6. Create Super User `python manage.py createsuperuser`
7. Create FixtureDump `python manage.py dumpdata > fixture.json`
7. Load FixtureDump `python manage.py loaddata fixture.json`
8. Run `python manage.py testserver fixture fixture.json`
8. Create Normal User wrom admin panel
9. Give Staff Permission
10. Grant all Permissons in entities of site
11. Explore the admin panel to know how to enter the data.

---
Open For contribution.
---
