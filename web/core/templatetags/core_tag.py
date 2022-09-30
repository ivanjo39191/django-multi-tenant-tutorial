from django import template
register = template.Library()

from core.models import Setting

@register.simple_tag
def get_setting():
    setting = Setting.objects.get(id='zh-hant')
    setting_dict = Setting.objects.get(id='zh-hant').__dict__
    setting_dict['home_type1'] = setting.home_type1.__dict__ if setting.home_type1 else None
    setting_dict['home_type2'] = setting.home_type2.__dict__ if setting.home_type2 else None
    setting_dict['home_type3'] = setting.home_type3.__dict__ if setting.home_type3 else None
    return setting_dict

