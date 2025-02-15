# EventAPI
# 1) Create a Django project and app
Create the project using this command : django-admin startproject EventAPI
and change the directory EventAPI and create app inside the project : python manage.py startapp myapp

# 2) Create a PostgreSQL database manually
here, first of all create a postgres database "events".

# 3) Update settings.py
    -In INSTALLED_APPS, add application name(here myapp),rest_framework, rest_framework_simplejwt (for jwt token)
    -we need to configure the database name, user,password,ip and port.
    -add this on sttings for custom user: AUTH_USER_MODEL = 'myapp.User'
    -For jwt token: add REST_FRAMEWORK and SIMPLE_JWT settings and change ACCESS_TOKEN_LIFETIME as per requirement.
    
# 4) Create models in models.py
        Create models in models.py and run below command to create table in postgres database:
    -python manage.py makemigrations
    -python manage.py migrate

# 5) Create serializer in serializers.py
        Create serializers.py in myapp (application) and create serializer class to convert queryset to json.

# 6) Create class in serializers.py
        Create classbased views for user, add events and ticket purchase

# 7) Create endpoints in urls.py

# 8) Start the Server
        Run python manage.py runserver to start the project and test.

# 9) Testing in Postman
    1-User Registration
        Endpoint: POST /api/register/
        Body (JSON):{
            "username": "admin",
            "password": "admin",
            "role": "admin"
        }

        -Get JWT Token
        Endpoint: POST /api/token/
        Body (JSON):{
            "username": "admin",
            "password": "admin"
        }

    2-Create an Event (Admin Only)
        Endpoint: POST /api/events/
        Body (JSON):{
            "name": "Event1",
            "date": "2025-02-15",
            "total_tickets": 100
        }

        Use the Access Token in Headers(Admin token):
        -Authorization: Bearer your_access_token

    3- Purchase Ticket (User Only)
        Endpoint: POST /api/events/1/purchase/
        Body (JSON):{"quantity": 2}

        Use the Access Token in Headers(User token):
        -Authorization: Bearer your_access_token


