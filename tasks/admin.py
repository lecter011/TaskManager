from django.contrib import admin
from .models import Task

class taskAdmin(admin.ModelAdmin):
    readonly_fields = ('created_on',)

# Register your models here.
admin.site.register(Task, taskAdmin)
