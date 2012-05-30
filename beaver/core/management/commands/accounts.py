import datetime
from django.core.management.base import BaseCommand, CommandError
from core import models

class Command(BaseCommand):
    args = ''
    help = 'Customer accounts commands'
    
    options = ''
    
    def handle(self, *args, **options):
        accounts = models.Account.objects.filter(is_active = False)
        for account in accounts:
            print account.registered - datetime.datetime.today()
        