from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.contrib.auth.decorators import login_required
from .forms import UploadFileForm
from .models import UploadedFile, Group, Profile,User
from .forms import GroupForm, AddStudentForm
from .forms import RegistrationForm


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            is_teacher = form.cleaned_data['is_teacher']
            user = User.objects.create_user(username=username, email=email, password=password)
            profile = Profile.objects.create(user=user, is_teacher=is_teacher)
            return redirect('login')  # replace 'login' with the name of your login URL
    else:
        form = RegistrationForm()
    return render(request, 'login/register.html', {'form': form})

def home_view(request):
    return redirect('login')

def login_view(request):
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                if user.profile.is_teacher:
                    return redirect('teacher_panel')
                else:
                    return redirect('student_panel')
    else:
        form = LoginForm()

    return render(request, 'login/login.html', {'form': form})




# @login_required
# def teacher_panel(request):
#     all_uploaded_files = UploadedFile.objects.all()
#     groups = Group.objects.filter(teacher=request.user)
#     return render(request, 'login/teacher_panel.html', {'all_uploaded_files': all_uploaded_files, 'groups': groups})
# views.py
@login_required
def teacher_panel(request):
    groups = Group.objects.filter(teacher=request.user)

    selected_group = request.GET.get('group')
    if selected_group:
        group = Group.objects.get(id=selected_group)
        group_uploaded_files = UploadedFile.objects.filter(group=group)
    else:
        group_uploaded_files = UploadedFile.objects.filter(group__in=groups)

    return render(request, 'login/teacher_panel.html', {
        'groups': groups,
        'group_uploaded_files': group_uploaded_files,
        'selected_group': selected_group
    })



@login_required
def create_group(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.teacher = request.user
            group.save()
            return redirect('teacher_panel')
    else:
        form = GroupForm()
    return render(request, 'create_group.html', {'form': form})


@login_required
def remove_student_from_group(request, group_id, user_id):
    group = get_object_or_404(Group, id=group_id, teacher=request.user)
    student = get_object_or_404(User, id=user_id)
    group.students.remove(student)
    return redirect('group_members', group_id=group_id)

@login_required
def delete_group(request, group_id):
    group = get_object_or_404(Group, id=group_id, teacher=request.user)
    group.delete()
    return redirect('teacher_panel')



@login_required
def student_panel(request):
    if request.method == 'POST':
        form = UploadFileForm(request.user,request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = UploadedFile(
                user=request.user,
                file=request.FILES['file'],
                group=form.cleaned_data['group']
            )
            uploaded_file.save()
            return redirect('student_panel')
    else:
        form = UploadFileForm(request.user)
        user_groups = request.user.student_groups.all()
        user_uploaded_files = UploadedFile.objects.filter(user=request.user, group__in=user_groups)
        all_uploaded_files = UploadedFile.objects.filter(group__in=user_groups)

    return render(request, 'login/student_panel.html', {
        'form': form,
        'user_uploaded_files': user_uploaded_files,
        'all_uploaded_files': all_uploaded_files
    })

@login_required
def group_members(request, group_id):
    # group = Group.objects.get(id=group_id)
    
    group = get_object_or_404(Group, id=group_id)
    members = group.students.all()
    print(f"Group : {group}")
    if request.method == 'POST':
        form = AddStudentForm(group, request.POST)
        if form.is_valid():
            student = form.cleaned_data['student']
            group.students.add(student)
            return redirect('teacher_panel')
    else:
        form = AddStudentForm(group)
    return render(request, 'login/group_members.html', {'group': group, 'members': members, 'form':form})