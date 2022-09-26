from django.db import models
from core import helpers as core_helpers

# Create your models here.
class Product(models.Model):
    '''
    商品模型
    '''
    name = models.CharField('商品名稱', max_length=50)
    description = models.TextField('商品描述', max_length=500, null=True, blank=True)
    price = models.PositiveIntegerField('商品價格', default=0)
    created = models.DateTimeField('建立日期', auto_now_add=True)
    modified = models.DateTimeField('修改日期', auto_now=True)
    category = models.ForeignKey(
        'products.ProductCategory', blank=True, null=True, 
        on_delete=models.RESTRICT, verbose_name='商品分類', related_name='product_set'
    )

    class Meta:
        verbose_name = '商品'
        verbose_name_plural = '商品'
        ordering = ['-created']

    def __str__(self):
        return f'{self.name}'


class ProductCategory(models.Model):
    '''
    商品分類模型
    '''
    name = models.CharField('商品分類名稱', max_length=50)
    description = models.TextField('商品分類描述', max_length=500, null=True, blank=True)
    created = models.DateTimeField('建立日期', auto_now_add=True)
    modified = models.DateTimeField('修改日期', auto_now=True)
    image = models.ImageField("圖片", null=True, blank=True, upload_to=core_helpers.upload_handle)

    class Meta:
        verbose_name = '商品分類'
        verbose_name_plural = '商品分類'
        ordering = ['-created']

    def __str__(self):
        return f'{self.name}'


class ProductImage(models.Model):
    name = models.CharField('商品圖片說明', max_length=50)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='product_set')
    image = models.ImageField("圖片", null=True, blank=True, upload_to=core_helpers.upload_handle)
    order = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        verbose_name = '商品圖片'
        verbose_name_plural = '商品圖片'
        ordering = ['order']

    def __str__(self):
        return f'{self.name}'