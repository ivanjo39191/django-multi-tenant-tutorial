from django.contrib import admin

from customers.models import Client, Domain
from . import forms

class DomainInline(admin.TabularInline):
    model = Domain

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    change_list_template = "customers/change_list.html"
    inlines = [DomainInline]
    list_display = ('schema_name', 'name')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        # 限制特定使用者才可刪除
        if request.user.username.startswith('admin') and request.user.is_superuser:
            return True

    def log_deletion(self, request, object, object_repr):
        
        pass