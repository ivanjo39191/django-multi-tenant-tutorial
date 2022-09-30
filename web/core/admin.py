from django.contrib import admin

# Register your models here.
from core.models import Setting

class SettingAdmin(admin.ModelAdmin):
    fieldsets = [
        ('語言', {
            'fields': (
                'id',
                'language',
            )
        }),
        ('網站資訊設定', {
            'classes': (
                'tab',
                'tab-general',
            ),
            'fields': (
                'sitename',
                'phone',
            )
        }),
        ('樣式設定', {
            'classes': (
                'tab',
                'tab-style',
            ),
            'fields': (
                'logo',
                'favicon',
                'style',
            )
        }),
        ('首頁設定', {
            'classes': (
                'tab',
                'tab-home',
            ),
            'fields': (
                'home_type1',
                'home_type2',
                'home_type3',
            )
        }),
        ('商品詳細頁設定', {
            'classes': (
                'tab',
                'tab-detail',
            ),
            'fields': (
                'detail_template',
            )
        }),
        ('更多資訊設定', {
            'classes': (
                'tab',
                'tab-more',
            ),
            'fields': (
                'facebook',
                'instagram',
                'twitter',
            )
        }),
    ]

admin.site.register(Setting, SettingAdmin) 