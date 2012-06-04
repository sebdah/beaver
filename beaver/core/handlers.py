"""
Misc code for handling data
"""

import os

from beaver import settings
from core import models

# Instanciate logging
import logging
logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger('core.handlers')

# Handle the uploaded logo
def logo_upload_handler(uploaded_file, calendar_id):
    """
    Handing logo image uploads
    """
    calendar = models.Calendar.objects.get(id = calendar_id)
    
    # Remove any previous files for this calendar
    if calendar.logo is not None:
        if os.path.exists(u'%s/%s' % (settings.MEDIA_ROOT, calendar.logo)):
            print u'Removed replaced image %s/%s' % (settings.MEDIA_ROOT, calendar.logo)
            os.remove(u'%s/%s' % (settings.MEDIA_ROOT, calendar.logo))
    
    # Check that the folder exists,
    # otherwise create its
    folder = u'%suploads/%i' % (settings.MEDIA_ROOT, calendar.id)
    if not os.path.exists(folder):
        try:
            print 'Created new image folder for calendar %i' % calendar.id
            os.makedirs(folder)
        except:
            print 'Error creating directory %s' % folder

    # Write the file in chunks to avoid memory overflow
    #file_handle = open(u'%s/%s' % (folder, uploaded_file.name), 'wb+')
    #for chunk in uploaded_file.chunks():
    #    print "Wrote chunk to %s/%s" % (folder, uploaded_file.name)
    #    file_handle.write(chunk)
