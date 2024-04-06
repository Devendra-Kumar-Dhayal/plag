from django.contrib import admin
from django.urls import path
from .views import login_view, teacher_panel, student_panel,home_view,create_group,add_student_to_group,group_members
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', home_view, name='home'),
    path('login/', login_view, name='login'),
    path('teacher-panel/', teacher_panel, name='teacher_panel'),
    path('add-student-to-group/<int:group_id>/', add_student_to_group, name='add_student_to_group'),
    path('create-group/', create_group, name='create_group'),
    path('group/<int:group_id>/members/', group_members, name='group_members'),
    path('student-panel/', student_panel, name='student_panel'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)