"""
General models
"""

import re
import uuid
import pprint
import datetime
from beaver import settings
from core import definitions
from django.db import models
from django.utils.timezone import utc
from django.core.mail import send_mail

# Instanciate logging
import logging
logger = logging.getLogger('core.models')

pp = pprint.PrettyPrinter(indent = 4)

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
    logo            = models.ImageField(upload_to = u'uploads/%Y/%m/%d', blank = True, null = True)
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

class BookingType(models.Model):
    """
    Definition of a booking type
    """
    def __unicode__(self):
        return u'%s, %s min (%0.2f %s)' % ( self.title, self.length,
                                            self.price, self.currency)

    calendar        = models.ForeignKey(Calendar)

    title           = models.CharField(blank = False, max_length = 100)
    description     = models.TextField(blank = True)
    length          = models.IntegerField(  blank = False, max_length = 4,
                                            help_text = 'Length in minutes')
    price           = models.FloatField(blank = False)
    currency        = models.CharField( blank = False,
                                        choices = definitions.CURRENCIES,
                                        max_length = 3)
    enabled         = models.BooleanField(default = True)

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

    def timeslots(self, start_date, end_date, booking_type_id, return_strings = False):
        """
        Method calculating timeslots for a given time period

        start_date          datetime.datetime object
        end_date            datetime.datetime object
        booking_type_id     id of a booking type to use

        Returns
        timeslots = {
            datetime.datetime(Y-m-d) : [(s, e), (s, e)]
        }
        """
        # Instanciate the return dict
        timeslots = {}

        # Get the booking_type
        booking_type = BookingType.objects.get(id = booking_type_id)

        # Get all bookings for the period
        bookings = Booking.objects.filter(  schedule = self.id,
                                            start__gte = start_date.replace(tzinfo = utc))
        for booking in bookings:
            print booking

        # Loop over all dates
        delta_days = (end_date - start_date).days
        while delta_days >= 0:
            # date refers to the date we are currently calculating
            date = end_date - datetime.timedelta(days = delta_days)

            # Instanciate this date in the return dict
            timeslots[date] = []

            # If the customer is closed this day,
            # just go to next
            if not self.base_schedule.get_enabled(date.weekday()):
                # Go to the next day in the range
                delta_days -= 1
                continue

            #
            # Calculate timespans that is of interest
            #
            booked_timespans = []

            # Get not bookable times from base schedule
            booked_timespans += [(
                (date + datetime.timedelta(  hours = int(self.base_schedule.get_not_bookable_from(date.weekday()).split(':')[0]),
                                            minutes = int(self.base_schedule.get_not_bookable_from(date.weekday()).split(':')[1]))).replace(tzinfo = utc),
                (date + datetime.timedelta(  hours = int(self.base_schedule.get_not_bookable_to(date.weekday()).split(':')[0]),
                                            minutes = int(self.base_schedule.get_not_bookable_to(date.weekday()).split(':')[1]))).replace(tzinfo = utc),
            )]

            # Insert bookings to the list
            for booking in bookings:
                if date.strftime('%Y-%m-%d') == booking.start.strftime('%Y-%m-%d'):
                    booking_start   = booking.start.replace(tzinfo = utc)
                    booking_end     = booking_start + datetime.timedelta(minutes = booking.length)

                    booked_timespans += [(booking_start, booking_end)]
            
            # Sort the timespans and merge any overlaps
            sorted_timespans = sorted(booked_timespans)
            booked_timespans = []
            for timespan in sorted_timespans:
                # Always add the first timespan
                if len(booked_timespans) == 0:
                    booked_timespans += [timespan]
                    continue

                # Pseudo code:
                # booked_timespans  = [(a, b)]
                # timespan          = (a', b')
                # if a' < b:
                #    booked_timespans = [(a - b')]
                if timespan[0] < booked_timespans[len(booked_timespans) - 1][1]:
                    old = booked_timespans[len(booked_timespans) - 1]
                    booked_timespans.pop()
                    booked_timespans += [(old[0], timespan[1])]
                else:
                    booked_timespans += [timespan]
            
            # Calculate the actual bookable timespans
            timespans = []
            i = 0
            while i <= len(booked_timespans):
                # If it is the first timestamp (i.e. from day start)
                if i == 0:
                    timespan_start  = (date + datetime.timedelta(
                        hours = int(self.base_schedule.get_bookable_from(date.weekday()).split(':')[0]),
                        minutes = int(self.base_schedule.get_bookable_from(date.weekday()).split(':')[1])
                    )).replace(tzinfo = utc)
                    timespan_end    = booked_timespans[i][0]
                # If it is the last timestamp (i.e. to day end)
                elif i + 1 > len(booked_timespans):
                    timespan_start  = booked_timespans[i - 1][1]
                    timespan_end    = (date + datetime.timedelta(
                        hours = int(self.base_schedule.get_bookable_to(date.weekday()).split(':')[0]),
                        minutes = int(self.base_schedule.get_bookable_to(date.weekday()).split(':')[1])
                    )).replace(tzinfo = utc)
                # If it is a timespan in the middle
                else:
                    timespan_start  = booked_timespans[i - 1][1]
                    timespan_end    = booked_timespans[i][0]

                ## Calculate how many timeslots that fits within timespan_end - timespan_start
                # Then fill timeslots
                num_slots = int((timespan_end - timespan_start).total_seconds()/60/booking_type.length)
                while num_slots:
                    # Calculate new timeslot end
                    timespan_end = timespan_start + datetime.timedelta(minutes = booking_type.length)

                    ## OPTIONAL TODO
                    # If we are implementing padding between timeslots, this is where it should
                    # be added.

                    # Add to list
                    if return_strings:
                        timespans += [(
                            timespan_start.strftime('%H:%M'),
                            timespan_end.strftime('%H:%M'),
                            True
                        )]
                    else:
                        timespans += [(timespan_start, timespan_end, True)]

                    # Update start time
                    timespan_start = timespan_end
                    num_slots -= 1

                i += 1
            
            ##
            ## Fill out the booked timespans
            ##
            i = 0
            while i < len(timespans) - 1:
                # Check if current timespan end is less than next timespan start
                # and it is not an already booked slot (as we are adding to the same list)
                if timespans[i][1] < timespans[i + 1][0] and timespans[i][2] is not False:
                    timespans += [(
                        timespans[i][1],
                        timespans[i + 1][0],
                        False
                    )]
                

                i += 1
                
            # Add the timeslots to this day
            timeslots[date] = sorted(timespans)

            # Go to the next day in the range
            delta_days -= 1

        return timeslots

class Booking(models.Model):
    """
    Defines a made Booking
    """
    def __unicode__(self):
        return u'%s, %s (%i min)' % (self.title, self.start.isoformat(), self.length)
        
    schedule        = models.ForeignKey(Schedule)
    booking_type    = models.ForeignKey(BookingType)

    title           = models.CharField(blank = False, max_length = 100)
    start           = models.DateTimeField(blank = False)
    length          = models.IntegerField(blank = False, max_length = 4)
    price           = models.FloatField(blank = True, null = True)
    currency        = models.CharField( blank = False,
                                        choices = definitions.CURRENCIES,
                                        max_length = 3)
    paid            = models.BooleanField(default = False)

    user_email      = models.EmailField(blank = False, verbose_name = 'E-mail')
    user_passphrase = models.CharField(blank = False, max_length = 20, verbose_name = 'Password')
    user_comment    = models.TextField(blank = True, verbose_name = 'Comment')
