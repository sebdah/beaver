import random

from beaver import settings
from core import forms, models

from django.contrib import auth
from django.shortcuts import redirect
from django.core.mail import send_mail
from django import forms as django_forms
from django.contrib.auth.decorators import login_required
from django.views.generic.simple import direct_to_template

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
                account.activate()
                activated = True
    except django_forms.ValidationError:
        pass
    except models.Account.DoesNotExist:
        pass

    return direct_to_template(request, 'core/accounts/activate.html', { 'activated': activated })

@login_required
def accounts_delete(request):
    """
    Delete account
    """
    account = models.Account.objects.get(email = request.user.email)

    if request.method == 'POST':
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
                auth.login(request, account)

                # If the next parameter is set
                if 'next' in request.GET:
                    return redirect(request.GET['next'])

                return redirect("/")
            else:
                error = True
                error_message = "Your account has been disabled!"
        else:
            error = True
            error_message = "Your username and password were incorrect."

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

                return direct_to_template(  request,
                                            'core/accounts/lost_password_done.html',
                                            {'request': request})
        except models.Account.DoesNotExist:
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
def accounts_settings(request):
    """
    Edit account information
    """
    account = models.Account.objects.get(email = request.user.email)

    account_updated = False
    if request.method == 'POST':
        form = forms.EditAccountForm(request.POST, instance = account)
        if form.is_valid():
            form.save()
            account_updated = True
    else:
        form = forms.EditAccountForm(instance = account)

    return direct_to_template(  request,
                                'core/accounts/settings.html',
                                {   'request': request,
                                    'form': form,
                                    'account_updated': account_updated })

@login_required
def calendars_create(request):
    """
    Create a new Calendar object
    """
    account = models.Account.objects.get(email = request.user.email)
    if request.method == 'POST':
        form = forms.CalendarForm(request.POST)
        if form.is_valid():
            new_calendar = form.save(commit = False)
            new_calendar.owner = account
            title = new_calendar.title
            new_calendar.save()
            calendar = models.Calendar.objects.get(owner = account, title = title)
            return redirect('/schedules/create/%i' % calendar.id)
    else:
        form = forms.CalendarForm()

    return direct_to_template(  request,
                                'core/calendars/create.html',
                                {   'request': request,
                                    'form': form, })

@login_required
def calendars_edit(request, calendar_id):
    """
    Edit a Calendar object
    """
    account = models.Account.objects.get(email = request.user.email)
    calendar = models.Calendar.objects.get(id = calendar_id, owner = account)
    
    if request.method == 'POST':
        form = forms.CalendarForm(request.POST, instance = calendar)
        if form.is_valid():
            updated_calendar = form.save(commit = False)
            updated_calendar.owner = account
            updated_calendar.save()
    else:
        form = forms.CalendarForm(instance = calendar)

    return direct_to_template(  request,
                                'core/calendars/edit.html',
                                {   'request': request,
                                    'form': form,
                                    'calendar': calendar, })

@login_required
def calendars_list(request):
    """
    List of an Accounts calendars
    """
    account = models.Account.objects.get(email = request.user.email)
    calendars = models.Calendar.objects.filter(owner = account, enabled = True)

    has_calendars = False
    if len(calendars) > 0:
        has_calendars = True

    return direct_to_template(  request,
                                'core/calendars/list.html',
                                {   'request': request,
                                    'has_calendars': has_calendars,
                                    'calendars': calendars, })

def index(request):
    """
    Index page
    """
    return direct_to_template(request, 'core/index.html', {'request': request})

@login_required
def schedules_create(request, calendar_id):
    """
    Create a new Schedule object
    """
    account = models.Account.objects.get(email = request.user.email)
    if request.method == 'POST':
        form = forms.BaseScheduleForm(request.POST)
        if form.is_valid():
            schedule = form.save(commit = False)
            schedule.calendar = models.Calendar.objects.get(id = calendar_id)
            schedule.save()
            return redirect('/schedules/created')
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
