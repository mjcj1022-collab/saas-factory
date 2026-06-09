from django.contrib import admin
from .models import FranchiseBrand, Franchisee, FranchiseLocation, TrainingModule

@admin.register(FranchiseBrand)
class FranchiseBrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'industry', 'created_at']
    list_filter = ['industry']
    search_fields = ['name']

@admin.register(Franchisee)
class FranchiseeAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'status', 'created_at']
    list_filter = ['status']
    search_fields = ['full_name', 'email']

@admin.register(FranchiseLocation)
class FranchiseLocationAdmin(admin.ModelAdmin):
    list_display = ['address', 'launch_status', 'target_open_date']
    list_filter = ['launch_status']
    search_fields = ['address']

@admin.register(TrainingModule)
class TrainingModuleAdmin(admin.ModelAdmin):
    list_display = ['title', 'content_type', 'is_required', 'sequence']
    list_filter = ['is_required']
    search_fields = ['title']
