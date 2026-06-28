from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import University, Course, Region, UniversityCourse

# Register your models here.

class RegionResource(resources.ModelResource):
    class Meta:
        model = Region
        fields = ('id', 'name')

    def skip_row(self, instance, original, row, import_validation_errors=None):
        name = row.get('name')
        if not name or str(name).strip() == '':
            return True
        return super().skip_row(instance, original, row, import_validation_errors=import_validation_errors)

@admin.register(Region)
class RegionAdmin(ImportExportModelAdmin):
    resource_classes = [RegionResource]
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
    )

    class Meta:
        model = UniversityCourse
        fields = ('id', 'university', 'course', 'level', 'duration', 'requirements', 'fee', 'application_link', 'is_active')
        export_order = ('id', 'university', 'course', 'level', 'duration', 'requirements', 'fee', 'application_link', 'is_active')

@admin.register(UniversityCourse)
class UniversityCourseAdmin(ImportExportModelAdmin):
    resource_classes = [UniversityCourseResource]
    search_fields = ['university__name', 'course__name', 'level']
    list_display = ['university', 'course', 'level', 'duration']
    list_filter = ['level', 'duration', 'is_active']
    autocomplete_fields = ['university', 'course']

