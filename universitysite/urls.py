from django.urls import path
from universitysite import views
app_name = 'universitysite'
urlpatterns = [
    path("home/", views.home, name = 'home'),
    path('home/course/<int:pk>/', views.course_detail, name='course_detail'),
    path('home/university/<int:pk>/', views.univ_detail, name='universi'),
    path('home/<int:pk>/', views.cou_detail, name = 'cou'),
    path('homes/<int:pk>/', views.vyuo_region, name= 'vyuo'),
    path('home/region/', views.region, name = 'region'),
]
