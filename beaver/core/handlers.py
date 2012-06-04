"""
Misc code for handling data
"""

import os

from beaver import settings

# Handle the uploaded logo
def file_upload_handler(uploaded_file, calendar_id):
    folder = u'%s/uploads/%i' % (settings.MEDIA_ROOT, calendar_id)
    if not os.path.exists(folder):
        try:
            os.makedirs(folder)
        except:
            logger.error('Error creating directory %s' % folder)

    with open(u'%s/%s' % (folder, uploaded_file.name), 'wb+') as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)
