from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import University, Course

class UniversitySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return University.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.created_at

class CourseSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return Course.objects.all()

class StaticViewSitemap(Sitemap):
    priority = 1.0
    changefreq = "daily"

    def items(self):
        return ['universitysite:home', 'universitysite:university_list', 'universitysite:course_list']

    def location(self, item):
        return reverse(item)
