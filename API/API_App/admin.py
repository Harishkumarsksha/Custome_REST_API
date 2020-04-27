from django.contrib import admin

# Register your models here.
from API_App.models import EmployeeData


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('eno', 'ename', 'esal', 'eaddr')
    list_filter = ('eno', 'ename', 'eaddr')
    search_fields = ('eno', 'ename', 'eaddr')
    list_per_page = 25


admin.site.register(EmployeeData, EmployeeAdmin)
