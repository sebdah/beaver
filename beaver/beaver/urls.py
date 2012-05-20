from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'beaver.views.home', name='home'),
    # url(r'^beaver/', include('beaver.foo.urls')),
    
    # Admin
    url(r'^admin/', include(admin.site.urls)),
    
    # Registration URLs
    # Users would then be able to register by visiting the URL
    # ``/accounts/register/``, login (once activated) at
    # ``/accounts/login/``, etc.
    (r'^accounts/', include('registration.backends.default.urls')),
)
