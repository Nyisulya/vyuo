from django.db import models

# Create your models here.
class Region(models.Model):
    name = models.CharField(max_length=70, unique=True)
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['name']
class University(models.Model):
    TYPE_CHOICE = [
        ('University', 'University'),
        ('University College', 'University College'),
        ('Institute', 'Institute'),
        ('University Compus College', 'University Compus College'),
        ('Non University', 'Non University')
    ]
    TYPE_UNIVER = [
        ('Private', 'Private'),
        ('Goverment', 'Goverment')
    ]
    name = models.CharField(max_length=150, unique=True)
    type = models.CharField(max_length=40, choices=TYPE_CHOICE, blank=True, null=True)
    umiliki = models.CharField(max_length=30, choices=TYPE_UNIVER ,blank=True, null=True)
    website = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=11, null=True, blank=True)
    region = models.ForeignKey(Region, on_delete=models.PROTECT, related_name="univesity")
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['name']
    def __str__(self):
        return self.name
class Course(models.Model):
    name = models.CharField(max_length=140, unique=True)
    description = models.TextField(blank=True)
    class Meta:
        ordering = ['name']
    def __str__(self):
        return self.name
class Requirement(models.Model):
    title = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField()
    def __str__(self):
        return self.title
    
class UniversityCourse(models.Model):
    LEVEL_CHOICE = [
        ('Certificate', 'Certificate'),
        ('Diploma','Diploma'),
        ('Degree', 'Degree'),
        
    ]
    DURA_TYPE = [
        ('1','1'),
        ('2','2'),
        ('3','3'),
        ('4','4'),
        ('5','5'),
    ]
   
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='unicourse')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='program')
    level = models.CharField(max_length=50, choices=LEVEL_CHOICE)
    duration = models.CharField(max_length=10, choices=DURA_TYPE)
    requirements = models.ForeignKey(Requirement, on_delete=models.CASCADE, related_name='university', blank=True, null=True)
    fee = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    application_link = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ['university','course','level']
        ordering = ['university','course']
    def __str__(self):
        return f"{self.university.name} {self.course.name} {self.level}"
    