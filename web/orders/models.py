from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Order(models.Model):
    '''
    訂單
    '''
    order_id = models.CharField(_('Order Id'), max_length=20)
    email = models.EmailField('E-mail', max_length=255)
    product = models.ManyToManyField('products.Product', related_name='order_set', through='products.RelationalProduct')
    name = models.CharField(_('Name'), max_length=50)
    phone = models.CharField(_('Phone'), max_length=50)
    district = models.CharField(_('District'), max_length=50)
    zipcode = models.CharField(_('Zip Code'), max_length=50)
    address = models.CharField(_('Address'), max_length=255)
    total = models.PositiveIntegerField(_('Total'), default=0)
    created = models.DateTimeField(_('Created Date'), auto_now_add=True)
    modified = models.DateTimeField(_('Modified Date'), auto_now=True)
    status = models.CharField(
        _('Status'), 
        max_length=100, 
        choices=(("unpaid", _("Unpaid")), ("payment_fail", _("Payment Fail")), ("waiting_for_shipment", _("Waiting for shipment")), ("transporting", _("Transporting")), ("completed", _("Completed")), ("cancelled", _("Cancelled"))), 
        default="unpaid"
    )
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.order_id:
            self.order_id = f'ORDER{self.id:08}'
            super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = '訂單'
        verbose_name_plural = '訂單'

    def __str__(self):
        return f'{self.order_id}'