from django import template
from core import models

register = template.Library()

def get_day_timeslots(date, schedule_id):
    """
    Returns a list of ('from-to', True/False) where from is the start time and to is the end time
    of the timeslot. The second option is whether or not the timeslot is bookable
    """
    schedule = models.Schedule.objects.get(id = schedule_id)
    print schedule.get_timeslots(date)
    
    return schedule.get_timeslots(date)

register.filter('get_day_timeslots', get_day_timeslots)