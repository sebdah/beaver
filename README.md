Booking Beaver
==============

Requirements
------------
* Python 2.7
* Virtualenv
* Django 1.4
* Python Image Library
* Python Timezone (pytz)

Set up development environment
------------------------------

Initial setup:

    cd beaver.git
    virtualenv --prompt v -p python2.7 .ve
    source .ve/bin/activate
    pip install django pil pytz

Then each time you are developing, load the virtual Python environment with

    source .ve/bin/activate
