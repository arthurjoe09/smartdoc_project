import os
from django.conf import settings
from django.core.management.base import BaseCommand
import logging
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Deletes all files in a given media subfolder (e.g., qr_codes/, barcodes/)'

    def add_arguments(self, parser):
        parser.add_argument('folder', type=str, help='Subfolder in media/ to clear')
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Only list files that would be deleted, don’t actually delete them',
        )

    def handle(self, *args, **options):
        folder = options['folder']
        dry_run = options['dry_run']

        folder_path = os.path.join(settings.MEDIA_ROOT, folder)

        if not os.path.exists(folder_path):
            logger.warning(f'Folder {folder} does not exist')
            return

        files = os.listdir(folder_path)
        if not files:
            logger.info(f"No files found in {folder_path}. Nothing to delete.")
            return

        for file_name in files:
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path):
                if dry_run:
                    logger.info(f"All files deleted from: {folder_path}")
                else:
                    os.remove(file_path)
                    logger.debug(f"Deleted file: {file_path}")

        if dry_run:
            logger.info("Dry run. Nothing to delete.")
        else:
            self.stdout.write(self.style.SUCCESS("✅ All files deleted."))

