from django.contrib import admin
from .models import Task
from django.contrib.auth.models import Group

admin.site.unregister(Group)

class TaskAdmin(admin.ModelAdmin):
    list_display = ('title','user','complete')
admin.site.register(Task,TaskAdmin);
