from django.contrib import admin
from .models import University, Course, Region, UniversityCourse, Requirement

# Register your models here.


admin.site.register(Region)
admin.site.register(Course)
admin.site.register(University)
admin.site.register(UniversityCourse)
admin.site.register(Requirement)
    
