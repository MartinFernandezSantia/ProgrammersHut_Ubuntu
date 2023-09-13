"""
WSGI config for ProgrammersHut project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os
import sys

path = '/var/www/ProgrammersHut'
if path not in sys.path:
	sys.path.append(path)
	
os.environ["DJANGO_SETTINGS_MODULE"] =  "ProgrammersHut.settings"
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
