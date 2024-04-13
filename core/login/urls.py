from django.contrib import admin
from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView


urlpatterns = [
    # pages 
    
    path('', home_view, name='home'),
    path('login/', login_view, name='login'),
    path('teacher-panel/', teacher_panel, name='teacher_panel'),
    path('create-group/', create_group, name='create_group'),
    path('group/<int:group_id>/members/', group_members, name='group_members'),
    path('student-panel/', student_panel, name='student_panel'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('remove-student-from-group/<int:group_id>/<int:user_id>/', remove_student_from_group, name='remove_student_from_group'),

    # api 
    path('delete-group/<int:group_id>/', delete_group, name='delete_group'),
    path('register/', register, name='register'),
    # path('verify-email/', verify_email, name='verify_email'),
    path('verify-otp/', verify_otp, name='verify_otp'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)