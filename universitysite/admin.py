from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
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

class UniversityCourseResource(resources.ModelResource):
    university = fields.Field(
        column_name='university',
        attribute='university',
        widget=ForeignKeyWidget(University, 'name')
    )
    course = fields.Field(
        column_name='course',
        attribute='course',
        widget=ForeignKeyWidget(Course, 'name')
    )
    requirements = fields.Field(
        column_name='requirements',
        attribute='requirements',
        widget=ForeignKeyWidget(Requirement, 'title')
    )
    requirement_description = fields.Field(
        column_name='requirement_description',
        readonly=True
    )

    class Meta:
        model = UniversityCourse
        fields = ('id', 'university', 'course', 'level', 'duration', 'requirements', 'requirement_description', 'fee', 'application_link', 'is_active')
        export_order = ('id', 'university', 'course', 'level', 'duration', 'requirements', 'requirement_description', 'fee', 'application_link', 'is_active')

    def dehydrate_requirement_description(self, university_course):
        if university_course.requirements:
            return university_course.requirements.description
        return ""

@admin.register(UniversityCourse)
class UniversityCourseAdmin(ImportExportModelAdmin):
    resource_class = UniversityCourseResource
    resource_classes = [UniversityCourseResource]
    search_fields = ['university__name', 'course__name', 'level']
    list_display = ['university', 'course', 'level', 'duration']
    list_filter = ['level', 'duration', 'is_active']
    autocomplete_fields = ['university', 'course', 'requirements']

@admin.register(Requirement)
class RequirementAdmin(ImportExportModelAdmin):
    search_fields = ['title', 'description']
