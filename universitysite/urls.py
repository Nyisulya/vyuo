from django.urls import path
from universitysite import views
app_name = 'universitysite'
urlpatterns = [
    path('', views.home, name = 'home'),
    path('homes/<int:pk>/', views.vyuo_region, name='vyuo'),
    path('home/course/<int:pk>/', views.course_detail, name='course_detail'),
    path('home/university/<int:pk>/', views.univ_detail, name='universi'),
    path('home/<int:pk>/', views.cou_detail, name = 'cou'),
    
    path('home/region/', views.region, name = 'region'),
    path('home/universities/', views.university_list, name = 'university_list'),
    path('home/courses/', views.course_list, name = 'course_list'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('privacy/', views.privacy, name='privacy'),
    path('feedback/', views.feedback, name='feedback'),
    path('download/combined-excel/', views.download_excel, name='download_excel'),
    path('upload-excel/', views.upload_excel, name='upload_excel'),
]
