"""
WSGI config for AXF project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

# 从AXF.settings中读取wsgi配置
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AXF.settings")

# django默认的application
application = get_wsgi_application()
