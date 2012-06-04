"""
General models
"""

import re
import uuid
import datetime
from beaver import settings
from core import definitions
from django.db import models
from django.core.mail import send_mail

# Instanciate logging
import logging
logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger('core.models')

class Account(models.Model):
    """
    Definition of an Account object
    """
    def __unicode__(self):
        return u'%s %s (%s)' % (self.first_name, self.last_name, self.email)

    email               = models.EmailField(blank = False, unique = True)
    password            = models.CharField(blank = False, max_length = 50)
    first_name          = models.CharField(blank = False, max_length = 50)
    last_name           = models.CharField(blank = False, max_length = 50)
    last_updated        = models.DateTimeField(auto_now = True)
    registered          = models.DateTimeField(auto_now_add = True)
    is_active           = models.BooleanField(default = False)
    activation_key      = models.CharField(blank = True, null = True, max_length = 50)
    is_authenticated    = False
    is_staff            = False # Should never be True

    def activate(self):
        """
        Activate account
        """
        self.is_active = True

        return self.save()

    def is_authenticated(self):
        return self.is_authenticated

    def save(self, *args, **kwargs):
        """
        Save a new account
        """
        # Generate activation key
        self.activation_key = uuid.uuid4()

        if not self.is_active:
            # Send activation e-mail
            message = \
"""\
Welcome %s,

You (or somebody else) has registrered an account for %s. Please follow
the below link in order to activate your account.

%s/accounts/activate/%s?email=%s

Best regards
The Booking Beaver team
""" % ( self.first_name, self.email,
        settings.BEAVER_EXTERNAL_URL, self.activation_key, self.email)
        
            try:
                send_mail(  'Activate your Beaver account', message,
                            settings.BEAVER_NO_REPLY_ADDRESS, [self.email],
                            fail_silently = False)
                logger.info('Sent registration/activation e-mail')
            except:
                logger.error('Failed sending registration/activation e-mail')

        # Save the object
        super(Account, self).save(*args, **kwargs)

class Calendar(models.Model):
    """
    A Calendar is a collection of Schedulesapp
    """
    class Meta:
        unique_together = ('owner', 'title')

    def __unicode__(self):
        return u'%s' % self.title

    owner           = models.ForeignKey(Account)

    slug            = models.SlugField(blank = False, unique = True, verbose_name = 'URL', help_text = 'Short URL to your calendar')
    title           = models.CharField(blank = False, max_length = 100)
    description     = models.TextField(blank = True, null = True)
    logo            = models.ImageField(upload_to = u'uploads/%s/', blank = True, null = True)
    url             = models.URLField(verbose_name = 'External website', blank = True, null = True)
    enabled         = models.BooleanField(blank = False, default = True, verbose_name = 'Published')

class BaseSchedule(models.Model):
    """
    Defining a base schedule
    """
    calendar                    = models.ForeignKey(Calendar)
    timeslot_length             = models.IntegerField(blank = False, default = 60)

    monday_enabled              = models.BooleanField(blank = False, default = False)
    monday_bookable_timespan    = models.CharField(blank = True, null = True, max_length = 40)
    monday_not_bookable         = models.CharField(blank = True, null = True, max_length = 200)
    tuesday_enabled             = models.BooleanField(blank = False, default = False)
    tuesday_bookable_timespan   = models.CharField(blank = True, null = True, max_length = 40)
    tuesday_not_bookable        = models.CharField(blank = True, null = True, max_length = 200)
    wednesday_enabled           = models.BooleanField(blank = False, default = False)
    wednesday_bookable_timespan = models.CharField(blank = True, null = True, max_length = 40)
    wednesday_not_bookable      = models.CharField(blank = True, null = True, max_length = 200)
    thursday_enabled            = models.BooleanField(blank = False, default = False)
    thursday_bookable_timespan  = models.CharField(blank = True, null = True, max_length = 40)
    thursday_not_bookable       = models.CharField(blank = True, null = True, max_length = 200)
    friday_enabled              = models.BooleanField(blank = False, default = False)
    friday_bookable_timespan    = models.CharField(blank = True, null = True, max_length = 40)
    friday_not_bookable         = models.CharField(blank = True, null = True, max_length = 200)
    saturday_enabled            = models.BooleanField(blank = False, default = False)
    saturday_bookable_timespan  = models.CharField(blank = True, null = True, max_length = 40)
    saturday_not_bookable       = models.CharField(blank = True, null = True, max_length = 200)
    sunday_enabled              = models.BooleanField(blank = False, default = False)
    sunday_bookable_timespan    = models.CharField(blank = True, null = True, max_length = 40)
    sunday_not_bookable         = models.CharField(blank = True, null = True, max_length = 200)

    def get_bookable_from(self, day):
        """
        Get the bookable from time for a given day
        """
        if day == 'monday' or day == 0:
            return self.monday_bookable_timespan.split('-')[0]
        elif day == 'tuesday' or day == 1:
            return self.tuesday_bookable_timespan.split('-')[0]
        elif day == 'wednesday' or day == 2:
            return self.wednesday_bookable_timespan.split('-')[0]
        elif day == 'thursday' or day == 3:
            return self.thursday_bookable_timespan.split('-')[0]
        elif day == 'friday' or day == 4:
            return self.friday_bookable_timespan.split('-')[0]
        elif day == 'saturday' or day == 5:
            return self.saturday_bookable_timespan.split('-')[0]
        elif day == 'sunday' or day == 6:
            return self.sunday_bookable_timespan.split('-')[0]

    def get_bookable_to(self, day):
        """
        Get the bookable from time for a given day
        """
        if day == 'monday' or day == 0:
            return self.monday_bookable_timespan.split('-')[1]
        elif day == 'tuesday' or day == 1:
            return self.tuesday_bookable_timespan.split('-')[1]
        elif day == 'wednesday' or day == 2:
            return self.wednesday_bookable_timespan.split('-')[1]
        elif day == 'thursday' or day == 3:
            return self.thursday_bookable_timespan.split('-')[1]
        elif day == 'friday' or day == 4:
            return self.friday_bookable_timespan.split('-')[1]
        elif day == 'saturday' or day == 5:
            return self.saturday_bookable_timespan.split('-')[1]
        elif day == 'sunday' or day == 6:
            return self.sunday_bookable_timespan.split('-')[1]

    def get_not_bookable_from(self, day):
        """
        Get the bookable from time for a given day
        """
        if day == 'monday' or day == 0:
            return self.monday_not_bookable.split('-')[0]
        elif day == 'tuesday' or day == 1:
            return self.tuesday_not_bookable.split('-')[0]
        elif day == 'wednesday' or day == 2:
            return self.wednesday_not_bookable.split('-')[0]
        elif day == 'thursday' or day == 3:
            return self.thursday_not_bookable.split('-')[0]
        elif day == 'friday' or day == 4:
            return self.friday_not_bookable.split('-')[0]
        elif day == 'saturday' or day == 5:
            return self.saturday_not_bookable.split('-')[0]
        elif day == 'sunday' or day == 6:
            return self.sunday_not_bookable.split('-')[0]

    def get_not_bookable_to(self, day):
        """
        Get the bookable from time for a given day
        """
        if day == 'monday' or day == 0:
            return self.monday_not_bookable.split('-')[1]
        elif day == 'tuesday' or day == 1:
            return self.tuesday_not_bookable.split('-')[1]
        elif day == 'wednesday' or day == 2:
            return self.wednesday_not_bookable.split('-')[1]
        elif day == 'thursday' or day == 3:
            return self.thursday_not_bookable.split('-')[1]
        elif day == 'friday' or day == 4:
            return self.friday_not_bookable.split('-')[1]
        elif day == 'saturday' or day == 5:
            return self.saturday_not_bookable.split('-')[1]
        elif day == 'sunday' or day == 6:
            return self.sunday_not_bookable.split('-')[1]

    def get_enabled(self, day):
        """
        Get the bookable from time for a given day
        """
        if day == 'monday' or day == 0:
            return self.monday_enabled
        elif day == 'tuesday' or day == 1:
            return self.tuesday_enabled
        elif day == 'wednesday' or day == 2:
            return self.wednesday_enabled
        elif day == 'thursday' or day == 3:
            return self.thursday_enabled
        elif day == 'friday' or day == 4:
            return self.friday_enabled
        elif day == 'saturday' or day == 5:
            return self.saturday_enabled
        elif day == 'sunday' or day == 6:
            return self.sunday_enabled

        return False

class Schedule(models.Model):
    """
    Definition of a schedule
    """
    def __unicode__(self):
        return u'%s %s - %s' % (self.owner.first_name, self.owner.last_name, self.calendar.title)

    calendar        = models.ForeignKey(Calendar)
    owner           = models.ForeignKey(Account)
    base_schedule   = models.ForeignKey(BaseSchedule)
    enabled         = models.BooleanField(default = True)

    def get_timeslots(self, date, timeslot_length):
        """
        Returns a list of ('from-to', True/False) where from is the start time and to is the end time
        of the timeslot. The second option is whether or not the timeslot is bookable
        """
        def calculator(start_point, end_point, timeslot_length):
            timeslots = []

            # Time format
            time_format = u'%H:%M'
            
            # Find out how many minutes it is between the start and the end
            time_delta = datetime.datetime.strptime(end_point, time_format) - datetime.datetime.strptime(start_point, time_format)
            time_delta = time_delta.total_seconds() / 60

            # Loop through all possible timeslots
            last_end_time = start_point
            num_timeslots = int(time_delta / timeslot_length)
            i = 0
            while i < num_timeslots:
                end_time = datetime.datetime.strptime(last_end_time, time_format) + datetime.timedelta(minutes = timeslot_length)
                end_time = end_time.strftime('%H:%M')
                timeslots += [(u'%s-%s' % (last_end_time, end_time), True)]
                last_end_time = end_time
                i += 1

            return timeslots

        # Find out what day of week the given date is
        year, month, day = date.split('-')
        day_of_week = datetime.date(int(year), int(month), int(day)).weekday()
        
        # Skip if the day is no enabled
        if not self.base_schedule.get_enabled(day_of_week):
            return []

        # Check if we should look at the not bookable times
        if not re.match('^[0-9]{2}:[0-9]{2}$', self.base_schedule.get_not_bookable_from(day_of_week)):
            timeslots = calculator(  self.base_schedule.get_bookable_from(day_of_week),
                                self.base_schedule.get_bookable_to(day_of_week),
                                timeslot_length)
            return timeslots
        else:
            timeslots = []
            timeslots += calculator(self.base_schedule.get_bookable_from(day_of_week),
                                    self.base_schedule.get_not_bookable_from(day_of_week),
                                    timeslot_length)
            timeslots += calculator(self.base_schedule.get_not_bookable_to(day_of_week),
                                    self.base_schedule.get_bookable_to(day_of_week),
                                    timeslot_length)
            return timeslots

class Booking(models.Model):
    """
    Defines a made Booking
    """
    def __unicode__(self):
        return u'%s - %s (%s - %s)' % (self.account, self.name, self.start_time, self.end_time)

    account         = models.ForeignKey(Account)
    schedule        = models.ForeignKey(Schedule)

    title           = models.CharField(blank = False, max_length = 100)
    start           = models.DateTimeField(blank = False)
    end             = models.DateTimeField(blank = False)
    comment         = models.TextField(blank = True)
    price           = models.FloatField(blank = True, null = True)

class BookingType(models.Model):
    """
    Definition of a booking type
    """
    def __unicode__(self):
        return u'%s, %i min (%0.2f %s)' % (self.title, self.length,
                                        self.price, self.currency)

    calendar        = models.ForeignKey(Calendar)

    title           = models.CharField(blank = False, max_length = 100)
    description     = models.TextField(blank = True)
    length          = models.IntegerField(  blank = False, max_length = 50,
                                            help_text = 'Length in minutes')
    price           = models.FloatField(blank = True, null = True)
    currency        = models.CharField( blank = False,
                                        choices = definitions.CURRENCIES,
                                        max_length = 3)
    enabled         = models.BooleanField(default = True)
