from beaver import settings
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

# 404 handler
handler404 = 'core.views.handler404'

# 500 handler
handler500 = 'core.views.handler500'

urlpatterns = patterns('',
    # Media
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    
    # 404/500 (not needed for Django 404/500 handling..)
    url(r'^404$', 'core.views.handler404'),
    url(r'^500$', 'core.views.handler500'),
    
    # Favicon
    (r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': '/media/images/favicon.ico'}),
    
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
    url(r'^accounts/(?P<account_id>[\w-]+)/settings$', 'core.views.accounts_settings'),
    
    # Booking type
    url(r'^bookingtypes/create/(?P<calendar_id>[\w-]+)$', 'core.views.bookingtypes_create'),
    url(r'^bookingtypes/(?P<bookingtype_id>[\w-]+)/delete$', 'core.views.bookingtypes_delete'),
    url(r'^bookingtypes/(?P<bookingtype_id>[\w-]+)/edit$', 'core.views.bookingtypes_edit'),
    
    # Customer's calendars URL
    url(r'^calendar/(?P<calendar_slug>[\w-]+)$', 'core.views.calendar_view'),
    url(r'^calendar/(?P<calendar_slug>[\w-]+)/book/(?P<schedule_id>[\w-]+)/(?P<bookingtype_id>[\w-]+)$', 'core.views.calendar_book'),
    url(r'^calendar/(?P<calendar_slug>[\w-]+)/cancel/(?P<booking_id>[\w-]+)$', 'core.views.calendar_cancel'),
    url(r'^calendar/(?P<calendar_slug>[\w-]+)/cancel/(?P<booking_id>[\w-]+)/done$', 'core.views.calendar_cancel_done'),
    url(r'^calendar/(?P<calendar_slug>[\w-]+)/complete/(?P<booking_id>[\w-]+)$', 'core.views.calendar_complete'),
    
    # Calendars
    url(r'^calendars/create$', 'core.views.calendars_create'),
    url(r'^calendars/(?P<calendar_id>[\w-]+)/edit$', 'core.views.calendars_edit'),
    url(r'^calendars/list$', 'core.views.calendars_list'),
    
    # Contact us
    url(r'^contact-us$', 'core.views.contact_us'),
    url(r'^contact-us/done$', 'core.views.contact_us_done'),
    
    # Schedules
    url(r'^schedules/create/(?P<calendar_id>[\w-]+)$', 'core.views.schedules_create'),
    url(r'^schedules/(?P<schedule_id>[\w-]+)/edit$', 'core.views.schedules_edit'),
)
