from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


from .models import *

# Register your models here.
admin.site.register(Speaker)
admin.site.register(Event)
admin.site.register(Place)
admin.site.register(Path)
admin.site.register(Timetable)

# Change user display in admin site for the USerDetails to be coupled
# with user and easily editable
class ProfileInline(admin.StackedInline):
    model = UserDetails
    can_delete = False
    verbose_name_plural = 'UserDetails'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)