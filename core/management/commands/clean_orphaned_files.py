from django.core.management.base import BaseCommand
from core.models import LabImage   # Replace 'core' with your app name
import os

class Command(BaseCommand):
    help = "Clean up LabFile entries without corresponding files in storage"

    def handle(self, *args, **kwargs):
        # Fetch all LabFile entries
        for lab_file in LabImage.objects.all():
            # Check if the associated file exists in storage
            if not os.path.isfile(lab_file.file.path):
                self.stdout.write(f"Deleting orphaned record: {lab_file}")
                lab_file.delete()
