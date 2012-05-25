Model relations
===============

    Calendar            * -> 1 Account (i.e. the owner)
    BaseSchedule        * -> 1 Calendar
    Schedule            * -> 1 Calendar
    Schedule            * -> 1 Account
    Schedule            * -> 1 BaseSchedule
    ScheduleException   * -> 1 Schedule
    Booking             * -> 1 Account
    BookingType         * -> 1 Calendar

Models
======

Account
-------

    email           String
    password        String
    first_name      String
    last_name       String
    is_active       Boolean
    activation_key  String
    registered      DateTime
    last_updated    DateTime

BaseSchedule
------------

    calendar                      FK(Calendar)
    monday_enabled                Boolean
    monday_bookable_timespan      Time-Time
    monday_not_bookable           Time-Time,Time-Time
    tuesday_enabled               Boolean
    tuesday_bookable_timespan     Time-Time
    tuesday_not_bookable          Time-Time,Time-Time
    wednesday_enabled             Boolean
    wednesday_bookable_timespan   Time-Time
    wednesday_not_bookable        Time-Time,Time-Time
    thursday_enabled              Boolean
    thursday_bookable_timespan    Time-Time
    thursday_not_bookable         Time-Time,Time-Time
    friday_enabled                Boolean
    friday_bookable_timespan      Time-Time
    friday_not_bookable           Time-Time,Time-Time
    saturday_enabled              Boolean
    saturday_bookable_timespan    Time-Time
    saturday_not_bookable         Time-Time,Time-Time
    sunday_enabled                Boolean
    sunday_bookable_timespan      Time-Time
    sunday_not_bookable           Time-Time,Time-Time

Booking
-------

    account         FK(Account)
    schedule        FK(Schedule)
    title           String
    start           DateTime
    end             DateTime
    comment         Text
    price           Float

BookingType
-----------

    calendar        FK(Calendar)
    title           String
    description     Text
    length          Integer (minutes)
    price           Float

Calendar
--------

    owner           FK(Account)
    title           String
    description     Text
    enabled         Boolean

Schedule
--------

    owner           FK(Account)
    calendar        FK(Calendar)
    baseschedule    FK(BaseSchedule)
    enabled         Boolean

ScheduleException
-----------------

    schedule        FK(Schedule)
    type            String (TIMESPAN, FULL_DAY)
    start           DateTime
    end             DateTime

If `FULL_DAY` is defined we will only consider the date of `start`.

