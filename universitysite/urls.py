from django.urls import path
from universitysite import views
app_name = 'universitysite'
urlpatterns = [
    path('', views.home, name = 'home'),
    path('home/course/<int:pk>/', views.course_detail, name='course_detail'),
    path('home/university/<int:pk>/', views.univ_detail, name='universi'),
    path('home/<int:pk>/', views.cou_detail, name = 'cou'),
    
    path('home/region/', views.region, name = 'region'),
    path('home/universities/', views.university_list, name = 'university_list'),
    path('home/courses/', views.course_list, name = 'course_list'),
    
]
