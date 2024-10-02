import os, sys
 
#project directory
sys.path.append('/home/b/balayi3c/thewoman.balayi3c.beget.tech/venv/lib/python3.11/site-packages')
sys.path.append('/home/b/balayi3c/thewoman.balayi3c.beget.tech')
 
#project settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "the_woman.settings")
 
#start server
 
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
