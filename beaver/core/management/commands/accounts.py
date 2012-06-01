
"""
Command file managing accounts
"""

import datetime
from optparse import make_option

from core import models
from beaver import settings
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    args = ''
    help = 'Customer accounts commands'
    
    option_list = BaseCommand.option_list + (
        make_option('--clean-inactive',
                    action = 'store_true',
                    dest = 'clean_inactive',
                    default = '',
                    help = 'Remove inactive accounts'),
    )
    
    def handle(self, *args, **options):
        if options.get('clean_inactive') != '':
            clean_inactive()
    
def clean_inactive():
    """
    Remove all inactive accounts
    """
    accounts = models.Account.objects.filter(is_active = False)
    for account in accounts:
        registered = datetime.datetime( year = account.registered.year,
                                        month = account.registered.month,
                                        day = account.registered.day )
        
        # If the number of inactive days has been passed,
        # delete the account
        if settings.BEAVER_INACTIVE_DAYS_LIMIT >= int((datetime.datetime.utcnow() - registered).total_seconds()/60/60/24):
            account.delete()
