"""
General models
"""

import uuid
from beaver import settings
from django.db import models
from django.core.mail import send_mail

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

            send_mail(  'Activate your Beaver account', message,
                        settings.BEAVER_NO_REPLY_ADDRESS, [self.email],
                        fail_silently = False)

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
    
    title           = models.CharField(blank = False, max_length = 100)
    description     = models.TextField(blank = True, null = True)
    enabled         = models.BooleanField(blank = False, default = True)

class BaseSchedule(models.Model):
    """
    Defining a base schedule
    """
    calendar                    = models.ForeignKey(Calendar)

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
        return u'%s, %i min' % (self.name, self.length)

    calendar        = models.ForeignKey(Calendar)

    title           = models.CharField(blank = False, max_length = 100)
    description     = models.TextField(blank = True)
    length          = models.IntegerField(  blank = False, max_length = 50,
                                            help_text = 'Length in minutes')
    price           = models.FloatField(blank = True, null = True)