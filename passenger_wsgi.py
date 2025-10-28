import sys, os

# Path to your project
project_home = '/home/aditacoq/myproject'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

os.environ['DJANGO_SETTINGS_MODULE'] = 'adita_backend.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

