import os
from django.conf import settings
from django.contrib import admin
from django.db import connection
from django.utils.translation import to_locale


# Register your models here.
from core.models import Setting, LocaleSetting, TranslateSetting, Locale


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
        ('郵件設定', {
            'classes': (
                'tab',
                'tab-mail',
            ),
            'fields': (
                'from_email',
            )
        }),
    ]


class TranslateSettingInline(admin.TabularInline):
    model = TranslateSetting
    fields = ('raw_string', 'translated_string')

class LocaleSettingAdmin(admin.ModelAdmin):
    search_fields = ['id', 'language']
    fields = ('id', 'language')
    list_display = ('id', 'language')
    inlines = [TranslateSettingInline, ]

    def save_related(self, request, form, formsets, change):
        super(LocaleSettingAdmin, self).save_related(request, form, formsets, change)
        locale_id = (to_locale(form.instance.id))
        locale_path = os.path.join(settings.BASE_DIR, f'tenant_locale/{connection.schema_name}/{locale_id}/LC_MESSAGES/')
        message_file = 'msgid ""\n' + \
        'msgstr ""\n' + \
        '"Project-Id-Version: PACKAGE VERSION\\n"\n' + \
        '"Report-Msgid-Bugs-To: \\n"\n' + \
        '"POT-Creation-Date: 2022-10-01 15:59+0800\\n"\n' + \
        '"PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\\n"\n' + \
        '"Last-Translator: FULL NAME <EMAIL@ADDRESS>\\n"\n' + \
        '"Language-Team: LANGUAGE <LL@li.org>\\n"\n' + \
        '"Language: \\n"\n' + \
        '"MIME-Version: 1.0\\n"\n' + \
        '"Content-Type: text/plain; charset=UTF-8\\n"\n' + \
        '"Content-Transfer-Encoding: 8bit\\n"\n' + \
        '"Plural-Forms: nplurals=1; plural=0;\\n"\n\n' 

        for trans_obj in form.instance.translatesetting_set.all():
            message_file += f'msgid "{trans_obj.raw_string}"\n'
            message_file += f'msgstr "{trans_obj.translated_string}"\n\n'
        with open(f"{locale_path}/django.po" , "w") as f:
            f.write(message_file)
        os.system(f"cd {locale_path} && msgfmt django.po -o django.mo")

admin.site.register(Setting, SettingAdmin) 
admin.site.register(LocaleSetting, LocaleSettingAdmin) 
admin.site.register(Locale) 