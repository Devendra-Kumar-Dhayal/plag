from django import forms
from .models import Group, User

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name']

class AddStudentForm(forms.Form):
    student = forms.ModelChoiceField(queryset=User.objects.filter(profile__is_teacher=False), label='Select Student')

    def __init__(self, group, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.group = group
        self.fields['student'].queryset = User.objects.filter(profile__is_teacher=False).exclude(groups__in=[group.id])

class LoginForm(forms.Form):
    email = forms.EmailField()

    password = forms.CharField(widget=forms.PasswordInput)

class UploadFileForm(forms.Form):
    file = forms.FileField(label='Select a file',required=True)
    group = forms.ModelChoiceField(
        queryset=None,
        label='Select a group',
        required=True
    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['group'].queryset = user.student_groups.all()


class RegistrationForm(forms.Form):
    username = forms.CharField(label='Username', max_length=50)
    number = forms.IntegerField(label= 'Registration Number')
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    is_teacher = forms.BooleanField(label='Are you a teacher?', required=False)



    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists.")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data