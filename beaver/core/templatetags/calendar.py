import datetime

from django import template
from core import models
from beaver import settings

register = template.Library()

def get_day_timeslots(date, input):
    """
    Returns a list of ('from-to', True/False) where from is the start time and to is the end time
    of the timeslot. The second option is whether or not the timeslot is bookable
    """
    schedule_id = int(input.split(',')[0])
    timeslot_length = int(input.split(',')[1])
    schedule = models.Schedule.objects.get(id = schedule_id)
    
    return schedule.get_timeslots(date, timeslot_length)

def short_date_format(date):
    """
    Returns a list of ('from-to', True/False) where from is the start time and to is the end time
    of the timeslot. The second option is whether or not the timeslot is bookable
    """
    return datetime.datetime.strptime(date, '%Y-%m-%d').strftime(settings.SHORT_DATE_FORMAT)

register.filter('get_day_timeslots', get_day_timeslots)
register.filter('short_date_format', short_date_format)
