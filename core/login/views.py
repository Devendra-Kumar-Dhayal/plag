from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.contrib.auth.decorators import login_required
from .forms import UploadFileForm
from .models import UploadedFile

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

def teacher_panel(request):
    all_uploaded_files = UploadedFile.objects.all()
    return render(request, 'login/teacher_panel.html', {'all_uploaded_files': all_uploaded_files})




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

