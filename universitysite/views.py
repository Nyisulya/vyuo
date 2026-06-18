from django.shortcuts import render, get_object_or_404
from .models import Region, University, Course, UniversityCourse
from django.core.paginator import Paginator
# Create your views here.
def university_list(request):
    university = University.objects.all()
    query = request.GET.get('q')
    if query:
        university = university.filter(name__icontains=query)
    paginator = Paginator(university, 10)
    page_number = request.GET.get('page')
    university = paginator.get_page(page_number)
    return render(request, 'universitysite/university_list.html', {'university': university})
def course_list(request):
    courses = Course.objects.all()
    query = request.GET.get('q')
    if query:
        courses = courses.filter(name__icontains=query)
    paginator = Paginator(courses, 10)
    page_number = request.GET.get('page')
    courses = paginator.get_page(page_number)
    return render(request, 'universitysite/course_list.html', {'course': courses})
def home(request,pk):
    
    regions = get_object_or_404(Region,pk=pk)
    reg_chuo = University.objects.filter(region = regions)
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