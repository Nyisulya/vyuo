from django.shortcuts import render, get_object_or_404
from .models import Region, University, Course, UniversityCourse
from django.core.paginator import Paginator
# Create your views here.
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
                q_objects |= (Q(program__requirements__description__icontains=pair[0]) & 
                              Q(program__requirements__description__icontains=pair[1]))
                
            # Pia ruhusu kozi zinazochukua mtu yeyote (any subjects)
            q_objects |= Q(program__requirements__description__icontains='any subject')
            q_objects |= Q(program__requirements__description__icontains='any of the following')
            q_objects |= Q(program__requirements__description__icontains='any two principal')
            
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