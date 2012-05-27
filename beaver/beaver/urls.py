from beaver import settings
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

# 404 handler
handler404 = 'core.views.handler404'

urlpatterns = patterns('',
    # Media
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    
    # Index
    url(r'^$', 'core.views.index'),
    
    # Admin
    url(r'^admin/', include(admin.site.urls)),
    
    # Account management
    url(r'^accounts/activate/(?P<activation_key>[\w-]+)$', 'core.views.accounts_activate'),
    url(r'^accounts/delete$', 'core.views.accounts_delete'),
    url(r'^accounts/delete/complete$', 'core.views.accounts_delete_complete'),
    url(r'^accounts/login[/]?$', 'core.views.accounts_login'),
    url(r'^accounts/logout[/]?$', 'core.views.accounts_logout'),
    url(r'^accounts/lost_password$', 'core.views.accounts_lost_password'),
    url(r'^accounts/register$', 'core.views.accounts_register'),
    url(r'^accounts/register/complete$', 'core.views.accounts_register_complete'),
    url(r'^accounts/settings$', 'core.views.accounts_settings'),
    
    # Customer's calendars URL
    url(r'^calendar/(?P<calendar_slug>[\w-]+)$', 'core.views.calendar_view'),
    
    # Calendars
    url(r'^calendars/create$', 'core.views.calendars_create'),
    url(r'^calendars/edit/(?P<calendar_id>[\w-]+)$', 'core.views.calendars_edit'),
    url(r'^calendars/list$', 'core.views.calendars_list'),
    
    # Schedules
    url(r'^schedules/create/(?P<calendar_id>[\w-]+)$', 'core.views.schedules_create'),
    url(r'^schedules/created$', 'core.views.schedules_created'),
    url(r'^schedules/edit/(?P<schedule_id>[\w-]+)$', 'core.views.schedules_edit'),
)
