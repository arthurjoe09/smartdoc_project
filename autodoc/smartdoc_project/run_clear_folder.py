import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smartdoc_project.settings')
django.setup()

from django.core.management import call_command

call_command('clear_files', 'qr_codes', '--dry-run')
