import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'glc.settings')

#application = get_wsgi_application()

from whitenoise import WhiteNoise
application = WhiteNoise(get_wsgi_application())

