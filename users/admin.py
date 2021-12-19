from django.contrib import admin


# Register your models here.

from .models import Profiles,Skill,Message

admin.site.register(Profiles)
admin.site.register(Skill)
admin.site.register(Message)