import os
import django
from django.conf import settings

# Configure Django to use SQLite database for local test
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vyuofinder.settings')

# Modify settings before calling django.setup() to point to the local sqlite db
from vyuofinder import settings as vyuofinder_settings

vyuofinder_settings.DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db.sqlite3'),
    }
}

django.setup()

from universitysite.admin import UniversityCourseResource
from universitysite.models import UniversityCourse

print("Checking if any UniversityCourse exists in sqlite...")
count = UniversityCourse.objects.count()
print("Count:", count)

# Try exporting
try:
    resource = UniversityCourseResource()
    dataset = resource.export()
    print("Headers:", dataset.headers)
    if len(dataset) > 0:
        print("Row 1:", dataset[0])
    else:
        print("No data exported.")
except Exception as e:
    import traceback
    traceback.print_exc()
