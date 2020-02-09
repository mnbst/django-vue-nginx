#!/usr/bin/env python
import os
import sys
# import ptvsd
#
# if os.environ.get('RUN_MAIN') or os.environ.get('WERKZEUG_RUN_MAIN'):
#     ptvsd.enable_attach(address=('0.0.0.0', 3000))
#     print('debug attach')

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.backend.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise
    execute_from_command_line(sys.argv)
