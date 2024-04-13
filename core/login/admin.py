from django.contrib import admin
from .models import Profile,Group,UploadedFile

# Register your models here.

admin.site.register(Profile)
admin.site.register(Group)
admin.site.register(UploadedFile)



# Change the site title
admin.site.site_title = "Report Manager"

# Change the site header
admin.site.site_header = "Coordinator"
