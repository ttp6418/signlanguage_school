from django.contrib import admin
from .models import language, user
# Register your models here.

"""admin.site.register(user)
admin.site.register(language)"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import user

admin.site.register(user, UserAdmin)
admin.site.register(language)