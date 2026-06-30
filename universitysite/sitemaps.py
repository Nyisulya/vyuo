from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import University, Course, Region
from django.utils import timezone

class UniversitySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return University.objects.filter(is_active=True).order_by('-created_at')

    def lastmod(self, obj):
        return obj.created_at


class CourseSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return Course.objects.all().order_by('name')

    def lastmod(self, obj):
        # Pata tarehe ya mwisho wa kozi kutoka program yake ya kwanza
        first_program = obj.program.order_by('-created_at').first()
        if first_program:
            return first_program.created_at
        return None


class RegionSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return Region.objects.all()

    def location(self, obj):
        return reverse('universitysite:vyuo', kwargs={'pk': obj.pk})


class StaticViewSitemap(Sitemap):
    changefreq = "daily"

    # Toa priority tofauti kwa kila ukurasa
    priority_map = {
        'universitysite:home': 1.0,
        'universitysite:university_list': 0.9,
        'universitysite:course_list': 0.9,
        'universitysite:about': 0.5,
        'universitysite:contact': 0.5,
        'universitysite:feedback': 0.4,
    }

    def items(self):
        return list(self.priority_map.keys())

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        return self.priority_map.get(item, 0.5)
