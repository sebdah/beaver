"""
View for the core module
"""

import os
import random
import datetime

from beaver import settings
from core import forms, models, definitions

from django.contrib import auth
from django.shortcuts import redirect
from django.core.mail import send_mail
from django import forms as django_forms
from django.shortcuts import get_object_or_404
from django.core.files.storage import default_storage
from django.contrib.auth.decorators import login_required
from django.views.generic.simple import direct_to_template

# Instanciate logging
import logging
logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger('core.views')

def accounts_activate(request, activation_key):
    """
    Activate account
    """
    activated = False
    email_address = request.GET['email']
    email_field = django_forms.EmailField()

    try:
        email_field.clean(email_address)
        account = models.Account.objects.get(email = email_address)
        if account:
            if account.activation_key == activation_key:
                logger.info('Activated account %s' % (account.email))
                account.activate()
                activated = True
    except django_forms.ValidationError:
        logger.warning('ValidationError when activating account')
    except models.Account.DoesNotExist:
        logger.warning('DoesNotExist when activating account')

    return direct_to_template(request, 'core/accounts/activate.html', { 'activated': activated })

@login_required
def accounts_delete(request):
    """
    Delete account
    """
    account = models.Account.objects.get(email = request.user.email)

    if request.method == 'POST':
        logger.info('Deleted account %s' % (account.email))
        account.delete()
        auth.logout(request)
        return redirect('/accounts/delete/complete')

    return redirect('/accounts/settings')

def accounts_delete_complete(request):
    """
    Delete account done
    """
    return direct_to_template(request, 'core/accounts/delete_complete.html', {'request': request})

def accounts_login(request):
    """
    Method for logging in
    """
    error = False
    error_message = None

    if request.method == 'POST':
        account = auth.authenticate(username = request.POST['email'],
                                    password = request.POST['password'])

        if account:
            if account.is_active:
                logger.debug('Account %s logged in' % (account.email))
                auth.login(request, account)

                # If the next parameter is set
                if 'next' in request.GET:
                    return redirect(request.GET['next'])

                return redirect("/")
            else:
                logger.debug('Account %s not logged in, it is disabled' % (account.email))
                error = True
                error_message = "Your account has been disabled!"
        else:
            error = True
            error_message = "Your username and password were incorrect."
            logger.debug('Could not log in, username and password where incorrect')

    return direct_to_template(  request,
                                'core/accounts/login.html',
                                {'form': forms.AuthenticationForm(),
                                'error': error,
                                'error_message': error_message,
                                'request': request})

@login_required
def accounts_logout(request):
    """
    Logout an Account
    """
    logger.debug('Logged out account %s' % request.user.email)
    auth.logout(request)
    return direct_to_template(request, 'core/accounts/logout.html', {'request': request})

def accounts_register(request):
    """
    Registration form for a new account
    """
    if request.method == 'POST':
        form = forms.AccountForm(request.POST)
        if form.is_valid():
            form.save()
            logger.info('Registered new user %s' % request.POST['email'])
            auth.logout(request)
            return redirect('/accounts/register/complete')
    else:
        form = forms.AccountForm()

    return direct_to_template(  request,
                                'core/accounts/register.html',
                                {   'request': request,
                                    'form': form, })

def accounts_lost_password(request):
    """
    Lost password page
    """
    if request.method == 'POST':
        try:
            account = models.Account.objects.get(email = request.POST['email'])

            if account:
                # Generate new password
                valid_chars = 'abcdefghijklmnopqrstuvqxyz0123456789_-'
                password = "".join(random.sample(valid_chars, 14))

                # Update the user's password
                account.password = password
                account.save()

                # Send the e-mail with the new password
                message = \
"""Hello, %s

You (or somebody else) has requested a password reset for %s. Your new password is:

%s

Best regards
The Booking Beaver Team
""" % (account.first_name, account.email, password)

                send_mail(  'Password reset', message, settings.BEAVER_NO_REPLY_ADDRESS,
                            [account.email], fail_silently = False)
                logger.info('Sent password reset e-mail to %s' % account.email)

                return direct_to_template(  request,
                                            'core/accounts/lost_password_done.html',
                                            {'request': request})
        except models.Account.DoesNotExist:
            logger.warning('Password reset: e-mail address not found')
            pass

    return direct_to_template(  request,
                                'core/accounts/lost_password.html',
                                {'form': forms.LostPasswordForm(),
                                'request': request})

def accounts_register_complete(request):
    """
    This is the page users are redirected to after
    a successful account registration
    """
    return direct_to_template(request, 'core/accounts/register_complete.html', {'request': request})

@login_required
def accounts_settings(request, account_id):
    """
    Edit account information
    """
    account = models.Account.objects.get(id = account_id)

    account_updated = False
    if request.method == 'POST':
        form = forms.EditAccountForm(request.POST, instance = account)
        if form.is_valid():
            form.save()
            account_updated = True
            logger.debug('Settings updated for %s' % account.email)
    else:
        form = forms.EditAccountForm(instance = account)

    return direct_to_template(  request,
                                'core/accounts/settings.html',
                                {   'request': request,
                                    'form': form,
                                    'account_updated': account_updated })

@login_required
def bookingtypes_create(request, calendar_id):
    """
    Create a new BookingType object
    """
    calendar = models.Calendar.objects.get(id = calendar_id)
    
    if request.method == 'POST':
        form = forms.BookingTypeForm(request.POST)
        if form.is_valid():
            bookingtype = form.save(commit = False)
            bookingtype.calendar_id = calendar_id
            bookingtype.save()
            logger.debug('BookingType created for calendar %i' % calendar.id)
            
            return redirect('/calendars/%i/edit' % calendar.id)
    else:
        form = forms.BookingTypeForm()

    return direct_to_template(  request,
                                'core/bookingtypes/create.html',
                                {   'request': request,
                                    'form': form, })

@login_required
def bookingtypes_delete(request, bookingtype_id):
    """
    Delete a given booking type
    """
    booking_type = models.BookingType.objects.get(id = bookingtype_id)
    calendar = models.Calendar.objects.get(id = booking_type.calendar.id)
    
    # Delete the booking type
    logger.debug('Deleted BookingType %i' % booking_type.id)
    booking_type.delete()
    
    # If this is the last enabled booking type for the
    # calendar, remove the published flag from the
    # calendar
    if len(models.BookingType.objects.filter(calendar = calendar.id, enabled = True)) == 0:
        form = forms.CalendarForm(instance = calendar)
        updated_calendar = form.save(commit = False)
        updated_calendar.enabled = False
        updated_calendar.save()
    
    return redirect('/calendars/%i/edit' % (calendar.id))

@login_required
def bookingtypes_edit(request, bookingtype_id):
    """
    Edit a BookingType object
    """
    booking_type = models.BookingType.objects.get(id = bookingtype_id)

    if request.method == 'POST':
        form = forms.BookingTypeForm(request.POST, instance = booking_type)
        if form.is_valid():
            form.save()
            logger.debug('BookingType %i updated' % (booking_type.id))

            return redirect('/calendars/%i/edit' % booking_type.calendar.id)
    else:
        form = forms.BookingTypeForm(instance = booking_type)

    return direct_to_template(  request,
                                'core/bookingtypes/edit.html',
                                {   'request': request,
                                    'form': form,
                                    'booking_type': booking_type, })

def calendar_book(request, calendar_slug, schedule_id, bookingtype_id):
    """
    Create a booking
    """
    calendar = get_object_or_404(models.Calendar, slug = calendar_slug)
    schedule = get_object_or_404(models.Schedule, id = schedule_id)
    bookingtype = get_object_or_404(models.BookingType, id = bookingtype_id)
    
    # Make sure we get the params we need
    if 'timeslot_start' not in request.GET or 'date' not in request.GET:
        return redirect('/404')
    
    # Store the GETs
    timeslot_start = request.GET['timeslot_start']
    date = request.GET['date']
    
    # Calculate timeslot end
    start_dt = datetime.datetime.strptime(  u'%s %s' % (date, timeslot_start),
                                            '%Y-%m-%d %H:%M')
    timeslot_end = (start_dt + datetime.timedelta(minutes = bookingtype.length)).strftime('%H:%M')
    
    # Form
    if request.POST:
        form = forms.BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit = False)
    form = forms.BookingForm()
    
    return direct_to_template(  request,
                                'core/calendar/book.html',
                                {   'request': request,
                                    'schedule': schedule,
                                    'calendar': calendar,
                                    'timeslot_start': timeslot_start,
                                    'timeslot_end': timeslot_end,
                                    'bookingtype': bookingtype,
                                    'form': form,
                                    'date': date, })

def calendar_view(request, calendar_slug):
    """
    Show the public calendar
    """
    calendar = get_object_or_404(models.Calendar, slug = calendar_slug)
    schedules = models.Schedule.objects.filter(calendar = calendar.id)
    booking_types = models.BookingType.objects.filter(calendar = calendar.id)
    
    # If the calendar is not published
    if not calendar.enabled:
        return redirect('/404')
        
    # Check if the user has selected a booking type
    booking_type = 'not-set'
    if 'booking_type' in request.GET:
        booking_type = int(request.GET['booking_type'])

    # See if any other dates has been requested
    if 'start_date' in request.GET:
        start_date = datetime.datetime.strptime(request.GET['start_date'], '%Y-%m-%d')
    else:
        # Get the date of this week's Monday
        day_of_week = datetime.date.weekday(datetime.datetime.today())
        start_date = datetime.datetime.today() - datetime.timedelta(days = day_of_week)
    
    # Add dates to list
    i = 0
    dates = []
    while i < 7:
        dates += [(start_date + datetime.timedelta(days = i)).strftime('%Y-%m-%d'),]
        i += 1
    
    # Show a little edit link for calendar owners
    is_owner = False
    if request.user.email == calendar.owner.email:
        is_owner = True
        
    if booking_type != 'not-set':
        timeslot_string = '%i,%i' % (schedules[0].id, (models.BookingType.objects.get(id = booking_type)).length)
    else:
        timeslot_string = '%i,%i' % (schedules[0].id, 60)

    return direct_to_template(  request,
                                'core/calendar/view.html',
                                {   'request': request,
                                    'calendar': calendar,
                                    'schedule': schedules[0],
                                    'is_owner': is_owner,
                                    'weekdays': definitions.WEEKDAYS_SHORT,
                                    'date_range': dates,
                                    'booking_types': booking_types,
                                    'booking_type': booking_type,
                                    'timeslot_string': timeslot_string,
                                    'previous_week_start': (datetime.datetime.strptime(dates[0], '%Y-%m-%d') - datetime.timedelta(days = 7)).strftime('%Y-%m-%d'),
                                    'next_week_start': (datetime.datetime.strptime(dates[6], '%Y-%m-%d') + datetime.timedelta(days = 1)).strftime('%Y-%m-%d'), 
                                    'week_number': datetime.datetime.strptime(dates[0], '%Y-%m-%d').isocalendar()[1], })

@login_required
def calendars_create(request):
    """
    Create a new Calendar object
    """
    account = models.Account.objects.get(email = request.user.email)
    if request.method == 'POST':
        form = forms.CalendarExceptEnabledForm(request.POST, request.FILES)
        if form.is_valid():
            # Create the new calendar object
            new_calendar = form.save(commit = False)
            new_calendar.owner = account
            new_calendar.enabled = False
            title = new_calendar.title
            new_calendar.save()
            
            # Get the calendar object
            calendar = models.Calendar.objects.get(owner = account, title = title)
            
            # Go to the schedule planner
            logger.debug('Calendar %i created' % (calendar.id))
            return redirect('/schedules/create/%i' % calendar.id)
    else:
        # Serve an empty form
        form = forms.CalendarExceptEnabledForm()

    return direct_to_template(  request,
                                'core/calendars/create.html',
                                {   'request': request,
                                    'form': form,
                                    'external_url': settings.BEAVER_EXTERNAL_CALENDAR_URL, })

@login_required
def calendars_edit(request, calendar_id):
    """
    Edit a Calendar object
    """
    account = models.Account.objects.get(email = request.user.email)
    calendar = models.Calendar.objects.get(id = calendar_id, owner = account)
    schedules = models.Schedule.objects.filter(calendar = calendar, owner = account).order_by('owner')
    booking_types = models.BookingType.objects.filter(calendar = calendar).order_by('title')

    updated = False
    if request.method == 'POST':
        form = forms.CalendarForm(request.POST, request.FILES, instance = calendar)
        if form.is_valid():
            updated_calendar = form.save(commit = False)
            updated_calendar.owner = account
            
            # Don't publish the calendar if it has no booking types
            # associated
            if len(models.BookingType.objects.filter(calendar = calendar, enabled = True)) == 0:
                updated_calendar.enabled = False
            
            updated_calendar.save()
            logger.debug('Calendar %i updated' % (calendar.id))
            updated = True
            form = forms.CalendarForm(instance = calendar)
    else:
        # Generate form
        form = forms.CalendarForm(instance = calendar)

    return direct_to_template(  request,
                                'core/calendars/edit.html',
                                {   'request': request,
                                    'form': form,
                                    'calendar': calendar,
                                    'schedule': schedules[0],
                                    'updated': updated,
                                    'external_url': settings.BEAVER_EXTERNAL_CALENDAR_URL,
                                    'media_url': settings.MEDIA_URL,
                                    'booking_types': booking_types, })

@login_required
def calendars_list(request):
    """
    List of an Accounts calendars
    """
    account = models.Account.objects.get(email = request.user.email)
    calendars = models.Calendar.objects.filter(owner = account).order_by('title')

    has_calendars = False
    if len(calendars) > 0:
        has_calendars = True

    return direct_to_template(  request,
                                'core/calendars/list.html',
                                {   'request': request,
                                    'has_calendars': has_calendars,
                                    'calendars': calendars,
                                    'external_url': settings.BEAVER_EXTERNAL_CALENDAR_URL })

def contact_us(request):
    """
    Contact page
    """
    if request.method == 'POST':
        form = forms.ContactForm(request.POST)
        
        if form.is_valid():
            try:
                send_mail(  '[contact-us] %s' % (request.POST['subject']),
                            request.POST['message'], 
                            request.POST['email_address'],
                            [settings.BEAVER_CONTACT_US_ADDRESS],
                            fail_silently = False)
                logger.info('Sent contact us e-mail to %s from %s' % ([settings.BEAVER_CONTACT_US_ADDRESS], request.POST['email_address']))
            except:
                logger.error('Error sending contact us email to %s from %s' % ([settings.BEAVER_CONTACT_US_ADDRESS],
                                                                                request.POST['email_address']))
            return redirect('/contact-us/done')
                
    form = forms.ContactForm()
    
    return direct_to_template(request, 'core/contact_us.html', {'request': request, 'form': form})

def contact_us_done(request):
    """
    E-mail sent page for contact form
    """
    return direct_to_template(request, 'core/contact_us_done.html', {'request': request})

def handler404(request):
    """
    404 page
    """
    return direct_to_template(request, 'core/404.html', {'request': request})

def handler500(request):
    """
    500 page
    """
    return direct_to_template(request, 'core/500.html', {'request': request})

def index(request):
    """
    Index page
    """
    return direct_to_template(request, 'core/index.html', {'request': request})

@login_required
def schedules_create(request, calendar_id):
    """
    Create a new BaseSchedule object
    """
    account = models.Account.objects.get(email = request.user.email)
    calendar = models.Calendar.objects.get(id = calendar_id)

    if request.method == 'POST':
        # Query Dict
        query_dict = {}

        # Add the timeslot
        query_dict['timeslot_length'] = 60

        # Make a new query list matching the model
        for day in definitions.WEEKDAYS:
            day_enabled = '%s_enabled' % (day)
            day_bookable_timespan = '%s_bookable_timespan' % (day)
            day_bookable_from = '%s_bookable_from' % (day)
            day_bookable_to = '%s_bookable_to' % (day)
            day_not_bookable = '%s_not_bookable' % (day)
            day_not_bookable_from = '%s_not_bookable_from' % (day)
            day_not_bookable_to = '%s_not_bookable_to' % (day)

            if day_enabled not in request.POST:
                query_dict[day_enabled] = False
            else:
                query_dict[day_enabled] = request.POST[day_enabled]

            if day_bookable_from not in request.POST:
                day_bookable_from_value = ''
            else:
                day_bookable_from_value = request.POST[day_bookable_from]

            if day_bookable_to not in request.POST:
                day_bookable_to_value = ''
            else:
                day_bookable_to_value = request.POST[day_bookable_to]

            if day_not_bookable_from not in request.POST:
                day_not_bookable_from_value = ''
            else:
                day_not_bookable_from_value = request.POST[day_not_bookable_from]

            if day_not_bookable_to not in request.POST:
                day_not_bookable_to_value = ''
            else:
                day_not_bookable_to_value = request.POST[day_not_bookable_to]

            query_dict[day_bookable_timespan] = u'%s-%s' % (day_bookable_from_value,
                                                            day_bookable_to_value)
            query_dict[day_not_bookable] = u'%s-%s' % ( day_not_bookable_from_value,
                                                        day_not_bookable_to_value)

        form = forms.BaseScheduleForm(query_dict)
        if form.is_valid():
            # Create the BaseSchedule
            base_schedule = form.save(commit = False)
            base_schedule.calendar = calendar
            base_schedule.save()

            # Add new Schedule object
            form = forms.ScheduleForm()
            schedule = form.save(commit = False)
            schedule.calendar = calendar
            schedule.owner = account
            schedule.base_schedule = base_schedule
            schedule.save()
            
            logger.debug('Created new schedule for calendar %i (by account %s)' % ( calendar.id,
                                                                                    account.email))

            return redirect('/calendars/list')
    else:
        form = forms.BaseScheduleForm()

    return direct_to_template(  request,
                                'core/schedules/create.html',
                                {   'request': request,
                                    'form': form, })

@login_required
def schedules_created(request):
    """
    Schedule created page
    """
    return direct_to_template(request, 'core/schedules/created.html', {'request': request})

@login_required
def schedules_edit(request, schedule_id):
    """
    Edit a Calendar object
    """
    account = models.Account.objects.get(email = request.user.email)
    schedule = models.Schedule.objects.get(id = schedule_id, owner = account)

    updated = False
    if request.method == 'POST':
        base_schedule = models.BaseSchedule.objects.get(id = schedule.base_schedule.id)

        # Query Dict
        query_dict = {}

        # Add the timeslot
        query_dict['timeslot_length'] = 60

        # Make a new query list matching the model
        for day in definitions.WEEKDAYS:
            day_enabled = '%s_enabled' % (day)
            day_bookable_timespan = '%s_bookable_timespan' % (day)
            day_bookable_from = '%s_bookable_from' % (day)
            day_bookable_to = '%s_bookable_to' % (day)
            day_not_bookable = '%s_not_bookable' % (day)
            day_not_bookable_from = '%s_not_bookable_from' % (day)
            day_not_bookable_to = '%s_not_bookable_to' % (day)

            if day_enabled not in request.POST:
                query_dict[day_enabled] = False
            else:
                query_dict[day_enabled] = request.POST[day_enabled]

            if day_bookable_from not in request.POST:
                day_bookable_from_value = ''
            else:
                day_bookable_from_value = request.POST[day_bookable_from]

            if day_bookable_to not in request.POST:
                day_bookable_to_value = ''
            else:
                day_bookable_to_value = request.POST[day_bookable_to]

            if day_not_bookable_from not in request.POST:
                day_not_bookable_from_value = ''
            else:
                day_not_bookable_from_value = request.POST[day_not_bookable_from]

            if day_not_bookable_to not in request.POST:
                day_not_bookable_to_value = ''
            else:
                day_not_bookable_to_value = request.POST[day_not_bookable_to]

            query_dict[day_bookable_timespan] = u'%s-%s' % (day_bookable_from_value,
                                                            day_bookable_to_value)
            query_dict[day_not_bookable] = u'%s-%s' % ( day_not_bookable_from_value,
                                                        day_not_bookable_to_value)

        form = forms.BaseScheduleForm(query_dict, instance = base_schedule)
        if form.is_valid():
            updated_base_schedule = form.save(commit = False)
            updated_base_schedule.calendar_id = base_schedule.calendar_id
            updated_base_schedule.save()
            updated = True

    base_schedule = models.BaseSchedule.objects.get(id = schedule.base_schedule.id)
    values = {}
    for day in definitions.WEEKDAYS:
        day_enabled = '%s_enabled' % (day)
        day_bookable_from = '%s_bookable_from' % (day)
        day_bookable_to = '%s_bookable_to' % (day)
        day_not_bookable_from = '%s_not_bookable_from' % (day)
        day_not_bookable_to = '%s_not_bookable_to' % (day)

        if base_schedule.get_enabled(day):
            values[day_enabled] = 'checked'
        else:
            values[day_enabled] = ''

        values[day_bookable_from]       = base_schedule.get_bookable_from(day)
        values[day_bookable_to]         = base_schedule.get_bookable_to(day)
        values[day_not_bookable_from]   = base_schedule.get_not_bookable_from(day)
        values[day_not_bookable_to]     = base_schedule.get_not_bookable_to(day)

    return direct_to_template(  request,
                                'core/schedules/edit.html',
                                {   'request': request,
                                    'updated': updated,
                                    'schedule': schedule,
                                    'values': values, })
