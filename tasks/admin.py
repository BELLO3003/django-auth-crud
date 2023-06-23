from django.contrib import admin
from .models import Task

class TaskAdmin(admin.ModelAdmin):
    readonly_fields=("created", ) #Al modelo de Admin le pasamos la fecha 'created' para visualizarla

# Register your models here.
admin.site.register(Task, TaskAdmin)