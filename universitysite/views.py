from django.shortcuts import render, get_object_or_404
from .models import Region, University, Course, UniversityCourse, Feedback
from django.core.paginator import Paginator
from django.contrib.admin.views.decorators import staff_member_required
# Create your views here.
def determine_course_level(course_name):
    name_lower = course_name.lower().strip()
    words = name_lower.split()
    if not words:
        return 'Diploma'
        
    first_word = words[0]
    
    # Degree indicators
    degree_prefixes = ('bachelor', 'bsc', 'b.sc', 'doctor', 'md', 'phd', 'master', 'postgraduate')
    if first_word.startswith(degree_prefixes) or first_word in ('ba', 'b.a'):
        return 'Degree'
        
    # Check if contains 'degree'
    if 'degree' in name_lower:
        return 'Degree'
        
    # Certificate indicators
    if 'certificate' in name_lower or 'astastahiki' in name_lower:
        return 'Certificate'
        
    return 'Diploma'

def university_list(request):
    university = University.objects.all()
    query = request.GET.get('q')
    uni_tpe = request.GET.get('umiliki')
    level = request.GET.get('level')
    
    if query:
        university = university.filter(name__icontains=query)
    if uni_tpe:
        university = university.filter(umiliki__icontains=uni_tpe)
    if level:
        university = university.filter(unicourse__level__icontains=level).distinct()
        
    paginator = Paginator(university, 10)
    page_number = request.GET.get('university_page')
    university = paginator.get_page(page_number)
    return render(request, 'universitysite/university_list.html', {'university': university})

def course_list(request):
    courses = Course.objects.all()
    query = request.GET.get('q')
    uni_tpe = request.GET.get('umiliki')
    level = request.GET.get('level')
    
    if query:
        courses = courses.filter(name__icontains=query)
    if uni_tpe:
        courses = courses.filter(program__university__umiliki__icontains=uni_tpe).distinct()
    if level:
        courses = courses.filter(program__level__icontains=level).distinct()
        
    comb = request.GET.get('combination')
    if comb:
        from django.db.models import Q
        from itertools import combinations
        
        comb_dict = {
            'PCM': ['Physics', 'Chemistry', 'Mathematics'],
            'PCB': ['Physics', 'Chemistry', 'Biology'],
            'PMC': ['Physics', 'Mathematics', 'Computer'],
            'CBG': ['Chemistry', 'Biology', 'Geography'],
            'PGM': ['Physics', 'Geography', 'Mathematics'],
            'EGM': ['Economics', 'Geography', 'Mathematics'],
            'ECA': ['Economics', 'Commerce', 'Accountancy'],
            'HGL': ['History', 'Geography', 'English'],
            'HGK': ['History', 'Geography', 'Kiswahili'],
            'HKL': ['History', 'Kiswahili', 'English'],
            'CBA': ['Chemistry', 'Biology', 'Agriculture'],
            'HGE': ['History', 'Geography', 'Economics'],
            'CBN': ['Chemistry', 'Biology', 'Nutrition'],
        }
        
        if comb in comb_dict:
            subjects = comb_dict[comb]
            q_objects = Q()
            
            # Tafuta kozi zenye angalau masomo MAWILI ya combination
            for pair in combinations(subjects, 2):
                q_objects |= (Q(program__requirements__icontains=pair[0]) & 
                              Q(program__requirements__icontains=pair[1]))
                
            # Pia ruhusu kozi zinazochukua mtu yeyote (any subjects)
            q_objects |= Q(program__requirements__icontains='any subject')
            q_objects |= Q(program__requirements__icontains='any of the following')
            q_objects |= Q(program__requirements__icontains='any two principal')
            
            courses = courses.filter(q_objects).distinct()
            
    paginator = Paginator(courses, 10)
    page_number = request.GET.get('course_page')
    courses = paginator.get_page(page_number)
    return render(request, 'universitysite/course_list.html', {'course': courses})
def home(request):
    university = University.objects.all()
    courses = Course.objects.all()
    region = Region.objects.all()
    
    university_paginator = Paginator(university, 10)
    university_page_number = request.GET.get('university_page')
    university = university_paginator.get_page(university_page_number)
    
    course_paginator = Paginator(courses, 10)
    courses_page_number = request.GET.get('course_page')
    courses = course_paginator.get_page(courses_page_number)
    
    context = {
        'university': university,
        'course': courses,
        'region': region
    }
    return render(request, 'universitysite/home.html', context)

def vyuo_region(request, pk):
    regions = get_object_or_404(Region, pk=pk)
    reg_chuo = University.objects.filter(region=regions)
    return render(request, 'universitysite/reg_chuo.html', {'region': regions, 'reg_chuos': reg_chuo})

def univ_detail(request, pk):
    university = get_object_or_404(University, pk=pk)
    courses = UniversityCourse.objects.filter (university = university) 
    
    course_paginator = Paginator(courses, 10)
    course_page_number = request.GET.get('course_page')
    courses = course_paginator.get_page(course_page_number)
    content = {
        'university': university,
        'course': courses
    }
    return render(request, 'universitysite/uni_details.html', content)

def course_detail(request, pk):
    course_uni = get_object_or_404(UniversityCourse, pk=pk)
    return render(request, 'universitysite/course_detail.html', {'course_uni': course_uni})

def cou_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    universities = UniversityCourse.objects.filter(course = course)
    return render(request, 'universitysite/cou_detail.html', {'university': universities, 'course': course})


    

def region(request):
    region = Region.objects.all()
    return render(request, 'universitysite/region.html', {'region': region})

def about(request):
    return render(request, 'universitysite/about.html')

def contact(request):
    return render(request, 'universitysite/contact.html')

def privacy(request):
    return render(request, 'universitysite/privacy.html')

def feedback(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        message = request.POST.get('message', '').strip()
        if message:
            Feedback.objects.create(name=name if name else None, email=email if email else None, message=message)
            return render(request, 'universitysite/feedback.html', {'success': True})
    return render(request, 'universitysite/feedback.html')


def download_excel(request):
    """
    Download combined_data.xlsx moja kwa moja kupitia browser.
    Inalindwa na login + staff tu (admin). 
    URL: /download/combined-excel/
    """
    import os
    from pathlib import Path
    from django.http import FileResponse, Http404
    from django.contrib.admin.views.decorators import staff_member_required
    from django.contrib.auth.decorators import login_required

    # Ruhusu staff/admin tu - au ondoa check hii kama unataka public
    if not request.user.is_authenticated or not request.user.is_staff:
        from django.contrib.auth.views import redirect_to_login
        return redirect_to_login(request.get_full_path())

    # Pata njia ya faili (manage.py ipo hapa)
    BASE_DIR = Path(__file__).resolve().parent.parent
    excel_path = BASE_DIR / "combined_data.xlsx"

    if not excel_path.exists():
        # Jaribu kutengeneza kwa haraka
        try:
            from django.core.management import call_command
            call_command("export_combined_excel", verbosity=0)
        except Exception:
            pass

    if not excel_path.exists():
        raise Http404(
            "Faili la Excel halipatikani. "
            "Endesha: python manage.py export_combined_excel"
        )

    from datetime import datetime
    filename = f"vyuo_data_{datetime.now().strftime('%Y%m%d')}.xlsx"

    response = FileResponse(
        open(excel_path, "rb"),
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response

@staff_member_required
def upload_excel(request):
    """
    Ruhusu admin/staff ku-upload Excel file moja kwa moja 
    na kuiweka kwenye database.
    """
    import pandas as pd

    context = {}
    if request.method == 'POST' and request.FILES.get('excel_file'):
        excel_file = request.FILES['excel_file']
        
        try:
            # Angalia kama mtumiaji anataka kufuta data za zamani
            wipe_first = request.POST.get('wipe_first') == '1'
            
            if wipe_first:
                UniversityCourse.objects.all().delete()
                Course.objects.all().delete()
                University.objects.all().delete()
                Region.objects.all().delete()
                context['wiped'] = True
            
            # Jaribu kusoma na headers kwanza
            df = pd.read_excel(excel_file, engine='calamine')
            
            # Angalia kama Excel ina headers sahihi au la
            expected_cols = ['Jina la chuo', 'Mkoa', 'Courses']
            has_headers = all(col in df.columns for col in expected_cols)
            
            if not has_headers:
                # Soma upya bila headers na uweke mwenyewe
                excel_file.seek(0)
                df = pd.read_excel(excel_file, header=None, engine='calamine')
                # Chukua columns 8 za kwanza tu
                df = df.iloc[:, :8]
                col_names = ['Jina la chuo', 'Mkoa', 'Umiliki (private/government)', 
                           'Courses', 'Requirements', 'Duration', 
                           'Type (university/institute)', 'Fee']
                df.columns = col_names[:len(df.columns)]
            
            total_imported = 0
            total_skipped = 0
            
            for index, row in df.iterrows():
                uni_name = str(row.get('Jina la chuo', '')).strip()
                region_name = str(row.get('Mkoa', '')).strip()
                umiliki = str(row.get('Umiliki (private/government)', '')).strip()
                course_name = str(row.get('Courses', '')).strip()
                req_text = str(row.get('Requirements', '')).strip()
                duration_val = str(row.get('Duration', '')).strip()
                uni_type = str(row.get('Type (university/institute)', '')).strip()
                fee_val = str(row.get('Fee', '')).strip()
                
                if uni_name == 'nan' or not uni_name or course_name == 'nan' or not course_name:
                    total_skipped += 1
                    continue
                    
                try:
                    if duration_val != 'nan' and duration_val:
                        dur_int = int(float(duration_val))
                        duration_str = str(dur_int)
                        if duration_str not in ['1', '2', '3', '4', '5']:
                            duration_str = '3'
                    else:
                        duration_str = '3'
                except:
                    duration_str = '3'
                    
                if region_name and region_name != 'nan':
                    region_name_clean = region_name[:70]
                else:
                    region_name_clean = "Tanzania"
                    
                region, _ = Region.objects.get_or_create(
                    name__iexact=region_name_clean,
                    defaults={'name': region_name_clean}
                )
                # Update region name kama herufi zimebadilika
                if region.name != region_name_clean:
                    region.name = region_name_clean
                    region.save()
                
                uni_name_clean = uni_name[:150]
                uni_type = uni_type[:40] if uni_type != 'nan' else None
                umiliki = umiliki[:30] if umiliki != 'nan' else None
                if umiliki:
                    umiliki_lower = umiliki.lower()
                    if 'gov' in umiliki_lower or 'pub' in umiliki_lower:
                        umiliki = 'Goverment'
                    elif 'priv' in umiliki_lower:
                        umiliki = 'Private'
                    else:
                        umiliki = None
                
                # Tafuta chuo kwa jina bila kujali herufi kubwa/ndogo
                uni_list = University.objects.filter(name__iexact=uni_name_clean)
                if uni_list.exists():
                    university = uni_list.first()
                    uni_created = False
                    # Kama kuna duplicates za chuo hiki, zifute zibaki moja tu ya kwanza
                    if uni_list.count() > 1:
                        University.objects.filter(name__iexact=uni_name_clean).exclude(id=university.id).delete()
                else:
                    university = University.objects.create(
                        name=uni_name_clean,
                        region=region,
                        type=uni_type,
                        umiliki=umiliki
                    )
                    uni_created = True
                
                if not uni_created:
                    # Daima update taarifa zote za chuo
                    university.name = uni_name_clean
                    if uni_type:
                        university.type = uni_type
                    if umiliki:
                        university.umiliki = umiliki
                    if region:
                        university.region = region
                    university.save()
                
                course_name_clean = course_name[:140]
                # Tafuta kozi kwa jina bila kujali herufi kubwa/ndogo
                course_list = Course.objects.filter(name__iexact=course_name_clean)
                if course_list.exists():
                    course = course_list.first()
                    # Kama kuna duplicates za kozi hii, zifute
                    if course_list.count() > 1:
                        Course.objects.filter(name__iexact=course_name_clean).exclude(id=course.id).delete()
                    # Update jina kama herufi zimebadilika
                    if course.name != course_name_clean:
                        course.name = course_name_clean
                        course.save()
                else:
                    course = Course.objects.create(name=course_name_clean)
                
                req_text = req_text if req_text != 'nan' else ""
                
                fee_clean = None
                if fee_val and fee_val != 'nan':
                    try:
                        fee_clean = float(fee_val.replace(',', ''))
                    except:
                        pass
                
                course_level = determine_course_level(course.name)
                
                uni_course, uc_created = UniversityCourse.objects.get_or_create(
                    university=university,
                    course=course,
                    level=course_level,
                    defaults={
                        'duration': duration_str,
                        'requirements': req_text,
                        'fee': fee_clean
                    }
                )
                
                if not uc_created:
                    uni_course.duration = duration_str
                    uni_course.requirements = req_text
                    if fee_clean is not None:
                        uni_course.fee = fee_clean
                    uni_course.save()
                    
                total_imported += 1

            context['success'] = True
            context['imported_count'] = total_imported
            context['skipped_count'] = total_skipped

        except Exception as e:
            context['error'] = f"Kuna tatizo wakati wa kusoma Excel: {str(e)}"

    return render(request, 'universitysite/upload_excel.html', context)