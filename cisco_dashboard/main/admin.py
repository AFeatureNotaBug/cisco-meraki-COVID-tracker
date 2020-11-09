from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import UserProfile

class ProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )

    #list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_apikey')
    list_display = ('username', 'email', 'is_staff', 'get_apikey')

    list_select_related = ('userprofile', )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

    def get_apikey(self, instance):
        print(instance.userprofile.apikey)
        return instance.userprofile.apikey
    get_apikey.short_description = 'APIKey'

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)