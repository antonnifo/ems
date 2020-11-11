import csv
import datetime
from django.utils.safestring import mark_safe

from django.contrib import admin
from django.http import HttpResponse

from .models import Employee, Customer, Assignment, Task, Leave


def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;'\
        'filename={}.csv'.format(opts.verbose_name)
    writer = csv.writer(response)

    fields = [field for field in opts.get_fields() if not field.many_to_many
              and not field.one_to_many]

    # Write a first row with header information
    writer.writerow([field.verbose_name for field in fields])
    # Write data rows
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response


export_to_csv.short_description = 'Export to CSV'

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):

    list_display = ['id','user', 'residence', 'phone','id_no']
    list_filter = ['created','gender','residence']    
    list_per_page = 20
    actions = [export_to_csv]

    # fields = ('cust_type','name', 'address', 'phone','id_number' )
    # def save_model(self, request, obj, form, change):
    #     if not change:
    #         obj.added_by = request.user
    #     obj.save() 

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['id','user', 'residence', 'phone','id_no']
    list_filter = ['created','gender','residence']    
    list_per_page = 20
    actions = [export_to_csv]

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['id','assignee', 'task']
    list_filter = ['created',]    
    list_per_page = 20
    actions = [export_to_csv]

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['id','title', 'due_date','paid','done','amount','owner']
    list_filter = ['created',]    
    list_per_page = 20
    actions = [export_to_csv]

@admin.register(Leave)
class LeaveAdmin(admin.ModelAdmin):
    list_display = ['id','employee','from_date','to_date']
    list_filter = ['created',]    
    list_per_page = 20
    actions = [export_to_csv]