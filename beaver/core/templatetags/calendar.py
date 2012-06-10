import datetime

from django import template
from core import models
from beaver import settings

register = template.Library()

def get_day_timeslots(date, attrs):
    """
    Returns a list of ('from-to', True/False) where from is the start time and to is the end time
    of the timeslot. The second option is whether or not the timeslot is bookable
    
    input       schedule_id, booking_type_id
    """
    schedule_id = int(attrs.split(',')[0])
    schedule = models.Schedule.objects.get(id = schedule_id)
    booking_type_id = int(attrs.split(',')[1])
    timeslots = schedule.timeslots(  datetime.datetime.strptime(date, '%Y-%m-%d'),
                                datetime.datetime.strptime(date, '%Y-%m-%d'),
                                booking_type_id, return_strings = True)
    return timeslots[datetime.datetime.strptime(date, '%Y-%m-%d')]

def short_date_format(date):
    """
    Returns a list of ('from-to', True/False) where from is the start time and to is the end time
    of the timeslot. The second option is whether or not the timeslot is bookable
    """
    return datetime.datetime.strptime(date, '%Y-%m-%d').strftime(settings.SHORT_DATE_FORMAT)

def datetime_format(date, format):
    return date.strftime(format)

def isodate_time_min(date):
    """
    Returns a list of ('from-to', True/False) where from is the start time and to is the end time
    of the timeslot. The second option is whether or not the timeslot is bookable
    """
    return date.strftime('%Y-%m-%d %H:%M')

def day_name(date):
    """
    Returns a list of ('from-to', True/False) where from is the start time and to is the end time
    of the timeslot. The second option is whether or not the timeslot is bookable
    """
    day = {
        1: 'mon',
        2: 'tue',
        3: 'wed',
        4: 'thu',
        5: 'fri',
        6: 'sat',
        7: 'sun',
    }
    return day[datetime.date.isoweekday(datetime.datetime.strptime(date, '%Y-%m-%d'))]

register.filter('datetime_format', datetime_format)
register.filter('day_name', day_name)
register.filter('get_day_timeslots', get_day_timeslots)
register.filter('short_date_format', short_date_format)
register.filter('isodate_time_min', isodate_time_min)