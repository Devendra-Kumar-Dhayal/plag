from django.contrib import admin
from django.urls import path
from .views import login_view, teacher_panel, student_panel

urlpatterns = [

    path('login/', login_view, name='login'),
    path('teacher-panel/', teacher_panel, name='teacher_panel'),
    path('student-panel/', student_panel, name='student_panel'),
]