from django.contrib import admin
from .models import *

class ProfileModelInline(admin.StackedInline):
    model = ProfileModel
    can_delete = False 
    verbose_name_plural = 'Profile'
class UserAdmin(admin.ModelAdmin):
    inlines = (ProfileModelInline,)
    list_display = ('email', 'username', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

admin.site.register(CustomUser, UserAdmin)

admin.site.register(Post)
admin.site.register(Comment)