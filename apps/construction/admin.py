from django.contrib import admin
from .models import Project, Drawing, PunchItem, DailyReport

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'status', 'start_date', 'completion_date']
    list_filter = ['status']
    search_fields = ['name', 'project_number']

@admin.register(Drawing)
class DrawingAdmin(admin.ModelAdmin):
    list_display = ['drawing_number', 'title', 'discipline', 'revision', 'uploaded_at']
    list_filter = ['discipline']
    search_fields = ['drawing_number', 'title']

@admin.register(PunchItem)
class PunchItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'due_date']
    list_filter = ['status']
    search_fields = ['title']

@admin.register(DailyReport)
class DailyReportAdmin(admin.ModelAdmin):
    list_display = ['project', 'report_date', 'crew_count']
