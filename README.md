# Comprehensive approach to django-rest-swagger 2 using both FBV and CBV
![main-demo](https://i.imgur.com/GgHxcHt.gif)

This project provides a beginner's guide to django rest swagger 2 with
function based views as well as class based views. It provides  building the 
project from scratch. For those who want to integrate Django Rest Swagger into
an existing project, head straight to: [Integrating Django Rest Swagger](https://github.com/m-haziq/django-rest-swagger-docs#integrating-django-rest-swagger) .

> Read this article on [Medium](https://medium.com/@m_haziq/comprehensive-approach-to-django-rest-swagger-2-583e91a4c833) if that is more convenient for you.

## Getting Started
Before we start, we need this to be installed:
- [Python3](https://www.python.org/downloads/)

## Project Setup
Start by making the project as in [DRF official docs](http://www.django-rest-framework.org/tutorial/quickstart/):
```
mkdir django-rest-swagger-docs
cd django-rest-swagger-docs
```
Make virtual environment with python3 and activate it:
```
virtualenv env --python=python3
source ./env/bin/activate
```
Install Django and DjangoRestFramework:
```
pip install django
pip install djangorestframework==3.5.3
```
**Note: Installing the correct version of DRF is very important.**

Make project named **demo** in current directory and navigate inside it:
```
django-admin startproject demo .
cd demo
```
Make two apps **cbv-demo** (for class based views) and **fbv-demo** (for function based view) inside **demo** project,:
```
django-admin startapp cbv_demo
django-admin startapp fbv_demo
```
Get back to main directory:
```
cd ..
```

Now sync database and create database user:
```
python manage.py migrate
python manage.py createsuperuser
```
##### Making class based views:

Make a simple model at `demo/cbv_demo/models.py` with code below:

```cython
from django.db import models


class Contact(models.Model):
    name = models.CharField(max_length=22)
    phone = models.CharField(max_length=22)
    address = models.CharField(max_length=44)
```

Make a simple serializer at `demo/cbv_demo/serializers.py` with code below:

```cython
from rest_framework import serializers
from .models import Contact


class ContactDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'
```

Make a simple view at `demo/cbv_demo/views.py` with code below:

```cython
from demo.cbv_demo.serializers import ContactDataSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Contact
from rest_framework import status , generics


class ContactData(generics.GenericAPIView):
    serializer_class = ContactDataSerializer
    permission_classes = [IsAuthenticated,]

    def get(self, request, format=None):
        contacts = Contact.objects.all()
        serializer = ContactDataSerializer(contacts, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ContactDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

Add urls of this app to `demo/cbv_demo/urls.py` as:

```cython
from django.conf.urls import url
from .views import ContactData


urlpatterns = [
    url(r'^contact', ContactData.as_view(), name='contact'),
]
```

##### Making function based views:

Make a simple model at `demo/fbv_demo/models.py` with code below:

```cython
from django.db import models


class Medical(models.Model):
    name = models.CharField(max_length=22)
    bloodgroup = models.CharField(max_length=22)
    birthmark = models.CharField(max_length=44)
```

Make a simple view at `demo/fbv_demo/views.py` with code below:

```cython
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Medical
from rest_framework import status


@api_view(['POST'])
def save_medical(request):
    name = request.POST.get('name')
    bloodgroup = request.POST.get('bloodgroup')
    birthmark = request.POST.get('birthmark')

    try:
        Medical.objects.create(name= name, bloodgroup = bloodgroup, birthmark = birthmark)
        return Response("Data Saved!", status=status.HTTP_201_CREATED)

    except Exception as ex:
        return Response(ex, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_medical(request):
    return Response(Medical.objects.all().values(), status=status.HTTP_200_OK)
```

Add urls of this app to `demo/fbv_demo/urls.py` as:

```cython
from django.conf.urls import url
from .views import save_medical, get_medical


urlpatterns = [
    url(r'^save_medical', save_medical, name='save_contact'),
    url(r'^get_medical', get_medical, name='get_contact'),
]
```

Add 'rest_framework' and both apps to `demo/settings.py` as:
```cython
INSTALLED_APPS = [
    ...
    'rest_framework',
    'demo.cbv_demo',
    'demo.fbv_demo',
]
```

Now add urls of both apps to `demo/urls.py`:
```cython
from django.conf.urls import url, include


urlpatterns = [
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^cbv/', include('demo.cbv_demo.urls')),
    url(r'^fbv/', include('demo.fbv_demo.urls')),
]
```

Now you have class based views (GET, POST) in `demo/cbv_demo/views.py` and 
two function based views in `demo/fbv_demo/views.py` .

In order to run the it apply migrations 
to make tables in db against models and runserver to test:
```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

## Integrating Django Rest Swagger:

In order to integrate django-rest-swagger,
first install it through pip as:

```
pip install django-rest-swagger==2.1.1
```
**Note: Installing the correct version is very important.(This one works best with djangorestframework==3.5.3)**

Add it into the `demo/settings.py` as:

```cython
INSTALLED_APPS = [
    ...
    'rest_framework_swagger',
]

# Parser classes to help swagger, default ll be JSONParser only.

REST_FRAMEWORK = {
    # Parser classes priority-wise for Swagger
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.JSONParser',
    ],
}

```

### Using `get_swagger_view` the shortcut method:
Make swagger schema view in `demo/urls.py` and assign it a url as :

```cython
from rest_framework_swagger.views import get_swagger_view
schema_view = get_swagger_view(title='Demo Swagger API')


urlpatterns = [
    ...
    url(r'^swagger/', schema_view),
]
```
Your swagger should run at: 
[http://127.0.0.1:8000/swagger/]()

Using shortcut method can let us into following issues:
- No way to document parameters of function based views
- Less customizablity 
- No way to enforce permission classes
- No handy way to exclude swagger view from schema

In order to acheive these functionalities, we ll go for its advance usage.

### Advance Usage:
For finer control and to make swagger more customizable
we write swagger schema view manually and to document parameters 
for function based views, we override SchemaGenerator of `rest_framework`
which is used by `django-rest-swagger` (version 2) to generate documentation.

Create a file `demo/swagger_schema.py` and add following code to it:

```cython
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_swagger import renderers
from rest_framework.schemas import SchemaGenerator
from urllib.parse import urljoin
import yaml
import coreapi


class CustomSchemaGenerator(SchemaGenerator):
    def get_link(self, path, method, view):
        fields = self.get_path_fields(path, method, view)
        yaml_doc = None
        if view and view.__doc__:
            try:
                yaml_doc = yaml.load(view.__doc__)
            except:
                yaml_doc = None

        #Extract schema information from yaml

        if yaml_doc and type(yaml_doc) != str:
            _method_desc = yaml_doc.get('description', '')
            params = yaml_doc.get('parameters', [])

            for i in params:
                _name = i.get('name')
                _desc = i.get('description')
                _required = i.get('required', False)
                _type = i.get('type', 'string')
                _location = i.get('location', 'form')
                field = coreapi.Field(
                    name=_name,
                    location=_location,
                    required=_required,
                    description=_desc,
                    type=_type
                )
                fields.append(field)
        else:

            _method_desc = view.__doc__ if view and view.__doc__ else ''
            fields += self.get_serializer_fields(path, method, view)

        fields += self.get_pagination_fields(path, method, view)
        fields += self.get_filter_fields(path, method, view)

        if fields and any([field.location in ('form', 'body') for field in fields]):
            encoding = self.get_encoding(path, method, view)
        else:
            encoding = None

        if self.url and path.startswith('/'):
            path = path[1:]

        return coreapi.Link(
            url=urljoin(self.url, path),
            action=method.lower(),
            encoding=encoding,
            fields=fields,
            description=_method_desc
        )


class SwaggerSchemaView(APIView):
    exclude_from_schema = True
    permission_classes = [AllowAny]
    renderer_classes = [
        renderers.OpenAPIRenderer,
        renderers.SwaggerUIRenderer
    ]

    def get(self, request):
        generator = CustomSchemaGenerator()
        schema = generator.get_schema(request=request)
        return Response(schema)
```

> **exclude_from_schema = True** removes the swagger view from schema.

> **CustomSchemaGenerator**
 class overrides the default DRF SchemaGenerator so that it first 
checks if the view has `.__doc__` inside it, if available it uses this YAML
to make parameter fields, otherwise it looks for serializers.
So in this way we acheive the functionality of Django Rest Swagger (version 1)
which supported YAML docstrings as well.

> **SwaggerSchemaView**
is the view made for swagger, which calls CustomSchemaGenerator
to create the schema instead of default SchemaGenerator.


Now, You ll need to install yaml as:

```
pip install PyYAML
```

Next change `demo/urls.py` to point swagger url to this SwaggerSchemaView as:

```cython
from .swagger_schema import SwaggerSchemaView


urlpatterns = [
    ...
    url(r'^swagger/', SwaggerSchemaView.as_view()),
]
```

###### Defining parameters in FBV using YAML:

Now add `__doc__` to the function based API by adding YAML
into it, add following YAML to *save_medical* in `demo/fbv_demo/views.py` as:

```cython
@api_view(['POST'])
def save_medical(request):
# ----- YAML below for Swagger -----
"""
description: This API deletes/uninstalls a device.
parameters:
  - name: name
    type: string
    required: true
    location: form
  - name: bloodgroup
    type: string
    required: true
    location: form
  - name: birthmark
    type: string
    required: true
    location: form
"""
...
...
```

> Now *CustomSchemaGenerator* will be able to read this YAML
and create input parameters against it accordingly.


Go to swagger url :
[http://127.0.0.1:8000/swagger/]()


> You will be able to see input parameters fields for 
*save_medical* POST API as well.

#### Customize Swagger UI:

Swagger UI can be customized to some [extent](https://django-rest-swagger.readthedocs.io/en/latest/customization/),
which is sufficient for a normal user, Follow these simple steps:

- Make the file as `demo/templates/rest_framework_swagger/index.html`
and add following code to it:

```html
{% extends "rest_framework_swagger/base.html" %}

{# TO Customizer Swagger UI #}

{% block header %}
    <div id='header' style="background-color: #000000;">
        <div class="swagger-ui-wrap">
            {% load staticfiles %}
            <a id="logo" href="http://swagger.io"><img class="logo__img" alt="swagger" height="30" width="30" src="{% static 'rest_framework_swagger/images/logo_small.png' %}" /><span class="logo__title">swagger</span></a>
            <form id='api_selector'>
                <input id="input_baseUrl" name="baseUrl" type="hidden"/>
                {% if USE_SESSION_AUTH %}
                {% csrf_token %}
                {% if request.user.is_authenticated %}
                <div class="input">
                    {% block user_context_message %}
                    {# Override this block to customize #}
                    Hello, {{ request.user }}
                    {% endblock %}
                </div>
                {% endif %}
                {% block extra_nav %}
                {# Override this block to add more buttons, content to nav bar. #}
                {% endblock %}
                {% endif %}

                {% if USE_SESSION_AUTH %}
                {% if request.user.is_authenticated %}
                <div class='input'><a id="auth" class="header__btn" href="{{ LOGOUT_URL }}?next={{ request.path }}" data-sw-translate>Django Logout</a></div>
                {% else %}
                <div class='input'><a id="auth" class="header__btn" href="{{ LOGIN_URL }}?next={{ request.path }}" data-sw-translate>Django Login</a></div>
                {% endif %}
                {% endif %}
                <div id='auth_container'></div>
            </form>
        </div>
    </div>
{% endblock %}
```

> This will override the tag **{% block header %}** , for the sample we are
just changing the colour of header, rest remains the same.

- Set template directory in `demo/settings.py` as:

```cython
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['demo/templates/'],
        ...
    }
]
```

>You ll be able to see custom BLACK header at http://127.0.0.1:8000/swagger/.

#### Some add-ons that may help:

Django Rest Swagger provide much customization, most of which is explained indepth
in its [Official Doc](https://django-rest-swagger.readthedocs.io/en/latest/) .

Few mostly used customization is explained here for ease. Add SWAGGER_SETTINGS in 
`demo/settings.py` to provide custom settings:

##### Swagger Login methods:

You can login to swagger by using button **Authorize** in the header of swagger UI.

In order to use django superuser **username** and **password** to login use:
```cython
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'basic': {
            'type': 'basic'
        }
    },
}
```

In order to use authentication token to login to swagger use:
```cython
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        "api_key": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header"
          },
    },
}
```

You can use oauth2 for security. Details: [security definitions](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/2.0.md#security-definitions-object) .

###### *DJANGO LOGIN* Button:

You can also use Django Login button to login. It uses django admin panel
for authentication. In order to make it run correctly you must set *LOGIN_URL* 
and *LOGOUT_URL* in swagger settings. For example if you have rest_framework's 
login mechanism, you can set:

```cython
SWAGGER_SETTINGS = {
    'USE_SESSION_AUTH': True,
    'LOGIN_URL': 'rest_framework:login',
    'LOGOUT_URL': 'rest_framework:logout',
}
```

If you want to disable this button just set *USE_SESSION_AUTH* to *False*.

##### VALIDATION_URL:

A schema json is generated against APIs which you may like to get validated by [swagger.io](swagger.io). 
Its value can be set to any local deployment of validator. By default it is set to:
[https://online.swagger.io/validator/](https://online.swagger.io/validator/). Set it to *None* to not validate
your schema. 

```cython
SWAGGER_SETTINGS = {
    ...
    
    'VALIDATOR_URL': None,
}
```

> Additionally you can also validate your schema manually by copying your schema json to 
[https://editor.swagger.io/](https://editor.swagger.io/).

##### Customize format of parameters defined in DOCSTRING:

You can customize YAML parameters, the most important is location
that helps you with passing the data to API in different forms.

- `location: form` , to access data as `request.POST['key']`

- `location: body` , to access data as `request.body` , you may have to
add `JSON_EDITOR: False` in `SWAGGER_SETTINGS` in `demo/settings.py`.

- `location: query` , to access data as `request.GET['key']` 

Other location options include `location: post` and `location: path`



### Common issues and their solution:

Since the release of version 2 of django-rest-swagger, various issues arise
because this version is fundamentally different from previous versions,
i.e. DOCSTRING has been deprecated by DRF and now swagger
uses DRF 's SchemaGenerator to generate schema.

Here are some of the reported issues and their possible solution:

- *The schema generator did not return a schema Document:* All the APIs
of your project may be authentication protected, try removing authentication
from few of them.

- *Input parameters for class based views do not appear:* You might be using
APIView for making class based views. Try using `generics.GenericAPIView` to
make APIs. All the views must have `serializer` or Docstring `__doc__`.

- *Input parameters for function based views do not appear:* You might be using
incompatible versions, try using `djangorestframework==3.5.3` and `django-rest-swagger==2.1.1`.
In order to use other versions you may need to modify `get_link` inside `demo/swagger_schema.py`.

- *TypeError: 'type' object is not iterable:* Try adding your authentication in this
format `@permission_classes((IsAuthenticated, ))`.

- *Invalid block tag: 'static', expected 'endblock'. Did you forget to register or load this tag? :* Try
 adding `{% load staticfiles %}` to the overridden block of swagger UI e.g. add in `demo/templates/rest_framework_swagger/index.html` as:
 
```
{% extends "rest_framework_swagger/base.html" %}
{% block header %}
    <div id='header' style="background-color: #000000;">
        <div class="swagger-ui-wrap">
            {% load staticfiles %}
            ...
            ...
        </div>
    </div>
{% endblock %}
```

- ![swagger-error](https://i.imgur.com/oBfXWVq.png) *schemaValidationMessages	message:"Can't read from file http://0.0.0.0:8000/swagger/?format=openapi* : This error is rendered
because you schema validation is enabled in swagger settings but your server is not accessible from external network(which swagger.io 
tries to access for validation purpose). Try running your server with `python manage.py runserver 0.0.0.0:8000 --insecure` and in your settings.py 
add `ALLOWED_HOSTS = ['*']` . You wont get this error while accessing server from external network now. 

    Success in validation would show: ![swagger-success](https://i.imgur.com/UwuUwIZ.png)

- ![swagger-error](https://i.imgur.com/oBfXWVq.png) *schemaValidationMessages message: "instance type () does not match any allowed primitive* : This error means that your schema json does not validated
by online.swagger.io/validator. You can disable validation by setting `"VALIDATION_URL" : None` in swagger settings or to fix the issue you can validate 
your schema better manually by pasting on [https://editor.swagger.io/](https://editor.swagger.io/).  

    Success in validation would show: ![swagger-success](https://i.imgur.com/UwuUwIZ.png)

## End Note:

This repository is intended to help those who are facing issues
using `django-rest-swagger 2`. If you like this effort, please like and share this with others. 
If you have any suggestions, comment here or approach me on [linkedin](https://www.linkedin.com/in/m-haziq/) , [medium](https://medium.com/@m_haziq/), [twitter](https://twitter.com/contacthaziq) 
or send me an [email](mailto:m_haziq@outlook.com) to discuss in person. 
I would love to hear from you.
