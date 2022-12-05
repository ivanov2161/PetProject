import os
import sys

try:
    sys.path.remove('/usr/lib/python3/dist-packages')
except:
    pass

sys.path.append('ПУТЬ_ДО_ПРОЕКТА')
sys.path.append('ПУТЬ_ДО_ПАКЕТОВ_PYTHON')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'имя_проекта.settings')

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()