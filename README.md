# Pokemon530
![django workflow](https://github.com/ZhihongPang/Pokemon530/actions/workflows/django.yml/badge.svg)
<br />
[Heroku Hosting Here (Coming Soon)](#)
# Running the Django application
## System Requirements
* Python version 3.9+. You can check if you have this installed with `python -V`
* Pip or pip3. You can check with `pip -V`
## Starting the app
1. Set up your venv in the project directory (optional)
2. Navigate to the project directory `Pokemon530`
3. Create a `.env` file here as this project requires a Django SECRET_KEY and a GOOGLE_API_KEY to properly function
4. For your `.env` file, open a text editor and format it to look like this
```bash
# Pokemon530/Pokemon530/.env
SECRET_KEY=[YOUR_KEY]
GOOGLE_API_KEY=[YOUR_KEY]
```
5. Run the following commands
```bash
$ cd Pokemon530
$ pip install -r requirements.txt 	# Download all python dependencies for the project
$ python manage.py migrate          # Migrate models to your local database
$ python manage.py runserver 		# Start up the project using Django
```
**NOTE:**
* You don't need to run `python manage.py migrate` if you've migrated previously
* The app should be running locally in port [:8000](http://127.0.0.1:8000/) by default
* If not, check to make sure that port 8000 is open on your localhost
* You will need to add at least one animal and one robot in order for the battle system to work
## Testing
All tests are stored in `PseudomonGo/tests.py` and in `PseudomonGo/tests`
<br />
To run the test suite:
```bash
$ python manage.py test                     # runs the main tests.py
$ python manage.py test PseudomonGo/tests   # runs unit tests in /tests
```
## For Developers
Most API access is restricted to authenticated users for security reasons. You **may** need to create an [admin user](https://docs.djangoproject.com/en/1.8/intro/tutorial02/#creating-an-admin-user) to access them
<br />
Head over to [/admin](http://127.0.0.1:8000/admin/) and login. You should be able to access most API routes at [/api](http://127.0.0.1:8000/api/) if done correctly. Some APIs are not listed there so check out `PseudomonGo/urls.py`
## ToDo
- [ ] For prod releases -- Set `DEBUG = False` to disable browsable API!
