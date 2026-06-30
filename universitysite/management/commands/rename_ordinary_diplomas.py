from django.core.management.base import BaseCommand
from django.db import transaction
from universitysite.models import Course, UniversityCourse
import re

class Command(BaseCommand):
    help = "Badilisha kozi zinazoanza na 'Ordinary Diploma' kuwa 'Diploma' na unganisha data"

    def handle(self, *args, **options):
        # Find all courses starting with "Ordinary Diploma" (case-insensitive)
        all_courses = Course.objects.all()
        target_pattern = re.compile(r'^ordinary\s+diploma', re.IGNORECASE)
        
        courses_to_process = []
        for c in all_courses:
            if target_pattern.match(c.name):
                courses_to_process.append(c)
                
        self.stdout.write(self.style.WARNING(f"Tumepata kozi {len(courses_to_process)} zinazoanza na 'Ordinary Diploma'."))
        
        with transaction.atomic():
            for old_course in courses_to_process:
                # Create the new name (replace "Ordinary Diploma" with "Diploma")
                new_name = target_pattern.sub('Diploma', old_course.name).strip()
                
                self.stdout.write(f"\nInashughulikiwa: '{old_course.name}' -> '{new_name}'")
                
                # Check if the target course already exists
                target_course = Course.objects.filter(name__iexact=new_name).first()
                
                if not target_course:
                    # If it doesn't exist, we can simply rename the old course
                    self.stdout.write(self.style.SUCCESS(f" -> Kozi '{new_name}' haipo. Inabadilishwa jina moja kwa moja."))
                    old_course.name = new_name
                    old_course.save()
                else:
                    # If it exists, we must merge UniversityCourse references
                    self.stdout.write(f" -> Kozi '{new_name}' tayari ipo. Tunaunganisha viungo vya vyuo...")
                    old_ucs = UniversityCourse.objects.filter(course=old_course)
                    
                    for old_uc in old_ucs:
                        # Check if a duplicate relationship already exists
                        duplicate_uc = UniversityCourse.objects.filter(
                            university=old_uc.university,
                            course=target_course,
                            level=old_uc.level
                        ).first()
                        
                        if duplicate_uc:
                            self.stdout.write(f"   - Mgongano chuo '{old_uc.university.name}': tayari kina kozi zote mbili. Tunaunganisha sifa.")
                            # Merge requirements
                            merged_reqs = ""
                            if old_uc.requirements and duplicate_uc.requirements:
                                if old_uc.requirements.strip() != duplicate_uc.requirements.strip():
                                    merged_reqs = f"{duplicate_uc.requirements}\n\nAU\n\n{old_uc.requirements}"
                                else:
                                    merged_reqs = duplicate_uc.requirements
                            else:
                                merged_reqs = duplicate_uc.requirements or old_uc.requirements
                                
                            duplicate_uc.requirements = merged_reqs
                            
                            # Merge fee (take the non-null or lower fee)
                            if old_uc.fee and not duplicate_uc.fee:
                                duplicate_uc.fee = old_uc.fee
                            
                            # Merge duration
                            if old_uc.duration and not duplicate_uc.duration:
                                duplicate_uc.duration = old_uc.duration
                                
                            duplicate_uc.save()
                            # Delete the old relation
                            old_uc.delete()
                        else:
                            # No duplicate relationship, just reassign the course
                            self.stdout.write(f"   - Inahamishwa kwenda chuo '{old_uc.university.name}'")
                            old_uc.course = target_course
                            old_uc.save()
                    
                    # Now delete the old course since all references are gone
                    self.stdout.write(self.style.SUCCESS(f" -> Inafuta kozi ya zamani '{old_course.name}'"))
                    old_course.delete()

        self.stdout.write(self.style.SUCCESS("\nZoezi limekamilika kikamilifu!"))
