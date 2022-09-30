from django.db import models
from core import helpers

# Create your models here.
class Setting(models.Model):
    id = models.CharField('語言代碼', max_length=10, primary_key=True)
    language = models.CharField('系統語言', max_length=50)
    sitename = models.CharField(
        '系統名稱', default='', null=True, max_length=100, blank=True
    )
    phone = models.CharField(
        '電話', default='', null=True, max_length=100, blank=True
    )
    logo = models.FileField(
        "logo 圖片", null=True, blank=True, upload_to=helpers.upload_handle
    )
    favicon = models.FileField(
        "favicon 圖片", null=True, blank=True, upload_to=helpers.upload_handle
    )
    style = models.FileField(
        "CSS樣式", null=True, blank=True, upload_to=helpers.upload_handle
    )
    home_type1 = models.ForeignKey(
        'products.ProductCategory', blank=True, null=True, 
        on_delete=models.RESTRICT, verbose_name='左上商品分類', related_name='home_type1_set'
    )
    home_type2 = models.ForeignKey(
        'products.ProductCategory', blank=True, null=True, 
        on_delete=models.RESTRICT, verbose_name='左下商品分類', related_name='home_type2_set'
    )
    home_type3 = models.ForeignKey(
        'products.ProductCategory', blank=True, null=True, 
        on_delete=models.RESTRICT, verbose_name='右側商品分類', related_name='home_type3_set'
    )
    detail_template = models.CharField(
        '詳細頁面版型', 
        max_length=100, 
        choices=(("Template-1", "版型一"),("Template-2", "版型二")), 
        default="Template-1"
    )
    facebook = models.CharField(
        'Facebook 連結', default='', null=True, max_length=100, blank=True
    )
    instagram = models.CharField(
        'Instagram 連結', default='', null=True, max_length=100, blank=True
    )
    twitter = models.CharField(
        'Twitter 連結', default='', null=True, max_length=100, blank=True
    )
    class Meta:
        verbose_name = '網站設定'
        verbose_name_plural = '網站設定'

    def __str__(self):
        return "%s" % (self.language)