from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm

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
    # Code for the teacher panel
    return render(request, 'login/teacher_panel.html')

def student_panel(request):
    # Code for the student panel
    return render(request, 'login/student_panel.html')