First app
=============================

In this tutorial we create single file application.


Preparing
---------

First of all, create porject folder.

Inside project folder create virtual environment and install `django-modern-rest`:

.. tabs::

    .. tab:: :iconify:`material-icon-theme:uv` uv

        .. code-block:: bash

            uv init
            uv venv
            uv add django-modern-rest

    .. tab:: :iconify:`devicon:poetry` poetry

        .. code-block:: bash

            poetry add django-modern-rest

    .. tab:: :iconify:`devicon:pypi` pip

        .. code-block:: bash

            pip install django-modern-rest

Simple app
----------

Next lets create our `main.py` file with following code.

.. literalinclude:: /examples/expanded/first_app.py
   :language: python
   :linenos:

We leave some comments to exaplain what each part of code do.


Now lets run our app using this command:

.. code-block:: bash

   python main.py runserver

When all goes fine you will see something like this:

.. code-block::

   Watching for file changes with StatReloader
   Performing system checks...

   System check identified no issues (0 silenced).
   March 04, 2026 - 13:26:37
   Django version 6.0.2, using settings None
   Starting development server at http://127.0.0.1:8000/
   Quit the server with CONTROL-C.

   WARNING: This is a development server. Do not use it in a production setting. Use a production WSGI or ASGI server instead.
   For more information on production servers see: https://docs.djangoproject.com/en/6.0/howto/deployment/


Then go to you brower and visit http://localhost:8000/.
You will see `"Hello from Django Modern Rest!"` message.

Congrats! You run your first app with `dmr`.
But its look to much simple and we even don't import `dmr` itself, are we?

Lets modify our code with some verification magic and different routes.


Verification and routing
------------------------

Honestly our previous example do nothing usefull.

Lets expand ourt application a bit and add 2 endpoints: one for set user and one for get all users.
We will not add database or something else and use simple dict instead.

First of all lets add 2 different urls in our urlpatterns. Replace code with the following

.. code-block:: python


   urlpatterns = [
     path('', lambda request: HttpResponse('Hello from Django Modern Rest!')),
     path('/get_users', lambda request: HttpResponse('Get users endpoints')),
     path('/set_user', lambda request: HttpResponse('Set user endpoint')),
   ]

Now you can go to http://localhost:8000/get_users or http://localhost:8000/set_user and see different messages.
But lets add meanful code to our new endpoints.

Lets add  this code to new endpoints

.. code-block:: python

  # add to imports
  import json
  from django.http import HttpResponse, JsonResponse

  DATABASE = {
   "1": "Alex",
   "2": "Sten"
  }


  def get_users(request):
      return HttpResponse(json.dumps(DATABASE), content_type='application/json')

  def set_user(request):
      if request.method != 'POST':
          return HttpResponse('Method not allowed', status=405)

      try:
          data = json.loads(request.body)
          user_id = data.get('id')
          name = data.get('name')

          if not user_id or not name:
              return HttpResponse('Missing id or name', status=400)

          DATABASE[user_id] = name

          return JsonResponse({'status': 'success', 'data': DATABASE})
      except json.JSONDecodeError:
          return HttpResponse('Invalid JSON', status=400)

Now you can test this enpoints. You can get user list with `get_users`.

Test `set_user` with this command:

.. code-block:: bash

  curl -X POST http://localhost:8000/set_user -H "Content-Type: application/json" -d '{"id": "3", "name": "John"}'


Command return answer:

.. code-block::

  {"status": "success", "data": {"1": "Alex", "2": "Sten", "3": "John"}}


Routes, Controllers and Swagger
-------------------------------

.. note::

  In this section we will use routing and controllers. We provide simple explanation of it.
  If you want to know more just go to other sections of documetation (we will link key concepts in example)


Let go further and add dmr to our project.

First of all, lets combine our endpoints to route.

What is route? In simple words route collect all provided url to single entry point. Its usefull to make your code much readable and expanded. (more in Routing)

In our case let move our user endpoints to single user router. Change whole url_patterns to this:

.. code-block:: python

   # add this to import
   from dmr.routing import Router


   user_router = Router(
   [
     path('get_users', get_users),
     path('set_user', set_user),
   ],
   prefix="api/"
   )

   urlpatterns = [
    path('', lambda request: HttpResponse('Hello from Django Modern Rest!')),
    path(user_router.prefix, include((user_router.urls, 'your_app'), namespace="api"))
  ]

Note that now endpoints will changes to http://localhost:8000/api/get_users and http://localhost:8000/api/set_user

But what next? Next we add `Controller` to our app

What is controller? Controller is a class that handle all endpoints with the same set of components of our system.
This mean that if we have set of endpoints to interact with user (create, modify, delete) its better to put them in single UserController.

In our case we create 2 controllers (one for user and another for users):

.. code-block:: python

  # models for users
  class UsersResponseModel(pydantic.BaseModel):
      users: dict

  class UsersController(Controller[PydanticSerializer]):
      def get(self) -> UsersResponseModel:
          return UsersResponseModel(users=DATABASE)

  class UserCreateModel(pydantic.BaseModel):
      id: int
      name: str

  # model for user
  class UserCreateStatusModel(pydantic.BaseModel):
      status: bool
      message: str

  class UserResponseModel(pydantic.BaseModel):
      name: str

  class UserController(
      Controller[PydanticSerializer],
      Body[UserCreateModel]
  ):

      def post(self) -> UserCreateStatusModel:
         user_id = self.parsed_body.id
         name = self.parsed_body.name
         DATABASE[user_id] = name
         return UserCreateStatusModel(status=True, message=f"User with {user_id=} and {name=} created")

Now all data will be validate!


Swagger
-------

Last thing that we will do in this simple example is connect Swagger doc to our app.
It will help you to debug all of your endpoinst.

For this lets add the following code:

 .. code-block:: python

   # add to imports
   from dmr.openapi import openapi_spec
   from dmr.openapi.renderers import JsonRenderer, SwaggerRenderer

   # change config to this
   settings.configure(
       DEBUG=True,
       SECRET_KEY='your-secret-key-here',
       ROOT_URLCONF=__name__,
       INSTALLED_APPS=[
           'django.contrib.contenttypes',
           'django.contrib.auth',
           'django.contrib.staticfiles',
           'dmr'
       ],
       MIDDLEWARE=[
           'django.middleware.security.SecurityMiddleware',
           'django.middleware.common.CommonMiddleware',
       ],
       STATIC_URL='/static/',
       STATICFILES_FINDERS=[
          'django.contrib.staticfiles.finders.AppDirectoriesFinder',
       ],
       TEMPLATES=[
          {
              'APP_DIRS': True,
              'BACKEND': 'django.template.backends.django.DjangoTemplates',
          },
       ],
   )

   # add this path to urlpatterns
   path(
        'docs/',
        openapi_spec(user_router, renderers=[JsonRenderer(), SwaggerRenderer()]),
   )

And then visit https://localhost:8000/docs/swagger for the interactive docs.

.. image:: /_static/images/swagger.png
   :alt: Swagger view
   :align: center

That's it, enjoy your new project!




