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
    file = forms.FileField(label='Select a file')