from core import models
from django.contrib import admin

class AccountAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'registered', 'last_updated', 'is_active')
    list_filter = ('is_active',)

class CalendarAdmin(admin.ModelAdmin):
    list_display = ('owner', 'title', 'enabled')
    list_filter = ('enabled',)

class BaseScheduleAdmin(admin.ModelAdmin):
    list_display = ('calendar',)
    
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('calendar', 'owner', 'base_schedule', 'enabled')
    list_filter = ('enabled',)
    
class BookingAdmin(admin.ModelAdmin):
    list_display = ('account', 'schedule', 'title')

class BookingTypeAdmin(admin.ModelAdmin):
    list_display = ('calendar', 'title', 'length')

admin.site.register(models.Account, AccountAdmin)
admin.site.register(models.Calendar, CalendarAdmin)
admin.site.register(models.BaseSchedule, BaseScheduleAdmin)
admin.site.register(models.Schedule, ScheduleAdmin)
admin.site.register(models.Booking, BookingAdmin)
admin.site.register(models.BookingType, BookingTypeAdmin)
