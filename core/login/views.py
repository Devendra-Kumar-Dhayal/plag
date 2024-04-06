from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.contrib.auth.decorators import login_required
from .forms import UploadFileForm
from .models import UploadedFile, Group, Profile
from .forms import GroupForm, AddStudentForm

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




@login_required
def teacher_panel(request):
    all_uploaded_files = UploadedFile.objects.all()
    groups = Group.objects.filter(teacher=request.user)
    return render(request, 'login/teacher_panel.html', {'all_uploaded_files': all_uploaded_files, 'groups': groups})



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
def add_student_to_group(request, group_id):
    print(f"Group ID: {group_id}")
    group = get_object_or_404(Group, id=group_id)
    print(f"Group : {group}")
    if request.method == 'POST':
        form = AddStudentForm(group, request.POST)
        if form.is_valid():
            student = form.cleaned_data['student']
            group.students.add(student)
            return redirect('teacher_panel')
    else:
        form = AddStudentForm(group)
    return render(request, 'add_student_to_group.html', {'form': form, 'group': group})



@login_required
def student_panel(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = UploadedFile(user=request.user, file=request.FILES['file'])
            uploaded_file.save()
            return redirect('student_panel')
    else:
        form = UploadFileForm()

    user_uploaded_files = UploadedFile.objects.filter(user=request.user)
    all_uploaded_files = UploadedFile.objects.all()
    return render(request, 'login/student_panel.html', {
        'form': form,
        'user_uploaded_files': user_uploaded_files,
        'all_uploaded_files': all_uploaded_files
    })

@login_required
def group_members(request, group_id):
    group = Group.objects.get(id=group_id)
    members = group.students.all()
    return render(request, 'group_members.html', {'group': group, 'members': members})