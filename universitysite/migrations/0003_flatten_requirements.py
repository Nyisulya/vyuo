# Generated manually for safe data migration
from django.db import migrations, models

def copy_data_forward(apps, schema_editor):
    UniversityCourse = apps.get_model('universitysite', 'UniversityCourse')
    
    # Copy data from the old ForeignKey to the new TextField
    # Since we are adding requirement_text and it exists in the database alongside the old requirements_id
    for course in UniversityCourse.objects.all():
        # requirements is the ForeignKey. course.requirements gets the Requirement object.
        if course.requirements:
            course.requirement_text = course.requirements.description
            course.save()

def copy_data_backward(apps, schema_editor):
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('universitysite', '0002_university_umiliki_alter_university_type'),
    ]

    operations = [
        # Step 1: Add temporary text field
        migrations.AddField(
            model_name='universitycourse',
            name='requirement_text',
            field=models.TextField(blank=True, null=True),
        ),
        
        # Step 2: Copy data from ForeignKey relation to TextField
        migrations.RunPython(copy_data_forward, copy_data_backward),
        
        # Step 3: Remove the old ForeignKey field
        migrations.RemoveField(
            model_name='universitycourse',
            name='requirements',
        ),
        
        # Step 4: Rename the temporary text field to 'requirements'
        migrations.RenameField(
            model_name='universitycourse',
            old_name='requirement_text',
            new_name='requirements',
        ),
        
        # Step 5: Delete the Requirement table
        migrations.DeleteModel(
            name='Requirement',
        ),
    ]
