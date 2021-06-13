from django.core.management.base import BaseCommand, CommandError
from bracket.models import ytVid

class Command(BaseCommand):
    help = "refreshes the database to have all the info.json files loaded"
    
    def handle():
        
        return f'updated DB with {len(newYtVids)} new videos'