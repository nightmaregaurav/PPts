from django.contrib import admin

from .models import SiteSetting


@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    def get_actions(self, request):
        if request.user.is_superuser:
            return super(SiteSettingAdmin, self).get_actions(request)
        else:
            return list()

    def get_list_display(self, request):
        return 'key', 'value'

    def has_view_permission(self, request, obj=None):
        if not request.user.is_superuser:
            return False
        else:
            return True

    def has_change_permission(self, request, obj=None):
        if not request.user.is_superuser:
            return False
        else:
            return True

    def has_view_or_change_permission(self, request, obj=None):
        if not request.user.is_superuser:
            return False
        else:
            return True

    def has_delete_permission(self, request, obj=None):
        if not request.user.is_superuser:
            return False
        else:
            return True

    def has_add_permission(self, request):
        if not request.user.is_superuser:
            return False
        else:
            return True

    def has_module_permission(self, request):
        if not request.user.is_superuser:
            return False
        else:
            return True
