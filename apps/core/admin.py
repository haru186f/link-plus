from django.contrib import admin
from .models import BusStop, BusSchedule, College, Department, Course, ReceivedEmail
from .models import Room, SchoolPeriod, LectureSchedule

admin.site.register(BusStop)
admin.site.register(BusSchedule)

admin.site.register(College)
admin.site.register(Department)
admin.site.register(Course)

admin.site.register(Room)
admin.site.register(SchoolPeriod)
admin.site.register(LectureSchedule)

@admin.register(ReceivedEmail)
class ReceivedEmailAdmin(admin.ModelAdmin):
    list_display = ('subject', 'sender', 'received_at')
    search_fields = ('subject', 'sender', 'body')
