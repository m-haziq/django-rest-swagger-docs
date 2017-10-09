# Comprehensive approach to django-rest-swagger 2 using both FBV and CBV

For making a DRF project we ll follow: http://www.django-rest-framework.org/tutorial/quickstart/

Start by making the project as in DRF docs:
`mkdir django-rest-swagger-docs` 

`cd django-rest-swagger-docs`

Make Virtual Environment with python3 and activate it:
`virtualenv env --python=python3`

`source ./env/bin/activate`

`pip install django`

`pip install djangorestframework`

Make project named 'demo' in current directory:

`django-admin startproject demo .`

`cd demo`

Make two apps inside 'demo' project, 'cbv-demo' for class based views and fbv-demo for function based view:

`django-admin startapp cbv_demo` 

`django-admin startapp fbv_demo`

Get back to main project directory:

`cd ..`

Now sync database and create database user:

`python manage.py migrate`
`python manage.py createsuperuser`
