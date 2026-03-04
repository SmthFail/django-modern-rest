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

# Define URL patterns
urlpatterns = [
    path('', lambda request: HttpResponse('Hello from Django Modern Rest!')),
]

if __name__ == '__main__':
    execute_from_command_line(sys.argv)
