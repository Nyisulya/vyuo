from django.shortcuts import render, get_object_or_404
from .models import Region, University, Course, UniversityCourse
from django.core.paginator import Paginator
# Create your views here.
def home(request):
    
    university = University.objects.all()
    courses = Course.objects.all()
    unicourse = UniversityCourse.objects.all()
    query = request.GET.get('q')

    uni_tpe = request.GET.get('umiliki')
    unifo = request.GET.get('level')

    if uni_tpe:
        university = university.filter(umiliki__icontains=uni_tpe)
    if query:
        university = university.filter(name__icontains=query)
        courses = courses.filter(name__icontains=query)
    if unifo:
        unicourse = unicourse.filter(level__icontains=unifo)

    university_paginator = Paginator(university, 10)
    university_page_number = request.GET.get('university_page')
    university = university_paginator.get_page(university_page_number)
    course_paginator = Paginator(courses, 10)
    courses_page_number = request.GET.get('course_page')
    courses = course_paginator.get_page(courses_page_number)
    context = {
        'university': university,
        'course': courses,
        'unicourses': unicourse
    }
    
    return render(request, 'universitysite/home.html', context)

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

def vyuo_region(request,pk):
    regions = get_object_or_404(Region,pk=pk)
    reg_chuo = University.objects.filter(region = regions)
    return render(request, 'universitysite/reg_chuo.html', {'region': regions, 'reg_chuos': reg_chuo})

def region(request):
    region = Region.objects.all()
    return render(request, 'universitysite/region.html', {'region': region})