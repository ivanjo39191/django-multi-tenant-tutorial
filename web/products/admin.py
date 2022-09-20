from django.contrib import admin
from products.models import Product, ProductCategory

# Register your models here.
admin.site.register(Product)         # 註冊 Product 模型
admin.site.register(ProductCategory)    # 註冊 ProductCategory 模型