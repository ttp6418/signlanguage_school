from django.contrib import admin
from accounts.models import language, user
# Register your models here.

"""admin.site.register(user)
admin.site.register(language)"""

from django.contrib.auth.admin import UserAdmin

admin.site.register(user, UserAdmin)
admin.site.register(language)