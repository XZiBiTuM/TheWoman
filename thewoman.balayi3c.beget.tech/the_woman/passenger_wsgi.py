# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, '/home/b/balayi3c/balayi3c.beget.tech/the_woman')
sys.path.insert(1, 'home/b/balayi3c/balayi3c.beget.tech/venv_django/lib/python3.11/site-packages')
os.environ['DJANGO_SETTINGS_MODULE'] = 'the_woman.settings'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
