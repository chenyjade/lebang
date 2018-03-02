from django.contrib import admin
from .models import User, Task, Report
# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('id','username','phone')
admin.site.register(User, UserAdmin)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id','task_title','time')
admin.site.register(Task, TaskAdmin)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('id','description','time')
admin.site.register(Report, ReportAdmin)
