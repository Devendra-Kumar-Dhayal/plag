from django import forms

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)



class UploadFileForm(forms.Form):
    file = forms.FileField(label='Select a file')