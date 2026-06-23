from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import University, Course, Region, UniversityCourse, Requirement

# Register your models here.

@admin.register(Region)
class RegionAdmin(ImportExportModelAdmin):
    pass

@admin.register(Course)
class CourseAdmin(ImportExportModelAdmin):
    pass

@admin.register(University)
class UniversityAdmin(ImportExportModelAdmin):
    pass

@admin.register(UniversityCourse)
class UniversityCourseAdmin(ImportExportModelAdmin):
    pass

@admin.register(Requirement)
class RequirementAdmin(ImportExportModelAdmin):
    pass
    
