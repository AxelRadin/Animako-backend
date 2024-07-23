from django.contrib import admin
from .models import Staff, StaffTimetable

# class StaffTimetableInline(admin.TabularInline):
#     model = StaffTimetable
#     extra = 0
    

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin): 
    list_display = ('staff_name', 'staff_fullname', 'staff_email', 'staff_role')
    #inlines = [StaffTimetableInline]
    list_filter = ('staff_role', 'staff_name', 'staff_fullname')
    search_fields = ('staff_name', 'staff_fullname', 'staff_role')
    

@admin.register(StaffTimetable)
class StaffTimetableAdmin(admin.ModelAdmin):
    list_display = ('staff_task','task_start_time', 'task_end_time', 'task_status') 
    filter_horizontal = ('staff_id',)