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

Next lets create our `main.py` file with following code.

.. code-block:: python

  import django
  import sys
  from django.conf import settings
  from django.http import HttpResponse
  from django.urls import path
  from django.core.management import execute_from_command_line

  # Configure Django settings
  settings.configure(
      DEBUG=True,
      SECRET_KEY='your-secret-key-here',
      ROOT_URLCONF=__name__,
      INSTALLED_APPS=[
          'django.contrib.contenttypes',
          'django.contrib.auth',
      ],
      MIDDLEWARE=[
          'django.middleware.security.SecurityMiddleware',
          'django.middleware.common.CommonMiddleware',
      ],
  )

  # Initialize Django
  django.setup()

  # Define URL patterns
  urlpatterns = [
      path('', lambda request: HttpResponse('Hello from Django Modern Rest!')),
  ]

  if __name__ == '__main__':
     execute_from_command_line(sys.argv)


Now lets run our app using this command:

.. code-block:: bash

   python main.py runserver

When all goes fine you will see something like this:

<Past terminal example here>

The go to you brower and visit http://localhost:8000/.
You will see "Hello from Django Modern Rest!" message.

Congrats! You run your first app with dmr. But its look to much simple and we even don't import dmr itself, are we?



