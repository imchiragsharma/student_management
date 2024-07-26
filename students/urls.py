from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.universal_login, name='universal_login'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('parent/dashboard/', views.parent_dashboard, name='parent_dashboard'),
    path('api/students/', views.StudentList.as_view(), name='student-list'),
    path('api/students/<int:pk>/', views.StudentDetail.as_view(), name='student-detail'),
    path('api/parents/', views.ParentList.as_view(), name='parent-list'),
    path('api/parents/<int:pk>/', views.ParentDetail.as_view(), name='parent-detail'), 
]