from django.contrib import admin
from . models import *

# Register your models here.
@admin.register(UserType)
class UserTypeAdmin(admin.ModelAdmin):
  list_display = ['id','user', 'user_roll', 'mobile']





admin.site.register(EstateProperty)
admin.site.register(Address)
admin.site.register(Feature)
admin.site.register(PropertyPhoto)
