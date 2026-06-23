from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import University, Course, Region, UniversityCourse, Requirement

# Register your models here.

@admin.register(Region)
class RegionAdmin(ImportExportModelAdmin):
    search_fields = ['name']
    list_display = ['name']

@admin.register(Course)
class CourseAdmin(ImportExportModelAdmin):
    search_fields = ['name', 'description']
    list_display = ['name']

@admin.register(University)
class UniversityAdmin(ImportExportModelAdmin):
    search_fields = ['name', 'type', 'region__name', 'umiliki']
    list_display = ['name', 'type', 'region', 'umiliki']
    list_filter = ['type', 'umiliki', 'is_active', 'region']

@admin.register(UniversityCourse)
class UniversityCourseAdmin(ImportExportModelAdmin):
    search_fields = ['university__name', 'course__name', 'level']
    list_display = ['university', 'course', 'level', 'duration']
    list_filter = ['level', 'duration', 'is_active']

@admin.register(Requirement)
class RequirementAdmin(ImportExportModelAdmin):
    search_fields = ['title', 'description']
