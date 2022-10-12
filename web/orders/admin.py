from django.contrib import admin

# Register your models here.
from orders.models import Order
from products.models import RelationalProduct

class RelationalProductInline(admin.TabularInline):
    model = RelationalProduct
    model = Order.product.through
    verbose_name = '商品名稱'
    extra = 2
    fields = ('name', 'price', 'number')
    readonly_fields = ('name', 'price', 'number')

    def has_add_permission(self, request, obj):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

class OrderAdmin(admin.ModelAdmin):
    model = Order
    search_fields = ['order_id', 'name']
    fields = ('order_id', 'name', 'email', 'phone', 'district', 'zipcode', 'address', 'total', 'status', 'created', 'modified')
    list_display = ('order_id', 'name', 'email', 'total')
    list_filter = ('status',)
    readonly_fields = ('order_id', 'name', 'email', 'phone', 'district', 'zipcode', 'address', 'total', 'created', 'modified')
    inlines = [RelationalProductInline,]

admin.site.register(Order, OrderAdmin)   