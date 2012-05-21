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
        return email

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
The booking beaver team
""" % ( self.first_name, self.email, 
        settings.BEAVER_EXTERNAL_URL, self.activation_key, self.email)

            send_mail(  'Activate your Beaver account', message,
                        settings.BEAVER_NO_REPLY_ADDRESS, [self.email], 
                        fail_silently = False)

        # Save the object
        super(Account, self).save(*args, **kwargs)
    