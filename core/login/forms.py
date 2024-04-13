from django import forms
from .models import Group, User
import re
from django.contrib.admin.widgets import AdminDateWidget
# from bootstrap_datepicker_plus import DatePickerInput

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
    regNo = forms.CharField(label='Registration Number', max_length=50)

    password = forms.CharField(widget=forms.PasswordInput)

class UploadFileForm(forms.Form):
    file = forms.FileField(label='Select a file',required=True)
    group = forms.ModelChoiceField(
        queryset=None,
        label='Select a class',
        required=True
    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['group'].queryset = user.student_groups.all()


class RegistrationForm(forms.Form):

    name = forms.CharField(label='Name', max_length=50, required=True)
    dob = forms.DateField(label='DOB' , required=True ,widget=AdminDateWidget())
    username = forms.CharField(label='Registration Number', max_length=50, required=True)
    
    email = forms.EmailField(label='Email', required=True)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput , required=True)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput ,required=True)
    is_teacher = forms.BooleanField(label='Are you a teacher?', required=False)
    @staticmethod
    def validate_email(email):
        """
        Validates the given email address.
        
        Args:
            email (str): The email address to be validated.
            
        Returns:
            bool: True if the email is valid, False otherwise.
        """
        # Regular expression pattern to match valid email addresses
        pattern = r'^[\w\.-]+@muj.manipal.edu'
        
        # Check if the email matches the pattern
        if re.match(pattern, email):
            return True
        else:
            return False

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists.")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if not RegistrationForm.validate_email(email):
            raise forms.ValidationError("Use Manipal Email")

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