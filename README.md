# Pokemon530
You need python 3.9+ to build this Django Project.

Here are all the dependencies required for this project to work:
-----------------------------------------------------------------
* asgiref==3.5.0
* certifi==2021.10.8
* charset-normalizer==2.0.12
* Django==4.0.3
* django-cors-headers==3.11.0
* djangorestframework==3.13.1
* idna==3.3
* python-decouple==3.6
* pytz==2022.1
* requests==2.27.1
* sqlparse==0.4.2
* tzdata==2022.1
* urllib3==1.26.9

# Running the Django application
## Requirements
* Make sure your system is running Python version 3.9+. You can check with `$ python -V`
* Make sure you have pip or pip3 in your system. You can check with `$ pip -V`
## Starting the app
* Run these commands on either your IDE or terminal
```bash
$ pip install -r requirements.txt
$ python manage.py runserver
```
* 1st command is to download all python dependencies for the project
* 2nd command is to start up the project using the Django framework
* Note that you may need to run `$ python manage.py migrate` if you haven't migrated any of the models to your local SQLite DB
* The app should be running in port :8000 by default
* IMPORTANT: If your app is still not running, you will need to store a SECRET_KEY in an env file for Django to work properly. See [here](https://docs.gitguardian.com/secrets-detection/detectors/specifics/django_secret_key) for more info.
## Testing
* All tests are stored in PseudomonGo/tests.py
* To run the test suite:
```bash
$ python managge.py test
```