# Library Service Project

API service for tracking books, borrowings and users written on DRF

## Installation
Python3 should be installed

#### Download the code
```angular2html
git clone https://github.com/isikach/library-management-system.git
cd library-service-project
```

#### Set Up for Unix, macOS
```angular2html
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Set Up for Windows
```angular2html
python3 -m venv venv
.\env\Scripts\activate
pip3 install -r requirements.txt
```

#### Set Up secret key and database for Windows
```angular2html
set SECRET_KEY=<your secret key>
  
python3 manage.py makemigrations
python3 manage.py migrate
```

#### Set Up secret key and database for Unix, macOS
```angular2html
export SECRET_KEY=<your secret key>
  
python3 manage.py makemigrations
python3 manage.py migrate
```

#### Start the app
```angular2html
python3 manage.py runserver
```

## Features

* JWT authentication
* Admin panel /admin/
* Documentation is located at /api/schema/swagger-ui/
* Managing books, borrowings and users
* Adding books by library staff
* Creating borrowings and filtering by user and status
* User registration

## Getting access
* create user via /users/register/
* get access token /users/token/
