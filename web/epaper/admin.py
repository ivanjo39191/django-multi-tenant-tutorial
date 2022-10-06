from django.contrib import admin

# Register your models here.
from epaper.models import EPaperEmail

admin.site.register(EPaperEmail)         # 註冊 EPaperEmail 模型