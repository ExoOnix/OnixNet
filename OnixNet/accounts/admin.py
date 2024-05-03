from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


admin.site.register(User, UserAdmin)
admin.site.site_header = "OnixNet"
admin.site.site_title = "OnixNet Admin Portal"
admin.site.index_title = "Welcome to the OnixNet Portal"